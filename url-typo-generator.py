from urllib.parse import urlparse


def skip_letter(keyword, list):
    """

    :param keyword:
    :param list:
    :return:
    """
    return list


def double_letter(keyword, list):
    """

    :param keyword:
    :param list:
    :return:
    """
    return list


def reverse_letters(keyword, list):
    """

    :param keyword:
    :param list:
    :return:
    """
    return list


def missed_key(keyword, list):
    """

    :param keyword:
    :param list:
    :return:
    """
    return list


def inserted_key(keyword, list):
    """

    :param keyword:
    :param list:
    :return:
    """
    return list


if __name__ == "__main__":
    original_bitly_link = input("Enter bit.ly short URL to create typos:")
    parsed_original_bitly_link = urlparse(original_bitly_link)

    path = parsed_original_bitly_link.path
    typo_list = []

    typo_list = skip_letter(path, typo_list)
    typo_list = double_letter(path, typo_list)
    typo_list = reverse_letters(path, typo_list)
    typo_list = missed_key(path, typo_list)
    typo_list = inserted_key(path, typo_list)

    print(typo_list)
