from bs4 import BeautifulSoup as Soup

from service import router


def prepare_html(content):
    html = Soup(content, "lxml")
    for a in html.find_all("a", href=True):
        a['href'] = a['href'].replace(router.API_HOST.lower(), "")
    return html
