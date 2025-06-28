from typo_list_generator import *

def test_skip_letter():
    skip_list = []
    skip_letter("example", skip_list, False)

    assert "xample" in skip_list
    assert "eample" in skip_list
    assert "exmple" in skip_list
    assert "exaple" in skip_list
    assert "examle" in skip_list
    assert "exampe" in skip_list
    assert "exampl" in skip_list

    # length
    assert len(skip_list) == 7

def test_double_letter():
    double_list = []
    double_letter("example", double_list, False)

    assert "eexample" in double_list
    assert "exxample" in double_list
    assert "exaample" in double_list
    assert "exammple" in double_list
    assert "exampple" in double_list
    assert "examplle" in double_list
    assert "examplee" in double_list

    # length
    assert len(double_list) == 7

def test_reverse_letters():
    reverse_list = []
    reverse_letters("example", reverse_list, False)

    assert "xeample" in reverse_list  # e <-> x
    assert "eaxmple" in reverse_list  # x <-> a
    assert "exmaple" in reverse_list  # a <-> m
    assert "exapmle" in reverse_list  # m <-> p
    assert "examlpe" in reverse_list  # p <-> l
    assert "exampel" in reverse_list  # l <-> e

    # length
    assert len(reverse_list) == 6

def test_miss_key_qwerty():
    miss_list_qwerty = []
    miss_key("example", miss_list_qwerty, False, "QWERTY")

    # starting 'e' -> ['w', '3', '4', 'r', 'f', 'd', 's']
    assert "wxample" in miss_list_qwerty
    assert "3xample" in miss_list_qwerty
    assert "4xample" in miss_list_qwerty
    assert "rxample" in miss_list_qwerty
    assert "fxample" in miss_list_qwerty
    assert "dxample" in miss_list_qwerty
    assert "sxample" in miss_list_qwerty

    # 'x' -> ['z', 's', 'd', 'c']
    assert "ezample" in miss_list_qwerty
    assert "esample" in miss_list_qwerty
    assert "edample" in miss_list_qwerty
    assert "ecample" in miss_list_qwerty

    # 'a' -> ['q', 'w', 's', 'x', 'z']
    assert "exqmple" in miss_list_qwerty
    assert "exwmple" in miss_list_qwerty
    assert "exsmple" in miss_list_qwerty
    assert "exxmple" in miss_list_qwerty
    assert "exzmple" in miss_list_qwerty

    # 'm' -> ['n', 'j', 'k']
    assert "exanple" in miss_list_qwerty
    assert "exajple" in miss_list_qwerty
    assert "exakple" in miss_list_qwerty

    # 'p' -> ['o', '0', 'l']
    assert "examole" in miss_list_qwerty
    assert "exam0le" in miss_list_qwerty
    assert "examlle" in miss_list_qwerty

    # 'l' -> ['k', 'o', 'p']
    assert "exampke" in miss_list_qwerty
    assert "exampoe" in miss_list_qwerty
    assert "examppe" in miss_list_qwerty

    # ending 'e' -> ['w', '3', '4', 'r', 'f', 'd', 's']
    assert "examplw" in miss_list_qwerty
    assert "exampl3" in miss_list_qwerty
    assert "exampl4" in miss_list_qwerty
    assert "examplr" in miss_list_qwerty
    assert "examplf" in miss_list_qwerty
    assert "exampld" in miss_list_qwerty
    assert "exampls" in miss_list_qwerty

    # length
    assert len(miss_list_qwerty) == 32

def test_miss_key_qwertz():
    miss_list_qwertz = []
    miss_key("amazingly", miss_list_qwertz, False, "QWERTZ")

    # 'z': ['t', 'g', 'h', 'u', 'j']
    assert "amatingly" in miss_list_qwertz
    assert "amagingly" in miss_list_qwertz
    assert "amahingly" in miss_list_qwertz
    assert "amauingly" in miss_list_qwertz
    assert "amajingly" in miss_list_qwertz

    # 'y': ['t', '6', '7', 'u', 'j', 'h', 'g']
    assert "amazinglt" in miss_list_qwertz
    assert "amazingl6" in miss_list_qwertz
    assert "amazingl7" in miss_list_qwertz
    assert "amazinglu" in miss_list_qwertz
    assert "amazinglj" in miss_list_qwertz
    assert "amazinglh" in miss_list_qwertz
    assert "amazinglg" in miss_list_qwertz

    # length
    assert len(miss_list_qwertz) == 45

