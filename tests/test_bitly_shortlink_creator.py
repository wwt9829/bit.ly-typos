import pytest
from random import randint
from bitly_shortlink_creator import *

bitly_api_key = keyring.get_password("system", "bitly")
headers = {
    'Authorization': 'Bearer {}'.format(bitly_api_key),
    'Content-Type': 'application/json',
}
short_url = None
prn = randint(100000, 999999)

@pytest.fixture
def var_create_link():
    response, short_url = create_link(headers, "https://example.com")

    return response, short_url

def test_create_link(var_create_link):
    assert var_create_link[0].status_code == HTTPStatus.OK
    assert var_create_link[1] is not None

def test_update_custom(var_create_link):
    old_short_url = urlparse(var_create_link[1])
    old_bitly_id = old_short_url.netloc + old_short_url.path
    response = update_custom(headers, old_bitly_id, "bit.ly/example" + str(prn))

    assert response.status_code == HTTPStatus.OK

def test_create_short_url():
    result = create_short_url(bitly_api_key, "https://example.com", "bit.ly/example" + str(prn))
    result_content = json.loads(result.content.decode('utf-8'))

    # will fail because already exists
    assert result.status_code == HTTPStatus.BAD_REQUEST