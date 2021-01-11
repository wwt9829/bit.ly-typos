from urllib.parse import urlparse
from http import HTTPStatus
import json
import requests
import sys


def create_link(head, long_url):
    """
    Shortens a long URL into a bit.ly short link URL
    :param head: request headers (API key and content type)
    :param long_url: a properly-formatted URL
    :return: a properly-formatted bit.ly short link URL
    """
    short_url = None

    # convert the URL parameters to JSON
    data = {
        'long_url': long_url,
        'domain': 'bit.ly'
    }
    data = json.dumps(data)

    # send the request to the bit.ly API and parse the JSON response for a 'content' field
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=head, data=data)
    re_json = json.loads(response.content)
    try:
        short_url = re_json['link']
    except KeyError as ke:
        # the JSON content couldn't be found, print the error
        print('KeyError:', ke, file=sys.stderr)

    return response, short_url


def update_custom(head, old_link, new_link):
    """
    Changes the ending of a bit.ly ID
    :param head: request headers (API key and content type)
    :param old_link: a properly-formatted bitlink ID to change
    :param new_link: an unused, properly-formatted bitlink ID
    :return: boolean indicating the status of the change
    """
    # convert the URL parameters to JSON
    data = {
        'custom_bitlink': new_link,
        'bitlink_id': old_link
    }
    data = json.dumps(data)

    # send the request to the bit.ly API and obtain the response
    response = requests.post('https://api-ssl.bitly.com/v4/custom_bitlinks', headers=head, data=data)
    return response


def create_short_url(key, long, short):
    """
    Create a bit.ly ID given a long URL
    :param key: the bit.ly API key for the user
    :param long: a properly-formatted long URL
    :param short: a properly-formatted bit.ly ID
    :return: status code of the result
    """
    # insert the api key into the request headers
    headers = {
        'Authorization': 'Bearer {}'.format(key),
        'Content-Type': 'application/json',
    }

    # create a bit.ly ID from a long URL
    result, bitly_link = create_link(headers, long)

    # return details of the result if unsuccessful
    if ((result.status_code != HTTPStatus.OK) and (result.status_code != HTTPStatus.CREATED)) or bitly_link is None:
        print('fail: error', result.status_code, 'creating the initial short link from', long, file=sys.stderr)
        print(result.content, file=sys.stderr)
        return result

    # parse the HTTP link to a bit.ly ID
    parsed_bitly_link = urlparse(bitly_link)
    bitly_id = parsed_bitly_link.netloc + parsed_bitly_link.path

    # change the bit.ly ID to have a custom ending
    result = update_custom(headers, bitly_id, short)

    # return details of the result if unsuccessful
    if result.status_code != HTTPStatus.OK:
        # the response returned something else
        print('fail: error', result.status_code, 'creating new short link', short, 'from generated link', bitly_id,
              'for', long, file=sys.stderr)
        print(result.content, file=sys.stderr)

    # return the status code of the change
    return result


if __name__ == '__main__':
    # check to see if the API key was supplied in program arguments, and exit if not
    if len(sys.argv) != 2:
        print('argument error: missing API key', file=sys.stderr)
        exit(1)
    api_key = sys.argv[1]

    url_to_shorten = input('Enter a URL to shorten:')
    change_to = input('Enter a new bit.ly ID to shorten to:')

    # shorten the URL
    results = create_short_url(api_key, url_to_shorten, change_to)

    # print the result
    if results.status_code == HTTPStatus.OK:
        print('Success!')
