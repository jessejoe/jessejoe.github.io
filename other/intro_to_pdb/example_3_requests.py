import logging
from pprint import pformat
from requests import session, Request

logging.basicConfig(level=logging.DEBUG)


class MySession():

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = session()
        self.send_request(
            'GET', '/basic-auth/user/passwd', auth=('user', 'passwd'))

    def send_request(self, method, endpoint, **kwargs):
        url = self.base_url + endpoint
        req = Request(method, url, **kwargs)
        prepped = self.session.prepare_request(req)
        resp = self.session.send(prepped)
        resp.raise_for_status()
        logging.info('JSON response:\n%s', pformat(resp.json()))


api = MySession('https://httpbin.org')
api.send_request('GET', '/cookies/set', params={'foo': 'bar'})
#api.send_request('POST', '/post', data={'baz': 'qux'})
#api.send_request('POST', '/post', json={'baz': 'qux'})
