import os
import platform
from urllib.parse import urlparse, urlunparse
from .utils.exceptions import IncorrectPath
import struct


class SettingsProperties(type):

    def __uri_validator(self, uri):
        try:
            url = urlparse(uri)
            if url.scheme and url.netloc:
                return urlunparse(url._replace(path=''))
        except:
            raise Exception('Unable to validate the provider URI: {}'.format(uri))

    @property
    def elasticsearch(cls):
        return cls._elasticsearch

    @elasticsearch.setter
    def elasticsearch(cls, value):
        cls._elasticsearch = cls.__uri_validator(value)

    @property
    def kibana(cls):
        return cls._kibana

    @kibana.setter
    def kibana(cls, value):
        cls._kibana = cls.__uri_validator(value)

    @property
    def credentials(cls):
        return cls._credentials

    @credentials.setter
    def credentials(cls, value):
        if isinstance(value, tuple):
            cls._credentials = value
        else:
            raise AttributeError('Please provide both a username and password')

    @property
    def platform(cls):
        return platform.system()

    @property
    def version(cls):
        return cls._version

    @version.setter
    def version(cls, value):
        major, minor, patch = value.split('.')
        version = (major, minor, patch)
        cls._version = ".".join(map(str, version))

    @property
    def download_endpoint(self):
        bitness = struct.calcsize("P") * 8
        if hasattr(self, 'platform'):
            endpoint = self.VERSION_MAP[self.platform.lower()][str(bitness)]
            return endpoint.format(version=self.version)

    @property
    def download_path(cls):
        return os.path.join('/', cls.download_endpoint)

    @property
    def certificate_authority(cls):
        return cls._certificate_authority

    @certificate_authority.setter
    def certificate_authority(cls, value):
        if os.path.exists(os.path.abspath(os.path.expanduser(os.path.expandvars(value)))):
            cls._certificate_authority = os.path.abspath(os.path.expanduser(os.path.expandvars(value)))
        else:
            raise IncorrectPath('Path does not exist!')

    @property
    def verify_ssl(cls):
        return cls._verify_ssl

    @verify_ssl.setter
    def verify_ssl(cls, value):
        cls._verify_ssl = bool(value)
    
    @property
    def policy_id(cls):
        return cls._policy_id

    @policy_id.setter
    def policy_id(cls, value):
        cls._policy_id = value

    @property
    def force_enroll(cls):
        return cls._force_enroll

    @force_enroll.setter
    def force_enroll(cls, value):
        cls._force_enroll = value

    @property
    def enrollment_token(cls):
        return cls._enrollment_token

    @enrollment_token.setter
    def enrollment_token(cls, value):
        cls._enrollment_token = value


class Settings(object, metaclass=SettingsProperties):
    _elasticsearch = "https://elasticsearch:9200"
    _kibana = "https://kibana:5601"
    _credentials = None
    _platform = platform.system()
    _version = None
    _download_endpoint = None
    _certificate_authority = None
    _verify_ssl = True
    _policy_id = None
    _force_enroll = True
    _enrollment_token = None
    enrollment_name = "elk-tls-docker-enrollment-token"
    VERSION_MAP = {
        'darwin': {
            '64': 'elastic-agent-{version}-darwin-x86_64.tar.gz'
        },
        'deb': {
            '64': 'elastic-agent-{version}-amd64.deb',
            '32': 'elastic-agent-{version}-i386.deb'
        },
        'rpm': {
            '64': 'elastic-agent-{version}-x86_64.rpm',
            '32': 'elastic-agent-{version}-i686.rpm'
        },
        'windows': {
            '64': 'elastic-agent-{version}-windows-x86_64.zip',
            '32': 'elastic-agent-{version}-windows-x86.zip'
        },
        'linux': {
            '64': 'elastic-agent-{version}-linux-x86_64.tar.gz',
            '32': 'elastic-agent-{version}-linux-x86.tar.gz'
        }
    }
    agent_command_string= 'cd {dir} && ./elastic-agent {subcommand} {force} --kibana-url="{kibana}" --enrollment-token="{token}" {certificate_authorities} {insecure}'
