import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def is_valid_url(url):
    """
    Checks if a given URL is valid by its components
    :param url: URL string to be validated
    :return: True if the URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False

def follow_shortlink(shortlink_url):
    """
    Follows a shortlink URL to resolve the final destination (through redirects, if necessary)
    :param shortlink_url: The shortlink URL to resolve.
    :return: the final resolved URL
    """
    # check validity
    if not is_valid_url(shortlink_url):
        raise ValueError("Invalid shortlink URL", shortlink_url)
    try:
        # send the GET request
        response = requests.get(shortlink_url, allow_redirects=True, timeout=10)

        # get the URL of the destination
        final_url = response.url

        # check for meta-refresh in the HTML body
        soup = BeautifulSoup(response.text, 'html.parser')
        meta = soup.find("meta", attrs={"http-equiv": re.compile("^refresh$", re.I)})
        if meta:
            content = meta.get("content", "")
            match = re.search(r'url=([^;]+)', content, flags=re.IGNORECASE)
            if match:
                refresh_url = match.group(1).strip()
                # resolve relative URLs
                refresh_url = requests.compat.urljoin(final_url, refresh_url)

                # update the final URL to the redirect
                final_url = refresh_url

        # return the final URL
        return final_url

    except Exception as e:
        raise RuntimeError("webpage creation error: failed to follow shortlink", shortlink_url, ":", e)

