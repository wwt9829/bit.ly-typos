import sys

# adjacent key mappings for the missed key and inserted key functions
adjacencies = {
    'QWERTY': {
        'a': ['q', 'w', 's', 'x', 'z'],
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
        },
    'QWERTZ': {
        'a': ['q', 'w', 's', 'y', 'z'],
        'b': ['v', 'g', 'h', 'n'],
        'c': ['x', 'd', 'f', 'v'],
        'd': ['s', 'e', 'r', 'f', 'c', 'x'],
        'e': ['w', '3', '4', 'r', 'f', 'd', 's'],
        'f': ['d', 'r', 't', 'g', 'v', 'c'],
        'g': ['f', 't', 'z', 'h', 'b', 'v'],
        'h': ['g', 'z', 'u', 'j', 'n', 'b'],
        'i': ['u', '8', '9', 'o', 'l', 'k', 'j'],
        'j': ['h', 'u', 'i', 'k', 'm', 'n'],
        'k': ['j', 'i', 'o', 'l', 'm'],
        'l': ['k', 'o', 'p'],
        'm': ['n', 'j', 'k'],
        'n': ['b', 'h', 'j', 'm'],
        'o': ['i', '9', '0', 'p', 'l', 'k'],
        'p': ['o', '0', 'l'],
        'q': ['1', '2', 'w', 'a'],
        'r': ['e', '4', '5', 't', 'g', 'f', 'd'],
        's': ['a', 'w', 'e', 'd', 'x', 'y'],
        't': ['r', '5', '6', 'z', 'h', 'g', 'f'],
        'u': ['z', '7', '8', 'i', 'k', 'j', 'h'],
        'v': ['c', 'f', 'g', 'b'],
        'w': ['q', '2', '3', 'e', 'd', 's', 'a'],
        'x': ['y', 's', 'd', 'c'],
        'y': ['t', '6', '7', 'u', 'j', 'h', 'g'],
        'z': ['t', 'g', 'h', 'u', 'j'],
        '1': ['2', 'q'],
        '2': ['1', '3', 'w', 'q'],
        '3': ['2', '4', 'e', 'w'],
        '4': ['3', '5', 'r', 'e'],
        '5': ['4', '6', 't', 'r'],
        '6': ['5', '7', 'z', 't'],
        '7': ['6', '8', 'u', 'z'],
        '8': ['7', '9', 'i', 'u'],
        '9': ['8', '0', 'o', 'i'],
        '0': ['9', 'p', 'o'],
        },
    'AZERTY': {
        'a': ['z', 'q', 's'],
        'z': ['a', 'e', 's'],
        'e': ['z', 'r', 'd', '3', '4'],
        'r': ['e', 't', 'f', '4', '5'],
        't': ['r', 'y', 'g', '5', '6'],
        'y': ['t', 'u', 'h', '6', '7'],
        'u': ['y', 'i', 'j', '7', '8'],
        'i': ['u', 'o', 'k', '8', '9'],
        'o': ['i', 'p', 'l', '9', '0'],
        'p': ['o', 'm', '0'],
        'q': ['a', 's', 'w', '1', '2'],
        's': ['q', 'd', 'z', 'a', 'w', '2', '3'],
        'd': ['s', 'f', 'e', 'x', '3', '4'],
        'f': ['d', 'g', 'r', 'c', '4', '5'],
        'g': ['f', 'h', 't', 'v', '5', '6'],
        'h': ['g', 'j', 'y', 'b', '6', '7'],
        'j': ['h', 'k', 'u', 'n', '7', '8'],
        'k': ['j', 'l', 'i', '8', '9'],
        'l': ['k', 'm', 'o', '9', '0'],
        'm': ['l', 'p', '0'],
        'w': ['q', 'x', 's'],
        'x': ['w', 'd', 'c', 's'],
        'c': ['x', 'f', 'v'],
        'v': ['c', 'g', 'b'],
        'b': ['v', 'h', 'n'],
        'n': ['b', 'j', 'm'],
        '1': ['2', 'q'],
        '2': ['1', '3', 'w', 'q', 's'],
        '3': ['2', '4', 'e', 'w', 's', 'd'],
        '4': ['3', '5', 'r', 'e', 'd', 'f'],
        '5': ['4', '6', 't', 'r', 'f', 'g'],
        '6': ['5', '7', 'y', 't', 'g', 'h'],
        '7': ['6', '8', 'u', 'y', 'h', 'j'],
        '8': ['7', '9', 'i', 'u', 'j', 'k'],
        '9': ['8', '0', 'o', 'i', 'k', 'l'],
        '0': ['9', 'p', 'o', 'l', 'm'],
        }
}

