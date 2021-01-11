from http import HTTPStatus
import sys
from typo_generator import make_typos
from url_shortener import create_short_url
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
    # check to see if the API key was supplied in program arguments, and exit if not
    if len(sys.argv) != 2:
        print('argument error: missing API key', file=sys.stderr)
        exit(1)
    api_key = sys.argv[1]

    # get the bit.ly ID and redirect URL from the user
    bitlink = input('Enter a bit.ly ID to generate typos for:')
    redirect = input('Enter a URL to redirect the typos to:')

    # create the links
    links = create_bitly_typos(api_key, bitlink, redirect)

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
