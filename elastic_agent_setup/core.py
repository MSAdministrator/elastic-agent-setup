import abc
from urllib.parse import urljoin
import requests
from requests import Session
from requests.auth import HTTPBasicAuth
from .utils import LoggingBase
from .settings import Settings


class Core(metaclass=LoggingBase):

    HEADERS = {
        'kbn-xsrf': 'true',
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    method = "GET"
    endpoint = ""
    host = ""
    kwargs = {}

    def __init__(self, proxy=None, raise_for_status=True):
        self.session = Session()
        self.session.proxies = {
            "http": proxy,
            "https": proxy
        }
        self.raise_for_status = raise_for_status
        self.session.headers.update(self.HEADERS)
        self.session.verify = Settings.certificate_authority# or Settings().verify_ssl
        username, password = Settings.credentials
        self.session.auth = HTTPBasicAuth(username=username, password=password)

    def get_host(self):
        return self.host

    def get_method(self):
        return self.method

    def get_url(self):
        return urljoin(self.host, self.endpoint)

    def get_kwargs(self):
        return self.kwargs

    def run(self):
        try:
            self.__logger.info('Sending {} request to {}'.format(self.get_method(), self.get_url()))
            response = self.session.request(
                self.get_method(),
                self.get_url(),
                **self.get_kwargs()
            )
            return self.parse_response(response)
        except requests.exceptions.HTTPError as errh:
            return "An Http Error occurred:" + repr(errh)
        except requests.exceptions.ConnectionError as errc:
            return "An Error Connecting to the API occurred:" + repr(errc)
        except requests.exceptions.Timeout as errt:
            return "A Timeout Error occurred:" + repr(errt)
        except requests.exceptions.RequestException as err:
            return "An Unknown Error occurred" + repr(err)

    @abc.abstractmethod
    def parse_response(self):
        raise NotImplemented
