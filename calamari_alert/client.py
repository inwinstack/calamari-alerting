import six
from calamari_alert.common import exceptions
from calamari_alert.common import logs
from requests.exceptions import ConnectionError
import requests

try:
    from lxml import etree
except ImportError as e:
    print("Missing required python module: " + str(e))
    exit()

try:
    import json
except ImportError:
    import simplejson as json

from api.v1 import UserMixin, ClusterMixin, SpaceMixin, HealthMixin


class HTTPClient(requests.Session,
                 UserMixin,
                 ClusterMixin,
                 SpaceMixin,
                 HealthMixin):

    def __init__(self, **params):
        """
        Initialize the class, get the necessary parameters
        """
        self.user_agent = 'python-calamari-alert'

        self.params = params
        self.log = logs.logger
        self.log.debug("PARAMS - {0}".format(str(self.params)))
        self.token = None
        self.ca_files = self.params['ca_files']
        self.ca_verify = (self.params['ca_verify'] == 'True')

        self.endpoint = self.params['endpoint']

        if 'timeout' not in self.params:
            self.timeout = None

        self.http = requests.Session()

    def _request(self, url, method, **kwargs):

        if self.timeout is not None:
            kwargs.setdefault('timeout', self.timeout)

        kwargs.setdefault('headers', kwargs.get('headers', {}))
        kwargs['headers']['User-Agent'] = self.user_agent

        if self.token is not None:
            kwargs['headers']['X-XSRF-TOKEN'] = self.token

        try:
            if kwargs['body'] is 'json':
                kwargs['headers']['Accept'] = 'application/json'
                kwargs['headers']['Content-Type'] = 'application/json'
            elif kwargs['body'] is 'xml':
                kwargs['headers']['Accept'] = 'application/xml'
                kwargs['headers']['Content-Type'] = 'application/xml'
            elif kwargs['body'] is 'text':
                kwargs['headers']['Accept'] = 'text/plain'
                kwargs['headers']['Content-Type'] = 'text/plain'
            elif kwargs['body'] is 'binary':
                kwargs['headers']['Accept'] = 'application/octet-stream'
                kwargs['headers']['Content-Type'] = 'application/octet-stream'
            else:
                raise exceptions.UnsupportedRequestType()
        except KeyError:
            # Default if body type is unspecified is text/plain
            kwargs['headers']['Accept'] = 'text/plain'
            kwargs['headers']['Content-Type'] = 'text/plain'

        # Optionally verify if requested body type is supported
        try:
            if kwargs['body'] not in kwargs['supported_body_types']:
                raise exceptions.UnsupportedBodyType()
            else:
                del kwargs['supported_body_types']
        except KeyError:
            pass

        del kwargs['body']

        resp = None

        try:
            resp = self.http.request(
                method,
                self.endpoint + url,
                verify=bool(self.ca_verify),
                cert=self.ca_files,
                **kwargs
            )
        except ConnectionError as error:
            self.log.error("{0} {1} - {2}"
                           .format(method, url, error.message))
        # else:
        #     self.log.debug("{0} {1}"
        #                    .format(method, url))

        body = None
        if resp is not None:
            if resp.text:
                try:
                    if kwargs['headers']['Content-Type'] is 'application/json':
                        body = json.loads(resp.text)
                    elif kwargs['headers']['Content-Type'] is 'application/xml':
                        body = etree.XML(resp.text)
                    else:
                        body = resp.text
                except ValueError:
                    body = None
            else:
                body = None

        return resp, body

    def _get(self, url, **kwargs):
        return self._request(url, 'GET', **kwargs)

    def _post(self, url, **kwargs):
        return self._request(url, 'POST', **kwargs)

    def _put(self, url, **kwargs):
        return self._request(url, 'PUT', **kwargs)

    def _delete(self, url, **kwargs):
        return self._request(url, 'DELETE', **kwargs)

    def _url(self, version, path_fmt, *args):
        for arg in args:
            if not isinstance(arg, six.string_types):
                raise ValueError(
                    'Expected a string but found {0} ({1}) '
                    'instead'.format(arg, type(arg))
                )

        args = map(six.moves.urllib.parse.quote_plus, args)

        version_str = 'v{0}/'.format(version)

        return '{0}{1}'.format(version_str, path_fmt.format(*args))

    def login(self, username, password):
        """
        Authenticate with the Django auth system as
        it is exposed in the Calamari REST API.
        """
        url = self._url(1, 'auth/login/')
        response, body = self._get(url, body='json')
        response.raise_for_status()
        self.token = response.cookies['XSRF-TOKEN']

        kwargs = {
            'body': 'json',
            "data": json.dumps({'username': username, 'password': password})
        }

        response, body = self._post(url, **kwargs)
        self.token = response.cookies['XSRF-TOKEN']
        if isinstance(body, dict):
            if 'message' in body:
                self.log.debug("LOGIN - {0}"
                               .format(body))
            else:
                body['message'] = 'Login success ...'
                self.log.debug("LOGIN - {0}"
                               .format(body))
        else:
            body['message'] = 'Unknow argument ...'
            self.log.debug("LOGIN - {0}"
                           .format(body))
