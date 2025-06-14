import argparse
from http import HTTPStatus
import os
import sys
from typo_list_generator import make_typos
import bitly_shortlink_creator
import tinyurl_shortlink_creator
import validators

def validate_api_file():
    """
    Check to see if the API keys file exists and is formatted properly
    :return: boolean indicating the existence of the file
    """
    # check to see if the API keys file exists
    if not os.path.isfile("api_keys.txt"):
        print('file error: missing api_keys.txt', file=sys.stderr)
        exit(1)

    # load the API keys
    api_keys = {}

    #bitly_api_key = ""
    #tinyurl_api_key = ""

    with open("api_keys.txt", "r") as api_keys_file:
        for line in api_keys_file:
            # bitly api key in the file
            if "bitly:" in line:
                try:
                    #bitly_api_key = line.strip().split()[1]
                    api_keys["bitly"] = line.strip().split()[1]
                    continue
                except IndexError:
                    print('file error: Bit.ly API key missing', file=sys.stderr)
                    exit(1)

            # tinyurl api key in the file
            if "tinyurl:" in line:
                try:
                    api_keys["tinyurl"] = line.strip().split()[1]
                    continue
                except IndexError:
                    print('file error: TinyUrl API key missing', file=sys.stderr)
                    exit(1)

            # something else in the file
            else:
                print('file error: no API keys identified', file=sys.stderr)
                exit(1)

    # return the api key
    #return bitly_api_key, tinyurl_api_key
    return api_keys


def validate_bitly_id(bit_id):
    """
    Determines if a given bit.ly ID is properly formatted
    :param bit_id: the bit.ly ID to be evaluated
    :return: ID validity, as a boolean
    """
    # must have a /
    if '/' not in bit_id:
        return False

    # must have 'bit.ly' and alpha-numeric code
    components = bit_id.split('/')
    if not components[0] == 'bit.ly':
        return False
    if not components[1].isalnum():
        return False

    # then it is a valid bit.ly ID
    return True


def validate_tinyurl_id(tiny_id):
    """
    Determines if a given TinyURL ID is properly formatted
    :param tiny_id: the TinyURL ID to be evaluated
    :return: ID validity, as a boolean
    """
    # must have a /
    if '/' not in tiny_id:
        return False

    # must have 'tinyurl.com' and alpha-numeric code
    components = tiny_id.split('/')
    if not components[0] == 'tinyurl.com':
        return False
    if not components[1].isalnum():
        return False

    # then it is a valid TinyURL ID
    return True


def validate_bitly(k, l, s):
    """
    Validate the api key, the long URL, and the bit.ly ID short link URL, exiting if invalid
    :param k: API key
    :param l: a URL
    :param s: a bit.ly ID
    """
    if not k.isalnum() or not k.islower() or not len(k) == 40:
        print('URL error: invalid API key', file=sys.stderr)
        exit(1)
    if not validators.url(l):
        print('URL error: invalid URL (include full path)', file=sys.stderr)
        exit(1)
    if not validate_bitly_id(s):
        print('shortlink error: invalid bit.ly ID', file=sys.stderr)
        exit(1)


def validate_tinyurl(k, l, s):
    """
    Validate the api key, the long URL, and the bit.ly ID short link URL, exiting if invalid
    :param k: API key
    :param l: a URL
    :param s: a bit.ly ID
    """
    if not k.isalnum() or not len(k) == 60:
        print('URL error: invalid API key', file=sys.stderr)
        exit(1)
    if not validators.url(l):
        print('URL error: invalid URL (include full path)', file=sys.stderr)
        exit(1)
    if not validate_tinyurl_id(s):
        print('shortlink error: invalid TinyURL ID', file=sys.stderr)
        exit(1)