def test_miss_key_azerty():
    miss_list_azerty = []
    miss_key("squeamishwaltz", miss_list_azerty, False, "AZERTY")

    # 's' -> ['q', 'd', 'z', 'a', 'w', '2', '3']
    assert "qqueamishwaltz" in miss_list_azerty
    assert "dqueamishwaltz" in miss_list_azerty
    assert "zqueamishwaltz" in miss_list_azerty
    assert "aqueamishwaltz" in miss_list_azerty
    assert "wqueamishwaltz" in miss_list_azerty
    assert "2queamishwaltz" in miss_list_azerty
    assert "3queamishwaltz" in miss_list_azerty

    # 'q' -> ['a', 's', 'w', '1', '2']
    assert "saueamishwaltz" in miss_list_azerty
    assert "ssueamishwaltz" in miss_list_azerty
    assert "swueamishwaltz" in miss_list_azerty
    assert "s1ueamishwaltz" in miss_list_azerty
    assert "s2ueamishwaltz" in miss_list_azerty

    # 'u' -> ['y', 'i', 'j', '7', '8']
    assert "sqyeamishwaltz" in miss_list_azerty
    assert "sqieamishwaltz" in miss_list_azerty
    assert "sqjeamishwaltz" in miss_list_azerty
    assert "sq7eamishwaltz" in miss_list_azerty
    assert "sq8eamishwaltz" in miss_list_azerty

    # 'a' -> ['z', 'q', 's']
    assert "squezmishwaltz" in miss_list_azerty
    assert "squeqmishwaltz" in miss_list_azerty
    assert "squesmishwaltz" in miss_list_azerty

    # 'm' -> ['l', 'p', '0']
    assert "squealishwaltz" in miss_list_azerty
    assert "squeapishwaltz" in miss_list_azerty
    assert "squea0ishwaltz" in miss_list_azerty

    # 'w' -> ['q', 'x', 's']
    assert "squeamishqaltz" in miss_list_azerty
    assert "squeamishxaltz" in miss_list_azerty
    assert "squeamishsaltz" in miss_list_azerty

    # 'z' -> ['a', 'e', 's']
    assert "squeamishwalta" in miss_list_azerty
    assert "squeamishwalte" in miss_list_azerty
    assert "squeamishwalts" in miss_list_azerty

    # length
    assert len(miss_list_azerty) == 65

def test_change_case():
    change_list = []
    change_case("example", change_list, False)

    assert "Example" in change_list
    assert "eXample" in change_list
    assert "exAmple" in change_list
    assert "exaMple" in change_list
    assert "examPle" in change_list
    assert "exampLe" in change_list
    assert "examplE" in change_list

    # length
    assert len(change_list) == 7

def test_change_confuse():
    confuse_list = []
    change_confuse("BOASTZILSA80", confuse_list, False)

    assert "8OASTZILSA80" in confuse_list
    assert "B0ASTZILSA80" in confuse_list
    assert "BO4STZILSA80" in confuse_list
    assert "BOA5TZILSA80" in confuse_list
    assert "BOAS7ZILSA80" in confuse_list
    assert "BOAST2ILSA80" in confuse_list
    assert "BOASTZ1LSA80" in confuse_list
    assert "BOASTZlLSA80" in confuse_list
    assert "BOASTZILS480" in confuse_list
    assert "BOASTZILS480" in confuse_list
    assert "BOASTZIL5A80" in confuse_list
    assert "BOASTZILS480" in confuse_list
    assert "BOASTZILSAB0" in confuse_list
    assert "BOASTZILSA8O" in confuse_list

    # length
    assert len(confuse_list) == 14

def test_make_typos():
    options = {"skip": True, "double": True, "reverse": True, "miss": True, "case": True, "confuse": True}
    typos = make_typos("example0", options, False, "QWERTY")

    assert "xample0" in typos
    assert "eexample0" in typos
    assert "examplE0" in typos
    assert "exampleO" in typos

    # length
    assert len(typos) == 68
