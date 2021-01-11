from http import HTTPStatus
import sys
from typo_generator import make_typos
from url_shortener import validate_id, create_short_url


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

    :param key:
    :param bitly_link:
    :param redirect_url:
    :return:
    """
    # check if the original bit.ly ID is valid
    # TODO: fix double validation
    valid_link = validate_id(bitly_link)

    # maintain a list of successfully-generated bit.ly links
    success_list = []

    if valid_link:
        # create a list of bit.ly ID typos
        path = bitly_link.split('/')[1]
        typos = make_typos(path)
        bitly_typos = append_bitly_url(typos)

        # link the typo'd bit.ly IDs to a long URL
        for bitly_typo in bitly_typos:
            result = create_short_url(key, redirect_url, bitly_typo)

            # add successful domains to a list
            if result.status_code == HTTPStatus.OK:
                new_link = 'https://' + bitly_typo
                success_list.append(new_link)

    else:
        # the link is invalid
        # TODO: error handling
        pass

    # return the list of successfully-generated bit.ly links
    return success_list


if __name__ == '__main__':
    # check to see if the API key was supplied in program arguments, and exit if not
    if len(sys.argv) != 2:
        print('argument error: missing API key', file=sys.stderr)
        exit(1)
    api_key = sys.argv[1]

    # get the bit.ly ID and redirect URL from the user
    # TODO: get from user input
    bitlink = 'bit.ly/wyatttauber'
    redirect = 'https://wyatttauber.com'

    # create the links
    links = create_bitly_typos(api_key, bitlink, redirect)

    if len(links) != 0:
        # print the links if successful
        print('Successfully generated', len(links), 'bit.ly typos that redirect to', redirect, ':')
        for link in links:
            print(link)
        print('Complete.')
        exit(0)

    else:
        # tell the user to look for errors if unsuccessful
        print('fail: see errors above', file=sys.stderr)
        print('exit')
        exit(1)