def parse_arguments():
    """
    Parse and validate command line arguments
    :return: an ArgumentParser object with the command line arguments validated
    """
    parser = argparse.ArgumentParser()

    # required positional arguments
    parser.add_argument("shortlink", help="The original bit.ly link")
    parser.add_argument("redirect_url", help="The URL to redirect all typos to")

    # optional typo generation flags
    parser.add_argument("-s", "--skip", action="store_true",
                        help="skip each letter (e.g., bit.ly/example → bit.ly/xample) (default)")
    parser.add_argument("-d", "--double", action="store_true",
                        help="double each letter (e.g., bit.ly/example → bit.ly/eexample)")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="reverse each letter (e.g., bit.ly/example → bit.ly/xeample)")
    parser.add_argument("-m", "--miss", action="store_true",
                        help="mistype each key to an adjacent key (e.g., bit.ly/example → bit.ly/wxample) (default)")
    parser.add_argument("-c", "--case", action="store_true",
                        help="change case of each letter (e.g., bit.ly/example → bit.ly/Example) (default)")
    parser.add_argument("-A", "--all", action="store_true", help="generate all typos (not recommended on first run of a shortlink)")

    # optional output and interaction arguments
    parser.add_argument("-P", "--preview", action="store_true", help="preview the typos to be generated before generating them (good idea on first run of a shortlink)")
    parser.add_argument("-B", "--BYPASS", action="store_true",
                        help="bypass the API call confirmation prompt (not recommended on first run of a shortlink)")

    args = parser.parse_args()

    # don't allow preview and bypass at the same time as it's probably dumb
    if args.preview and args.BYPASS:
        print("args error: preview and bypass options are mutually exclusive as a precaution", file=sys.stderr)
        exit(1)

    if args.all:
        # apply all arguments if --all is passed
        args.skip = True
        args.double = True
        args.reverse = True
        args.miss = True
        args.case = True

        print("Running via cmd | ALL typo generation options enabled: skip double reverse miss case\n")

    elif not any([args.skip, args.double, args.reverse, args.miss, args.case]):
        # apply defaults if no options are explicitly passed
        args.skip = True
        args.miss = True
        args.case = True

        print("Running via cmd | Default typo generation options enabled:", end=" ")
        for opt in ["skip", "double", "reverse", "miss", "case"]:
            if getattr(args, opt):
                print(opt, end=" ")
        print("\n")

    else:
        # print options that are enabled
        print("Running via cmd | Typo generation options enabled:", end=" ")
        for opt in ["skip", "double", "reverse", "miss", "case"]:
            if getattr(args, opt):
                print(opt, end=" ")
        print("\n")

    return args


def select_options():
    """
    Select which typos to generate
    :return: a dictionary of options selected by the user
    """
    # options dictionary
    options = {'skip': True, 'double': False, 'reverse': False, 'miss': True, 'case': True}

    # explain the simple options to the user and perform selection
    print("Press ENTER to create the most common typos (default).")
    print("Press c to customize typo generation (-sdrmc).")
    print("Press a to create all possible typos (-A).")

    selection = input()
    while selection != "" and selection != "a" and selection != "c":
        print("Invalid selection. Please try again.")
        selection = input()
    if selection == "a":
        options = {'skip': True, 'double': True, 'reverse': True, 'miss': True, 'case': True}
    elif selection == "c":
        options = {'skip': False, 'double': False, 'reverse': False, 'miss': False, 'case': False}

        # explain the detailed options to the user and perform selection
        print("Select options for typo generation (y to confirm, any other key to skip):")
        print("! options are the default options, and therefore are strongly recommended.")
        print("Letter-based options:")
        if input("\t! Skip each letter (-s)? (ex: bit.ly/example → bit.ly/xample): ") == 'y':
            options['skip'] = True
        if input("\t* Double each letter (-d)? (ex: bit.ly/example → bit.ly/eexample): ") == 'y':
            options['double'] = True
        if input("\t* Reverse each letter (-r)? (ex: bit.ly/example → bit.ly/xeample): ") == 'y':
            options['reverse'] = True
        print("Key-based options:")
        if input("\t! Mistype each key to an adjacent key (-m)? (ex: bit.ly/example → bit.ly/wxample): ") == 'y':
            options['miss'] = True
        if input("\t! Change case of letter (-c)? (ex: bit.ly/example → bit.ly/Example): ") == 'y':
            options['case'] = True

        if options == {'skip': False, 'double': False, 'reverse': False, 'miss': False, 'case': False}:
            print("options error: no options selected", file=sys.stderr)
            exit(1)

    preview = False
    preview_input = input("Do you want to preview the typos to be generated before generating them (good idea on first run of a shortlink) (-P)? (y) ")
    if preview_input == "y":
        preview = True

    # return the selected options
    return preview, options


def append_shortlink_domain(typo_list, domain):
    """
    Create a list of bit.ly ID typos
    :param typo_list: a list of typos
    :param domain: a domain to append to the typos
    :return: a list of shortlink ID typos
    """
    url_list = []

    for typo in typo_list:
        url = domain + "/" + typo
        url_list.append(url)

    return url_list


def create_bitly_typos(key, bitly_link, redirect_url, options, debug, bypass):
    """
    Create a list of typos for a bit.ly link and register them with a URL
    :param key: a bit.ly API key
    :param bitly_link: a bit.ly ID to generate typos for
    :param redirect_url: a URL to redirect the typo'd bit.ly IDs to
    :param options: a dictionary of options selected by the user
    :param debug: a boolean indicating whether to preview the typos before generating them
    :param bypass: a boolean indicating whether to bypass the API call confirmation prompt
    :return: a list of successfully-created bit.ly hyperlinks
    """
    # validate the api key, the long URL, and the bit.ly ID short link URL
    validate_bitly(key, redirect_url, bitly_link)

    # maintain a list of successfully-generated bit.ly links
    success_list = []

    # create a list of bit.ly ID typos
    path = bitly_link.split('/')[1]
    typos = make_typos(path, options, debug)
    bitly_typos = append_shortlink_domain(typos, "bit.ly")

    # confirm the number of typos to generate with the user if not bypassed
    if not bypass:
        print("This will use", len(bitly_typos), "Bit.ly API calls. Press ENTER to confirm or any other key to exit... (-B to bypass this warning in cmd) ")
        if input() != "":
            exit(0)

    # link the typo'd bit.ly IDs to a long URL
    print('Attempting to create', len(bitly_typos), 'bit.ly typos...')
    print('NOTE: Bitly WILL NOT report an error if you re-register a shortlink you already own.')
    for bitly_typo in bitly_typos:
        print('Creating', bitly_typo)
        result = bitly_shortlink_creator.create_short_url(key, redirect_url, bitly_typo)

        # add successful domains to a list
        if result.status_code == HTTPStatus.OK:
            new_link = 'https://' + bitly_typo
            success_list.append(new_link)

    # return the list of successfully-generated bit.ly links
    return success_list


