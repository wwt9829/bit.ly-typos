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


def get_site_title(url):
    """
    Fetch the title of a web page from a given URL.
    :param url: the URL of the web page to fetch the title from
    :return: the title of the web page (or the input URL if the title is not found)
    """
    try:
        # send the GET request
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        # parse the response
        soup = BeautifulSoup(response.text, 'html.parser')

        if soup.title and soup.title.string:
            # return the title
            return soup.title.string.strip()
        else:
            # return the URL if no title is found
            return url

    except Exception as e:
        raise RuntimeError("Failed to fetch site title from", url, ":", e)


def sanitize_filename(title):
    """
    Replace invalid characters with an underscore
    :param title: the input filename to be sanitized
    :return: a sanitized string without invalid characters
    """
    return re.sub(r'[\\/*?:"<>|]', '_', title)


def replace_placeholders(html, replacements):
    """
    Replace placeholders in an HTML string with corresponding values from a
    dictionary of replacements
    :param html: the HTML string containing placeholders to be replaced.
    :param replacements: dict[str, str]
        a dictionary containing mappings of placeholder strings to their
        replacement values.
    :return: the HTML string with the placeholders replaced
    """
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)
    return html


def process_html_with_shortlink(html, shortlink_url):
    """
    Replace placeholders in an html template with information derived
    from a shortlink URL.
    :param html: the HTML template containing placeholders to be replaced
    :param shortlink_url: a valid shortlink URL to be resolved and analyzed
    :return: the updated HTML with placeholders replaced based on the shortlink
    """
    # validate the shortlink URL
    if not is_valid_url(shortlink_url):
        raise ValueError("Invalid shortlink URL:", shortlink_url)

    # resolve the shortlink URL to the final destination and get the site title
    redirection_url = follow_shortlink(shortlink_url)
    site_title = get_site_title(redirection_url)

    # determine replacement variable values for the HTML template
    replacements = {
        "shortlink_link": urlparse(shortlink_url).netloc + urlparse(shortlink_url).path,
        "shortlink_url": shortlink_url,
        "redirection_url": redirection_url,
        "redirection_title": site_title.split("|")[0].strip()
    }

    # update the HTML template and the filename with the replacements
    updated_html = replace_placeholders(html, replacements)
    filename = sanitize_filename(site_title).split("_")[0].strip() + ".html"

    # save the new HTML to the file
    with open("web/" + filename, "w", encoding="utf-8") as f:
        f.write(updated_html)

    # print success (errors will be printed above if applicable)
    print("HTML saved as:", filename)


if __name__ == "__main__":
    # read the HTML template from the file
    with open("web/index.html", "r", encoding="utf-8") as f:
        html_template = f.read()

    # replace placeholders in the HTML template with information derived from the shortlink URL
    process_html_with_shortlink(html_template, "https://tinyurl.com/csc842example")