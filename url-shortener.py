from urllib.parse import urlparse
from http import HTTPStatus
import json
import requests
import sys

# TODO: exception handling so the program can continue making URLs if one fails

def create_link(head, long_url):
    """
    Shortens a long URL into a bit.ly short link URL
    :param head: request headers (API key and content type)
    :param long_url: a properly-formatted URL (TODO: implement a check for this)
    :return: a properly-formatted bit.ly short link URL
    """
    # convert the URL parameters to JSON
    data = {
        'long_url': long_url,
        'domain': 'bit.ly'
    }
    data = json.dumps(data)

    # TODO: try/except for json dump

    # send the request to the bit.ly API and parse the JSON response for a 'content' field
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=head, data=data)
    re_json = json.loads(response.content)
    try:
        short_url = re_json["link"]
        if response.status_code == HTTPStatus.CREATED:
            # the response returned a CREATED status code, return CREATED and the URL
            return HTTPStatus.CREATED, short_url
        elif response.status_code == HTTPStatus.OK:
            # the response returned an OK status code, return OK and the URL
            return HTTPStatus.OK, short_url
        else:
            # the response returned something else, print the error and exit the program
            print("fail:", response.status_code)
            exit()

    except KeyError:
        # the JSON content couldn't be found, print the error and exit the program
        # TODO: print the actual error
        print("fail: error reading JSON.")
        exit()


def update_custom(head, old_link, new_link):
    """
    Changes the ending of a bit.ly short URL
    :param head: request headers (API key and content type)
    :param old_link: a bitlink ID to change
    :param new_link: an unused bitlink ID
    :return: boolean indicating the status of the change
    """
    # convert the URL parameters to JSON
    data = {
        'custom_bitlink': new_link,
        'bitlink_id': old_link
    }
    data = json.dumps(data)

    # TODO: try/except for json dump

    # send the request to the bit.ly API and obtain the response
    response = requests.post('https://api-ssl.bitly.com/v4/custom_bitlinks', headers=head, data=data)

    if response.status_code == HTTPStatus.OK:
        # the response returned an OK status code, return True
        return HTTPStatus.OK
    else:
        # the response returned something else, exit the program
        print('fail:', response.status_code, ".")
        exit()


if __name__ == "__main__":
    # check to see if the API key was supplied in program arguments
    # TODO: move somewhere else?
    if len(sys.argv) != 2:
        print("Argument error: missing API key")
        exit()

    # obtain the API key and insert it into the request headers
    # TODO: move somewhere else?
    api_key = sys.argv[1]
    headers = {
        'Authorization': 'Bearer {}'.format(api_key),
        'Content-Type': 'application/json',
    }

    # the URL to shorten
    # TODO: replace
    url_to_shorten = 'https://example.net/'

    # create a bit.ly short URL from a long URL
    print('Shortening', url_to_shorten, 'to a bit.ly link', end="...")
    result, bitly_link = create_link(headers, url_to_shorten)

    # print the result
    if result == HTTPStatus.CREATED:
        print('created!')
    if result == HTTPStatus.OK:
        print('already exists!')

    # parse the HTTP link to a bit.ly short URL
    parsed_bitly_link = urlparse(bitly_link)
    bitly_id = parsed_bitly_link.netloc + parsed_bitly_link.path

    # the custom bit.ly short URL to use
    # TODO: replace
    change_to = 'bit.ly/correct1102021'

    # change the bit.ly short URL to have a custom ending
    print('Changing', bitly_id, 'to', change_to, "short link", end="...")
    result = update_custom(headers, bitly_id, change_to)

    if result == HTTPStatus.OK:
        print('success!')