def create_tinyurl_typos(key, tinyurl_link, redirect_url, options, debug, bypass):
    """
    Create a list of typos for a tinyurl link and register them with a URL
    :param key: a tinyurl API key
    :param tinyurl_link: a tinyurl ID to generate typos for
    :param redirect_url: a URL to redirect the typo'd tinyurl IDs to
    :param options: a dictionary of options selected by the user
    :param debug: a boolean indicating whether to preview the typos before generating them
    :param bypass: a boolean indicating whether to bypass the API call confirmation prompt
    :return: a list of successfully-created tinyurl hyperlinks
    """
    # validate the api key, the long URL, and the TinyURL ID short link URL
    validate_tinyurl(key, redirect_url, tinyurl_link)

    # maintain a list of successfully-generated tinyurl links
    success_list = []

    # create a list of tinyurl ID typos
    path = tinyurl_link.split('/')[1]
    typos = make_typos(path, options, debug)
    tinyurl_typos = append_shortlink_domain(typos, "tinyurl.com")

    # confirm the number of typos to generate with the user if not bypassed
    if not bypass:
        print("This will use", len(tinyurl_typos), "TinyURL API calls. Press ENTER to confirm or any other key to exit... (-B to bypass this warning in cmd) ")
        if input() != "":
            exit(0)

    # link the typo'd bit.ly IDs to a long URL
    print('Attempting to create', len(tinyurl_typos), 'TinyURL typos...')
    print('NOTE: TinyURL WILL report an error if you re-register a shortlink you already own.')
    for tinyurl_typo in tinyurl_typos:
        print('Creating', tinyurl_typo)
        result = tinyurl_shortlink_creator.create_short_url(key, redirect_url, tinyurl_typo)  # TODO

        # add successful domains to a list  # TODO
        if result.status_code == HTTPStatus.OK:
            new_link = 'https://' + tinyurl_typo
            success_list.append(new_link)

    # return the list of successfully-generated TinyURL links
    return success_list


if __name__ == '__main__':
    # print the welcome message
    print("############################")
    print("# SHORTLINK TYPO GENERATOR #")
    print("############################")
    print("Generate and register common typos for your shortlinks! | by Wyatt Tauber (wyatttauber.com)")

    # read the API keys
    #bitly_api_key, tinyurl_api_key = validate_api_file()
    api_keys = validate_api_file()

    # initialize values to be assigned
    shortlink = ""
    redirect = ""
    options = {}
    bypass = False
    debug = False

    if len(sys.argv) > 1:
        args = parse_arguments()

        # assign values
        shortlink = args.shortlink
        redirect = args.redirect_url
        options = {'skip': args.skip, 'double': args.double, 'reverse': args.reverse, 'miss': args.miss, 'case': args.case}
        bypass = args.BYPASS
        debug = args.preview

    else:
        # show command line usage
        print("cmd usage: shortlink_typo_generator.py [-h --help] [-s --skip] [-d --double] [-r --reverse] [-m --miss] [-c --case] [-A --all] [-P --preview] [-B --bypass (cmd only)] shortlink redirect_url\n")

        # get the shortlink ID and redirect URL from the user
        shortlink = input('Enter a shortlink (bit.ly or tinyurl.com) to generate typos for: ').strip()
        redirect = input('Enter a URL to redirect the typos to: ').strip()
        print()

        # select which typos to generate
        debug, options = select_options()

    # create the links
    links = []

    if "bit.ly/" in shortlink:
        links = create_bitly_typos(api_keys["bitly"], shortlink, redirect, options, debug, bypass)
    elif "tinyurl.com/" in shortlink:
        links = create_tinyurl_typos(api_keys["tinyurl"], shortlink, redirect, options, debug, bypass)
    else:
        print('shortlink error: shortlink provided is not a supported shortlink', file=sys.stderr)
        exit(1)

    if len(links) != 0:
        # print the links if successful
        print('Generated', len(links), 'bit.ly typos that redirect to', redirect, ':')
        for link in links:
            print(link)
        exit(0)

    else:
        # tell the user to look for errors if unsuccessful
        print('fail: see errors above', file=sys.stderr)
        exit(1)
