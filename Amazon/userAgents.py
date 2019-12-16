import requests
from lxml.html import fromstring


def Get_Headers():
    url = 'https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome'
    response = requests.get(url)
    parser = fromstring(response.text)
    Headers = parser.xpath('//tbody//td[2]/span/text()')[0]
    return Headers

