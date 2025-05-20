from http import HTTPStatus
import os
import sys
from typo_generator import make_typos
from bitly_url_shortener import create_short_url
import validators


def validate_id(bit_id):
    """
    Determines if a given bit.ly ID is properly formatted
    :param bit_id: the bit.ly ID to be evaluated
    :return: ID validity, as a boolean
    """
    # must have a /
    if '/' not in bit_id:
        return False

    # must have 'bit.ly' and and alpha-numeric code
    components = bit_id.split('/')
    if not components[0] == 'bit.ly':
        return False
    if not components[1].isalnum():
        return False

    # then it is a valid bit.ly ID
    return True


def validate(k, l, s):
    """
    Validate the api key, the long URL, and the bit.ly ID short link URL, exiting if invalid
    :param k: API key
    :param l: a URL
    :param s: a bit.ly ID
    """
    if not k.isalnum() or not k.islower() or not len(k) == 40:
        print('fail: invalid API key', file=sys.stderr)
        exit(1)
    if not validators.url(l):
        print('fail: invalid URL', file=sys.stderr)
        exit(1)
    if not validate_id(s):
        print('fail: invalid bit.ly ID', file=sys.stderr)
        exit(1)


def append_bitly_url(typo_list):
    """
    Create a list of bit.ly ID typos
    :param typo_list: a list of typos
    :return: a list of bit.ly ID typos
    """
    url_list = []

    for typo in typo_list:
        url = 'bit.ly/' + typo
        url_list.append(url)

    return url_list


def create_bitly_typos(key, bitly_link, redirect_url):
    """
    Create a list of typos for a bit.ly link and register them with a URL
    :param key: a bit.ly API key
    :param bitly_link: a bit.ly ID to generate typos for
    :param redirect_url: a URL to redirect the typo'd bit.ly IDs to
    :return: a list of successfully-created bit.ly hyperlinks
    """
    # validate the api key, the long URL, and the bit.ly ID short link URL
    validate(key, redirect_url, bitly_link)

    # maintain a list of successfully-generated bit.ly links
    success_list = []

    # create a list of bit.ly ID typos
    path = bitly_link.split('/')[1]
    typos = make_typos(path)
    bitly_typos = append_bitly_url(typos)

    # link the typo'd bit.ly IDs to a long URL
    print('Attempting to create', len(bitly_typos), 'bit.ly typos...')
    for bitly_typo in bitly_typos:
        print('Creating', bitly_typo)
        result = create_short_url(key, redirect_url, bitly_typo)

        # add successful domains to a list
        if result.status_code == HTTPStatus.OK:
            new_link = 'https://' + bitly_typo
            success_list.append(new_link)

    # return the list of successfully-generated bit.ly links
    return success_list


if __name__ == '__main__':
    # check to see if the API keys file exists
    if not os.path.isfile("api_keys.txt"):
        print('file error: missing api_keys.txt', file=sys.stderr)
        exit(1)

    # load the API keys
    bitly_api_key = ""

    with open("api_keys.txt", "r") as api_keys:
        for line in api_keys:
            if "bitly:" in line:
                try:
                    bitly_api_key = line.strip().split()[1]
                except IndexError:
                    print('file error: Bit.ly API key missing', file=sys.stderr)
                    exit(1)
            else:
                print('file error: no API keys identified', file=sys.stderr)
                exit(1)

    # get the bit.ly ID and redirect URL from the user
    shortlink = input('Enter a shortlink (bit.ly) to generate typos for:')
    redirect = input('Enter a URL to redirect the typos to:')

    # create the links
    links = []

    if "bit.ly" in shortlink:
        links = create_bitly_typos(bitly_api_key, shortlink, redirect)
    else:
        print('shortlink error: shortlink provided is not a supported shortlink', file=sys.stderr)
        exit(1)

    if len(links) != 0:
        # print the links if successful
        print('Successfully generated', len(links), 'bit.ly typos that redirect to', redirect, ':')
        for link in links:
            print(link)
        print('Complete. Exiting...')
        exit(0)

    else:
        # tell the user to look for errors if unsuccessful
        print('fail: see errors above', file=sys.stderr)
        print('Exiting...')
        exit(1)
