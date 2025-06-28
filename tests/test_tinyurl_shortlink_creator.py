import pytest

from tinyurl_shortlink_creator import *
from random import randint

tinyurl_api_key = keyring.get_password("system", "tinyurl")
headers = {
    'Authorization': 'Bearer {}'.format(tinyurl_api_key),
    'Content-Type': 'application/json',
}
short_url = None
prn = randint(100000, 999999)

@pytest.fixture
def var_create_link():
    response, short_url = create_link(headers, "https://example.com", tinyurl_api_key)

    return response, short_url

def test_create_link(var_create_link):
    assert var_create_link[0].status_code == HTTPStatus.OK
    assert var_create_link[1] is not None

def test_update_custom(var_create_link):
    old_short_url = urlparse(var_create_link[1])
    old_tinyurl_id = old_short_url.path.strip("/")
    response = update_custom(headers, old_tinyurl_id, "tinyurl.com/example" + str(prn), tinyurl_api_key)

    assert response.status_code == HTTPStatus.OK

def test_create_short_url():
    result = create_short_url(tinyurl_api_key, "https://example.com", "tinyurl.com/example" + str(prn))
    result_content = json.loads(result.content.decode('utf-8'))
    message = result_content.get('message')

    # will fail because already exists
    assert result.status_code == HTTPStatus.UNPROCESSABLE_ENTITY