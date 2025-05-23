import sys

# adjacent key mappings for the missed key and inserted key functions
key_list = {'a': ['q', 'w', 's', 'x', 'z'],
            'b': ['v', 'g', 'h', 'n'],
            'c': ['x', 'd', 'f', 'v'],
            'd': ['s', 'e', 'r', 'f', 'c', 'x'],
            'e': ['w', '3', '4', 'r', 'f', 'd', 's'],
            'f': ['d', 'r', 't', 'g', 'v', 'c'],
            'g': ['f', 't', 'y', 'h', 'b', 'v'],
            'h': ['g', 'y', 'u', 'j', 'n', 'b'],
            'i': ['u', '8', '9', 'o', 'l', 'k', 'j'],
            'j': ['h', 'u', 'i', 'k', 'm', 'n'],
            'k': ['j', 'i', 'o', 'l', 'm'],
            'l': ['k', 'o', 'p'],
            'm': ['n', 'j', 'k'],
            'n': ['b', 'h', 'j', 'm'],
            'o': ['i', '9', '0', 'p', 'l', 'k'],
            'p': ['o', '0', 'l'],
            'q': ['1', '2', 'w', 's', 'a'],
            'r': ['e', '4', '5', 't', 'g', 'f', 'd'],
            's': ['a', 'w', 'e', 'd', 'x', 'z'],
            't': ['r', '5', '6', 'y', 'h', 'g', 'f'],
            'u': ['y', '7', '8', 'i', 'k', 'j', 'h'],
            'v': ['c', 'f', 'g', 'b'],
            'w': ['q', '2', '3', 'e', 'd', 's', 'a'],
            'x': ['z', 's', 'd', 'c'],
            'y': ['t', '6', '7', 'u', 'j', 'h', 'g'],
            'z': ['a', 's', 'x'],
            '1': ['2', 'q'],
            '2': ['1', '3', 'w', 'q'],
            '3': ['2', '4', 'e', 'w'],
            '4': ['3', '5', 'r', 'e'],
            '5': ['4', '6', 't', 'r'],
            '6': ['5', '7', 'y', 't'],
            '7': ['6', '8', 'u', 'y'],
            '8': ['7', '9', 'i', 'u'],
            '9': ['8', '0', 'o', 'i'],
            '0': ['9', 'p', 'o'],
            }


def skip_letter(keyword, list):
    """
    Generates all keywords with a letter skipped
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    """
    skip_list = []

    i = 0
    while i < len(keyword):
        # skip a letter
        new_word = keyword[0:i] + keyword[i+1:]

        skip_list.append(new_word)
        i += 1

    print("Skip:", skip_list)
    list += skip_list

def double_letter(keyword, list):
    """
    Generates all keywords with a letter duplicated
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    """
    double_list = []

    i = 0
    while i < len(keyword):
        # duplicate a letter
        new_word = keyword[0:i+1] + keyword[i] + keyword[i + 1:]

        double_list.append(new_word)
        i += 1

    print("Double:", double_list)
    list += double_list

def reverse_letters(keyword, list):
    """
    Generates all keywords with a letter reversed
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    """
    reverse_list = []

    i = 0
    while i < len(keyword) - 1:
        # reverse a letter
        new_word = keyword[0:i] + keyword[i + 1] + keyword[i] + keyword[i + 2:]

        reverse_list.append(new_word)
        i += 1

    print("Reverse:", reverse_list)
    list += reverse_list

def miss_key(keyword, list):
    """
    Generate all keywords with a missed key (assume only one missed key per generated word)
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    """
    miss_list = []

    i = 0
    j = 0
    capital = False

    while i < len(keyword):
        # capital letter detection
        if keyword[i].isupper():
            character = keyword[i].lower()
            capital = True
        else:
            character = keyword[i]

        while j < len(key_list[character]):
            if capital:
                # if the letter is capital, make the mapping capital as well
                replacement_key = key_list[character][j].upper()
            else:
                # if the letter is not capital, do not change the case of the letter
                replacement_key = key_list[character][j]

            # miss a letter
            new_word = keyword[0:i] + replacement_key + keyword[i + 1:]

            j += 1
            miss_list.append(new_word)

        i += 1
        j = 0
        capital = False

    print("Miss:", miss_list)
    list += miss_list

def change_case(keyword, list):
    """
    Generate all keywords with a letter changed case
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    """
    case_list = []

    i = 0
    while i < len(keyword):
        new_word = ""

        if keyword[i].isupper():
            # make uppercase lowercase
            new_word = keyword[0:i] + keyword[i].lower() + keyword[i + 1:]
        elif keyword[i].islower():
            # make lowercase uppercase
            new_word = keyword[0:i] + keyword[i].upper() + keyword[i + 1:]

        if new_word != "":
            case_list.append(new_word)

        i += 1

    print("Case:", case_list)
    list += case_list

def make_typos(string, options):
    """
    Apply the typo operations
    :param string: a string to generate typos with
    :param options: a dictionary of options for which typos to generate
    """
    # check if the string is alphanumeric, exiting if not
    for character in string:
        if not character.isalnum():
            print("fail: string contains non-alphanumeric characters", file=sys.stderr)
            exit(1)

    # the list to append typos to
    typo_list = []

    # create the necessary typos
    if options["skip"]:
        skip_letter(string, typo_list)
    if options["double"]:
        double_letter(string, typo_list)
    if options["reverse"]:
        reverse_letters(string, typo_list)
    if options["miss"]:
        miss_key(string, typo_list)
    if options["case"]:
        change_case(string, typo_list)

    return typo_list


if __name__ == "__main__":
    # get a string to create typos for
    original_string = input("Enter a string to create typos:")

    # get a list of generated typos
    typos = make_typos(original_string)

    # print the typo list
    for typo in typos:
        print(typo)
