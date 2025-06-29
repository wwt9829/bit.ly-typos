from shortlink_typo_generator import *
import pytest
from random import randint
from unittest.mock import patch

bitly_api_key = keyring.get_password("system", "bitly")
tinyurl_api_key = keyring.get_password("system", "tinyurl")
prn = randint(100000, 999999)

def test_validate_bitly_id():
    assert validate_bitly_id("bit.ly/example") is True
    assert validate_bitly_id("https://bit.ly/example") is True
    assert validate_bitly_id("bit.ly/example1") is True
    assert validate_bitly_id("bit.ly") is False
    assert validate_bitly_id("https://bit.ly/") is False
    assert validate_bitly_id("bit.ly/examp!e") is False

    assert validate_bitly_id("tinyurl.com/example") is False
    assert validate_bitly_id("https://tinyurl.com/example") is False
    assert validate_bitly_id("tinyurl.com/example1") is False
    assert validate_bitly_id("tinyurl.com") is False
    assert validate_bitly_id("https://tinyurl.com/") is False
    assert validate_bitly_id("tinyurl.com/examp!e") is False

    assert validate_bitly_id("https://example.com/") is False

def test_validate_tinyurl_id():
    assert validate_tinyurl_id("bit.ly/example") is False
    assert validate_tinyurl_id("https://bit.ly/example") is False
    assert validate_tinyurl_id("bit.ly/example1") is False
    assert validate_tinyurl_id("bit.ly") is False
    assert validate_tinyurl_id("https://bit.ly/") is False
    assert validate_tinyurl_id("bit.ly/examp!e") is False

    assert validate_tinyurl_id("tinyurl.com/example") is True
    assert validate_tinyurl_id("https://tinyurl.com/example") is True
    assert validate_tinyurl_id("tinyurl.com/example1") is True
    assert validate_tinyurl_id("tinyurl.com") is False
    assert validate_tinyurl_id("https://tinyurl.com/") is False
    assert validate_tinyurl_id("tinyurl.com/examp!e") is False

    assert validate_tinyurl_id("https://example.com/") is False

