from urllib.parse import urlparse
from http import HTTPStatus
import json
import os
import requests
import sys


def create_link(head, long_url, key):
    """
    Shortens a long URL into a TinyURL short link URL
    :param head: request headers (API key and content type)
    :param long_url: a properly-formatted URL
    :param key: the TinyURL API key for the user
    :return: a properly-formatted TinyURL short link URL
    """
    short_url = None

    # convert the URL parameters to JSON
    data = {
        'url': long_url,
        'domain': 'tinyurl.com'
    }
    data = json.dumps(data)

    # send the request to the TinyURL API and parse the JSON response for a 'content' field
    response = requests.post('https://api.tinyurl.com/create?api_token=' + key, headers=head, data=data)
    re_json = json.loads(response.content)
    try:
        short_url = (re_json['data'])['tiny_url']
    except KeyError:
        # the JSON content couldn't be found, the error will be printed in the return
        pass

    return response, short_url


def update_custom(head, old_link, new_link, key):
    """
    Changes the ending of a TinyURLID
    :param head: request headers (API key and content type)
    :param old_link: a properly-formatted TinyURL ID to change
    :param new_link: an unused, properly-formatted TinyURL ID
    :param key: the TinyURL API key for the user
    :return: boolean indicating the status of the change
    """
    # convert the URL parameters to JSON
    data = {
        'domain': "tinyurl.com",
        'alias': old_link,
        'new_domain': "tinyurl.com",
        'new_alias': new_link.split('/')[1],
    }
    data = json.dumps(data)

    # send the request to the TinyURL API and obtain the response
    response = requests.patch('https://api.tinyurl.com/update?api_token=' + key, headers=head, data=data)
    return response


def create_short_url(key, long, short):
    """
    Create a TinyURL ID given a long URL
    :param key: the TinyURL API key for the user
    :param long: a properly-formatted long URL
    :param short: a properly-formatted TinyURL ID
    :return: status code of the result
    """
    # insert the api key into the request headers
    headers = {
        'Authorization': 'Bearer {}'.format(key),
        'Content-Type': 'application/json',
    }

    # create a TinyURL ID from a long URL
    result, tinyurl_link = create_link(headers, long, key)

    # return details of the result if unsuccessful
    if ((result.status_code != HTTPStatus.OK) and (result.status_code != HTTPStatus.CREATED)) or tinyurl_link is None:

        result_content = json.loads(result.content.decode('utf-8'))
        message = result_content.get('message')
        print('fail: error', result.status_code, 'creating the initial short link from', long, "due to", message, file=sys.stderr)
        return result

    # parse the HTTP link to a TinyURL ID
    parsed_tinyurl_link = urlparse(tinyurl_link)
    tinyurl_id = parsed_tinyurl_link.path[1:]

    # change the TinyURL ID to have a custom ending
    result = update_custom(headers, tinyurl_id, short, key)

    # return details of the result if unsuccessful
    if result.status_code != HTTPStatus.OK:
        # the response returned something else
        result_content = json.loads(result.content.decode('utf-8'))
        message = result_content.get('errors')[0]
        print('fail: error', result.status_code, 'creating new short link', short, 'from generated link', 'tinyurl.com/' + tinyurl_id,
              'for', long, "due to", message, file=sys.stderr)
        return result

    # return the status code of the change
    return result


if __name__ == '__main__':
    # check to see if the API keys file exists
    if not os.path.isfile("api_keys.txt"):
        print('file error: missing api_keys.txt', file=sys.stderr)
        exit(1)

    # load the API keys
    tinyurl_api_key = ""

    with open("api_keys.txt", "r") as api_keys:
        for line in api_keys:
            if "tinyurl:" in line:
                try:
                    tinyurl_api_key = line.strip().split()[1]
                except IndexError:
                    print('file error: TinyURL API key missing or formatted improperly', file=sys.stderr)
                    exit(1)
            else:
                print('file error: no API keys identified', file=sys.stderr)
                exit(1)

    url_to_shorten = input('Enter a URL to shorten:')
    change_to = input('Enter a new TinyURL ID to shorten to:')

    # shorten the URL
    results = create_short_url(tinyurl_api_key, url_to_shorten, change_to)

    # print the result
    if results.status_code == HTTPStatus.OK:
        print('Success!')
