from urllib.parse import urlparse
import json
import requests
import sys

# TODO: comments
# TODO: make a headers class


def create_link(head, long_url):
    """
    Shortens a long URL into a bit.ly short link
    :param head: request headers (API key and content type)
    :param long_url: a properly-formatted URL (TODO: implement a check for this)
    :return: a properly-formatted bit.ly short link URL
    """
    p_data = {
        'long_url': long_url,
        'domain': 'bit.ly'
    }
    data = json.dumps(p_data)

    # TODO: try/except for json dump

    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=head, data=data)
    re_json = json.loads(response.content)
    try:
        short_url = re_json["link"]
        print(response)
        return short_url
    except KeyError:
        print("Error reading JSON")
        exit()

    # TODO: implement handling of 200/201 and error messages


def update_custom(head, old_link, new_link):
    """
    Changes the short link of a bit.ly URL
    :param head: request headers (API key and content type)
    :param old_link: a bitlink ID to change
    :param new_link: an unused bitlink ID
    :return: HTTP status code of request (TODO: add succes/fail messages instead)
    """
    data = {
        'custom_bitlink': new_link,
        'bitlink_id': old_link
    }
    data = json.dumps(data)

    # TODO: try/except for json dump

    response = requests.post('https://api-ssl.bitly.com/v4/custom_bitlinks', headers=head, data=data)
    return response

    # TODO: implement handling of 200 and error messages


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Argument error: missing API key")
        exit()

    token = sys.argv[1]
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'Content-Type': 'application/json',
    }

    url_to_shorten = 'https://example.net/'
    bitly_link = create_link(headers, url_to_shorten)
    parsed = urlparse(bitly_link)
    bitly_link = parsed.netloc + parsed.path
    print(bitly_link)

    change_to = 'bit.ly/correct1102021'
    http_response = update_custom(headers, bitly_link, change_to)
    print(http_response)
