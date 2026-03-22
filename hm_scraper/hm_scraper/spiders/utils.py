from urllib.parse import urlencode
from ..settings import PROXY_KEY, PROXY_BASE_URL


def get_proxy_url(url):
    payload = {'api_key': PROXY_KEY, 'url': url}
    url_encoded_query_string_with_params = urlencode(payload)
    proxy_url = f'{PROXY_BASE_URL}{url_encoded_query_string_with_params}'
    return proxy_url


# scrapy list
# proxy_url = get_proxy_url('https://www2.hm.com/bg_bg/productpage.1274171042.html')
# proxy_url = get_proxy_url('https://www.chocolate.co.uk/collections/all')
# print(proxy_url)