def test_validate_bitly():
    assert validate_bitly("notanapikey", "https://example.com/", "bit.ly/example") is False
    assert validate_bitly("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "https://example.com/", "bit.ly/example") is False
    assert validate_bitly("0000000000000000000000000000000000000000", "https://example.com/", "bit.ly/example") is False
    assert validate_bitly("Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0", "https://example.com/", "bit.ly/example") is False

    assert validate_bitly(bitly_api_key, "example.com", "bit.ly/example") is False # what scheme?
    assert validate_bitly(bitly_api_key, "https://example.notatld/", "bit.ly/example") is False

    assert validate_bitly(bitly_api_key, "https://example.com/", "bit.ly/example") is True
    assert validate_bitly(bitly_api_key, "https://example.com/", "tinyurl.com/example") is False
    assert validate_bitly(bitly_api_key, "https://example.com/", "example.com") is False

def test_validate_tinyurl():
    assert validate_tinyurl("notanapikey", "https://example.com/", "tinyurl.com/example") is False
    assert validate_tinyurl("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "https://example.com/", "tinyurl.com/example") is False
    assert validate_tinyurl("000000000000000000000000000000000000000000000000000000000000", "https://example.com/", "tinyurl.com/example") is False
    assert validate_tinyurl("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa0", "https://example.com/", "tinyurl.com/example") is False

    assert validate_tinyurl(tinyurl_api_key, "example.com", "tinyurl.com/example") is False # what scheme?
    assert validate_tinyurl(tinyurl_api_key, "https://example.notatld/", "tinyurl.com/example") is False

    assert validate_tinyurl(tinyurl_api_key, "https://example.com/", "tinyurl.com/example") is True
    assert validate_tinyurl(tinyurl_api_key, "https://example.com/", "bit.ly/example") is False
    assert validate_tinyurl(tinyurl_api_key, "https://example.com/", "example.com") is False

### PARSE ARGUMENTS TESTS (CLI)

def test_defaults_enabled_when_no_options():
    test_args = ["shortlink_typo_generator.py", "bit.ly/example", "https://example.com"]
    with patch.object(sys, 'argv', test_args):
        args = parse_arguments()
        assert args.shortlink == "bit.ly/example"
        assert args.redirect_url == "https://example.com"
        assert args.skip is True
        assert args.miss is True
        assert args.case is True
        assert args.confuse is True
        assert args.double is False
        assert args.reverse is False
        assert args.keyboard is None

def test_all_option_enables_everything():
    test_args = ["shortlink_typo_generator.py", "tinyurl.com/example", "https://example.com", "--all"]
    with patch.object(sys, 'argv', test_args):
        args = parse_arguments()
        assert args.skip is True
        assert args.double is True
        assert args.reverse is True
        assert args.miss is True
        assert args.case is True
        assert args.confuse is True
        assert args.keyboard == "QWERTY"  # default when --all is used

def test_keyboard_layout_is_parsed():
    test_args = ["shortlink_typo_generator.py", "bit.ly/example", "https://example.com", "-m", "--keyboard", "AZERTY"]
    with patch.object(sys, 'argv', test_args):
        args = parse_arguments()
        assert args.miss is True
        assert args.keyboard == "AZERTY"

def test_preview_and_bypass_mutually_exclusive():
    test_args = ["shortlink_typo_generator.py", "tinyurl.com/example", "https://example.com", "--preview", "--BYPASS"]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            parse_arguments()

def test_typo_flags_enabled_individually():
    test_args = ["shortlink_typo_generator.py", "bit.ly/example", "https://example.com", "-d", "-r"]
    with patch.object(sys, 'argv', test_args):
        args = parse_arguments()
        assert args.double is True
        assert args.reverse is True
        assert args.skip is False  # not default without --all or no flags
        assert args.miss is False
        assert args.case is False
        assert args.confuse is False

###

### SELECT OPTIONS TESTS (INTERACTIVE)

def test_select_defaults():
    with patch("builtins.input", side_effect=["", "", "y"]):
        preview, options, layout = select_options()
        assert preview is True
        assert options == {
            'skip': True, 'double': False, 'reverse': False,
            'miss': True, 'case': True, 'confuse': True
        }
        assert layout == "QWERTY"


def test_select_all_options():
    with patch("builtins.input", side_effect=["a", "", "y"]):
        preview, options, layout = select_options()
        assert preview is True
        assert options == {
            'skip': True, 'double': True, 'reverse': True,
            'miss': True, 'case': True, 'confuse': True
        }
        assert layout == "QWERTY"


def test_select_custom_options():
    with patch("builtins.input", side_effect=[
        "c",    # custom
        "y",    # skip
        "",     # double
        "y",    # reverse
        "y",    # miss
        "y",    # case
        "",     # confuse
        "AZERTY",   # layout
        "y"     # preview
    ]):
        preview, options, layout = select_options()
        assert preview is True
        assert options == {
            'skip': True, 'double': False, 'reverse': True,
            'miss': True, 'case': True, 'confuse': False
        }
        assert layout.upper() == "AZERTY"


def test_invalid_first_input_then_default(capsys):
    with patch("builtins.input", side_effect=["x", "", "", "y"]):
        preview, options, layout = select_options()

        captured = capsys.readouterr()
        assert "Invalid selection. Please try again." in captured.out

        assert preview is True
        assert options["skip"] is True
        assert layout == "QWERTY"


def test_invalid_keyboard_then_valid(capsys):
    with patch("builtins.input", side_effect=[
        "c",    # custom
        "",     # skip
        "",     # double
        "",     # reverse
        "y",    # miss
        "",     # case
        "",     # confuse
        "INVALID", "qwertz",  # retry layout
        "y"     # preview
    ]):
        preview, options, layout = select_options()

        captured = capsys.readouterr()
        assert "Invalid layout. Please try again." in captured.out

        assert options["miss"] is True
        assert layout.upper() == "QWERTZ"
        assert preview is True


def test_error_if_no_options_selected(capsys):
    with patch("builtins.input", side_effect=[
        "c",    # custom
        "", "", "", "", "", "", # all options skipped
        "",     # preview
    ]):
        preview, options, layout = select_options()

        assert options == {
            'skip': False, 'double': False, 'reverse': False,
            'miss': False, 'case': False, 'confuse': False
        }

###

def test_append_shortlink_domain():
    typo_list = ['xample', 'eample', 'exmple', 'exaple', 'examle', 'exampe', 'exampl'] # skip
    bitly_typo_list = ['bit.ly/xample', 'bit.ly/eample', 'bit.ly/exmple', 'bit.ly/exaple', 'bit.ly/examle', 'bit.ly/exampe', 'bit.ly/exampl']
    tinyurl_typo_list = ['tinyurl.com/xample', 'tinyurl.com/eample', 'tinyurl.com/exmple', 'tinyurl.com/exaple', 'tinyurl.com/examle', 'tinyurl.com/exampe', 'tinyurl.com/exampl']

    assert append_shortlink_domain(typo_list, 'bit.ly') == bitly_typo_list
    assert append_shortlink_domain(typo_list, 'tinyurl.com') == tinyurl_typo_list


def test_create_bitly_typos(capsys):
    options = {
        'skip': False, 'double': False, 'reverse': False,
        'miss': False, 'case': True, 'confuse': False
    }
    success_list = create_bitly_typos(bitly_api_key, "bit.ly/example" + str(prn), 'https://example.com/', options, True, True, 'QWERTY')

    captured = capsys.readouterr()

    assert 'Case: [' in captured.out
    assert 'Attempting to create 7 bit.ly typos...' in captured.out
    assert 'Example' + str(prn) in captured.out
    assert len(success_list) > 0

def test_create_tinyurl_typos(capsys):
    options = {
        'skip': False, 'double': False, 'reverse': False,
        'miss': True, 'case': False, 'confuse': False
    }
    success_list = create_tinyurl_typos(tinyurl_api_key, "tinyurl.com/example" + str(prn), 'https://example.com/', options, True, True, 'AZERTY')

    captured = capsys.readouterr()

    assert 'Miss (AZERTY): [' in captured.out
    assert 'Attempting to create 51 tinyurl.com typos...' in captured.out
    assert 'zxample' + str(prn) in captured.out
    assert len(success_list) > 0