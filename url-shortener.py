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
    Changes the ending of a bit.ly ID
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


def create_short_url(api_key, long, short):
    """
    Create a bit.ly ID given a long URL
    :param api_key: the bit.ly API key for the user
    :param long: a properly-formatted long URL
    :param short: a properly-formatted bit.ly ID
    :return: status code of the result
    """
    # insert the api key into the request headers
    headers = {
        'Authorization': 'Bearer {}'.format(api_key),
        'Content-Type': 'application/json',
    }

    # create a bit.ly ID from a long URL
    result, bitly_link = create_link(headers, long)

    # return the status code of the result if unsuccessful
    # TODO: better method of differentiating between fail types
    if (result != HTTPStatus.OK) and (result != HTTPStatus.CREATED):
        return result

    # parse the HTTP link to a bit.ly ID
    parsed_bitly_link = urlparse(bitly_link)
    bitly_id = parsed_bitly_link.netloc + parsed_bitly_link.path

    # change the bit.ly ID to have a custom ending
    result = update_custom(headers, bitly_id, short)

    # TODO: better method of differentiating between fail types
    # return the status code of the result
    return result


if __name__ == "__main__":
    # check to see if the API key was supplied in program arguments
    if len(sys.argv) != 2:
        print("Argument error: missing API key")
        exit()
    # TODO: validation of api key
    api_key = sys.argv[1]

    # the URL to shorten
    # TODO: URL checking
    url_to_shorten = input("Enter a properly-formatted URL to shorten:")

    # the custom bit.ly ID to use
    # TODO: URL checking
    change_to = input("Enter a new properly formatted bit.ly ID to shorten to:")

    # shorten the URL
    print('Shortening', url_to_shorten, 'to', 'https://'+change_to, 'bit.ly link', end="...")
    result = create_short_url(api_key, url_to_shorten, change_to)

    # print the result
    if result == HTTPStatus.OK:
        print("done!")
    else:
        print("error:", result)