# mappings for common confusable characters
confusables = {
    '0': ['O'],
    '1': ['I', 'l'],
    '2': ['Z'],
    '4': ['A'],
    '5': ['S'],
    '7': ['T'],
    '8': ['B'],
    'A': ['4'],
    'B': ['8'],
    'I': ['1', 'l'],
    'L': ['1', 'I'],
    'O': ['0'],
    'S': ['5'],
    'T': ['7'],
    'Z': ['2'],
    'l': ['1', 'I']
}

def skip_letter(keyword, list, debug):
    """
    Generates all keywords with a letter skipped
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    :param debug: a boolean indicating whether to preview the typos before generating them
    """
    skip_list = []

    i = 0
    while i < len(keyword):
        # skip a letter
        new_word = keyword[0:i] + keyword[i+1:]

        skip_list.append(new_word)
        i += 1

    if debug:
        print("Skip:", skip_list)
    list += skip_list

def double_letter(keyword, list, debug):
    """
    Generates all keywords with a letter duplicated
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    :param debug: a boolean indicating whether to preview the typos before generating them
    """
    double_list = []

    i = 0
    while i < len(keyword):
        # duplicate a letter
        new_word = keyword[0:i+1] + keyword[i] + keyword[i + 1:]

        double_list.append(new_word)
        i += 1

    if debug:
        print("Double:", double_list)
    list += double_list

def reverse_letters(keyword, list, debug):
    """
    Generates all keywords with a letter reversed
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    :param debug: a boolean indicating whether to preview the typos before generating them
    """
    reverse_list = []

    i = 0
    while i < len(keyword) - 1:
        # reverse a letter
        new_word = keyword[0:i] + keyword[i + 1] + keyword[i] + keyword[i + 2:]

        reverse_list.append(new_word)
        i += 1

    if debug:
        print("Reverse:", reverse_list)
    list += reverse_list

def miss_key(keyword, list, debug, layout):
    """
    Generate all keywords with a missed key (assume only one missed key per generated word)
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    :param debug: a boolean indicating whether to preview the typos before generating them
    :param layout: the keyboard layout to use for the missed keys generator
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

        while j < len(adjacencies[layout][character]):
            if capital:
                # if the letter is capital, make the mapping capital as well
                replacement_key = adjacencies[layout][character][j].upper()
            else:
                # if the letter is not capital, do not change the case of the letter
                replacement_key = adjacencies[layout][character][j]

            # miss a letter
            new_word = keyword[0:i] + replacement_key + keyword[i + 1:]

            j += 1
            miss_list.append(new_word)

        i += 1
        j = 0
        capital = False

    if debug:
        print("Miss (" + layout + "):", miss_list)
    list += miss_list

def change_case(keyword, list, debug):
    """
    Generate all keywords with a letter changed case
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    :param debug: a boolean indicating whether to preview the typos before generating them
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

    if debug:
        print("Case:", case_list)
    list += case_list

def change_confuse(keyword, list, debug):
    """
    Generate all keywords with confusable letters changed
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    :param debug: a boolean indicating whether to preview the typos before generating them
    """
    confuse_list = []

    i = 0
    j = 0

    while i < len(keyword):
        character = keyword[i]
        try:
            while j < len(confusables[character]):
                confuse_character = confusables[character][j]
                new_word = keyword[0:i] + confuse_character + keyword[i + 1:]
                confuse_list.append(new_word)
                j += 1
        except KeyError:
            pass
        j = 0
        i += 1

    if debug:
        print("conFuse:", confuse_list)
    list += confuse_list

def make_typos(string, options, debug, layout):
    """
    Apply the typo operations
    :param string: a string to generate typos with
    :param options: a dictionary of options selected by the user
    :param debug: a boolean indicating whether to preview the typos before generating them
    :param layout: the keyboard layout to use for the missed keys generator
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
        skip_letter(string, typo_list, debug)
    if options["double"]:
        double_letter(string, typo_list, debug)
    if options["reverse"]:
        reverse_letters(string, typo_list, debug)
    if options["miss"]:
        miss_key(string, typo_list, debug, layout)
    if options["case"]:
        change_case(string, typo_list, debug)
    if options["confuse"]:
        change_confuse(string, typo_list, debug)

    return typo_list


if __name__ == "__main__":
    # get a string to create typos for
    original_string = input("Enter a string to create typos:")

    # get a list of generated typos
    options = {'skip': True, 'double': False, 'reverse': False, 'miss': True, 'case': True, 'confuse': True}
    typos = make_typos(original_string, options, True, 'qwerty')

    # print the typo list
    for typo in typos:
        print(typo)
