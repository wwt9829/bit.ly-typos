from urllib.parse import urlparse

# TODO: comments


def skip_letter(keyword, list):
    """
    Generates all keywords with a letter skipped
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    """
    i = 0
    while i < len(keyword):
        new_word = keyword[0:i] + keyword[i+1:]
        list.append(new_word)
        i += 1


def double_letter(keyword, list):
    """
    Generates all keywords with a letter duplicated
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    """
    i = 0
    while i < len(keyword):
        new_word = keyword[0:i+1] + keyword[i] + keyword[i + 1:]
        list.append(new_word)
        i += 1


def reverse_letters(keyword, list):
    """
    Generates all keywords with a letter reversed
    :param keyword: a keyword to generate typos for
    :param list: the list of typos to append to
    """
    i = 0
    while i < len(keyword) - 1:
        new_word = keyword[0:i] + keyword[i + 1] + keyword[i] + keyword[i + 2:]
        list.append(new_word)
        i += 1


def missed_key(keyword, list):
    """

    :param keyword:
    :param list:
    """


def inserted_key(keyword, list):
    """

    :param keyword:
    :param list:
    """
    return list


if __name__ == "__main__":
    #original_bitly_link = input("Enter bit.ly short URL to create typos:")

    #path = original_bitly_link.split("/")[-1]
    path = 'test123'
    typo_list = []

    skip_letter(path, typo_list)
    double_letter(path, typo_list)
    reverse_letters(path, typo_list)
    #typo_list = missed_key(path, typo_list)
    #typo_list = inserted_key(path, typo_list)

    for typo in typo_list:
        print(typo)
