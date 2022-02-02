import os
import shutil
import subprocess
import json
import tarfile
import time
from requests import api
from requests.api import head
import yaml
import requests
from urllib.parse import urlparse, urljoin
from requests.auth import HTTPBasicAuth

import logging.config

from logging import FileHandler, DEBUG, INFO, ERROR, WARNING, CRITICAL
import logging


class DebugFileHandler(FileHandler):
    def __init__(self, filename, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record):
        if not record.levelno == DEBUG:
            return
        super().emit(record)

class LoggingBase(type):
    def __init__(cls, *args):
        super().__init__(*args)
        cls.setup_logging()

        # Explicit name mangling
        logger_attribute_name = '_' + cls.__name__ + '__logger'

        # Logger name derived accounting for inheritance for the bonus marks
        logger_name = '.'.join([c.__name__ for c in cls.mro()[-2::-1]])

        setattr(cls, logger_attribute_name, logging.getLogger(logger_name))
    
    def setup_logging(cls, default_path='./logging.yml', default_level=logging.INFO, env_key='LOG_CFG'):
        """Setup logging configuration

        """
        log_config = '''
---
version: 1
disable_existing_loggers: False
formatters:
    simple:
        format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

handlers:
    console:
        class: logging.StreamHandler
        level: DEBUG
        formatter: simple
        stream: ext://sys.stdout

    info_file_handler:
        class: logging.handlers.RotatingFileHandler
        level: INFO
        formatter: simple
        filename: info.log
        maxBytes: 10485760 # 10MB
        backupCount: 20
        encoding: utf8

    error_file_handler:
        class: logging.handlers.RotatingFileHandler
        level: ERROR
        formatter: simple
        filename: errors.log
        maxBytes: 10485760 # 10MB
        backupCount: 20
        encoding: utf8

    warning_file_handler:
        class: logging.handlers.RotatingFileHandler
        level: WARNING
        formatter: simple
        filename: warnings.log
        maxBytes: 10485760 # 10MB
        backupCount: 20
        encoding: utf8

loggers:
    my_module:
        level: INFO
        handlers: [console]
        propagate: no

root:
    level: INFO
    handlers: [console, info_file_handler, error_file_handler, warning_file_handler]
'''
        config = yaml.safe_load(log_config)
        logger = logging.config.dictConfig(config)


class ConfigureElasticAgent(metaclass=LoggingBase):

    HEADERS = {
        'kbn-xsrf': 'true',
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    enrollment_name = "elk-tls-docker-enrollment-token"

    def __init__(self):
        self.session = requests.Session()
        self.elastic_agent = '/elastic-agent-{}-linux-x86_64.tar.gz'.format(os.environ.get('ELK_VERSION'))
        self.username = os.environ.get('ELASTICSEARCH_USERNAME')
        self.password = os.environ.get('ELASTICSEARCH_PASSWORD')
        self.kibana_host = os.environ.get('KIBANA_HOST', 'https://localhost:5601')
        self.elasticsearch_host = os.environ.get('ELASTICSEARCH_HOSTS', 'https://localhost:9200')
        self.enroll_insecure = os.environ.get('FLEET_ENROLL_INSECURE')
        self.certificate_authorities = os.environ.get('FLEET_CA')
        self.fleet_enroll = os.environ.get('FLEET_ENROLL')
        self.enroll_force = os.environ.get('ENROLL_FORCE')
        self.setup_fleet_var = os.environ.get('FLEET_SETUP')
        self.auth = HTTPBasicAuth(self.username, self.password)

    def _request(self, url, method, data=None):
        self.__logger.info('Issuing {} request to {}'.format(method, url))
        verify = False if self.enroll_insecure else True
        if data:
            response = self.session.request(method=method, url=url, data=json.dumps(data), headers=self.HEADERS, auth=self.auth, verify=verify)
        else:
            response = self.session.request(method=method, url=url, headers=self.HEADERS, auth=self.auth, verify=verify)
        self.__logger.info('Successful {} request to {} with the following response: {}'.format(method, url, response))
        print(response, flush=True)
        return response.json()

    def check_if_fleet_is_setup(self):
        try:
            response = self._request(urljoin(self.kibana_host, '/api/fleet/setup'), 'GET')
            if response.get('isInitialized'):
                return True
            else:
                return False
        except:
            pass

    def setup_fleet(self):
        try:
            response = self._request(urljoin(self.kibana_host, '/api/fleet/setup'), 'POST')
            return True
        except:
            pass

    def check_if_fleet_agents_setup(self):
        try:
            response = self._request(urljoin(self.kibana_host, '/api/fleet/agents/setup'), 'GET')
            if response.get('isReady'):
                return True
            else:
                return False
        except:
            pass

    def setup_fleet_agents(self):
        try:
            response = self._request(urljoin(self.kibana_host, '/api/fleet/agents/setup'), 'POST', data={
                'forceRecreate': True
            })
            return True
        except:
            pass

    def check_service(self, service):
        if service == 'elasticsearch':
            url = urljoin(self.elasticsearch_host, '/_cluster/health?wait_for_status=yellow')
        elif service == 'kibana':
            url = urljoin(self.kibana_host, '/api/status')
        while True:
            try:
                self.__logger.info('Checking if {} is up and ready'.format(service))
                response = self._request(url, 'GET')
                self.__logger.debug('{} Response: {}'.format(service, response))
                return True
            except Exception as e:
                print('exception is: {}'.format(e), flush=True)
                time.sleep(10)
                pass

    def get_policy_id(self):
        policy_id = None
        while not policy_id:
            try:
                response = self._request(urljoin(self.kibana_host, '/api/fleet/agent_policies?page=1&perPage=100'), 'GET')
                policy_id = [item.get('id') for item in response.get('items') if item.get('is_default')][0]
            except:
                pass
        return policy_id

    def get_enrollment_api_keys(self):
        try:
            response = self._request(urljoin(self.kibana_host, '/api/fleet/enrollment-api-keys'), 'GET')
            return response
        except:
            pass

    def get_enrollment_api_key(self, api_key_id):
        try:
            return self._request(urljoin(self.kibana_host, '/api/fleet/enrollment-api-keys/{}'.format(api_key_id)), 'GET')
        except:
            pass

    def delete_enrollment_api_key(self, api_key_id):
        try:
            response = self._request(urljoin(self.kibana_host, '/api/fleet/enrollment-api-keys/{}'.format(api_key_id)), 'DELETE')
        except:
            pass

    def create_enrollment_api_key(self, policy_id):
        body = {
            "name": self.enrollment_name, 
            "policy_id": "{}".format(policy_id)
        }
        api_key = None
        while not api_key:
            try:
                response = self._request(urljoin(self.kibana_host, '/api/fleet/enrollment-api-keys'), 'POST', data=body)
                api_key = response.get('item').get('api_key')
            except:
                time.sleep(15)
                pass
        return api_key

    def __download_elastic_agent(self):
        self.__logger.info('Downloading elastic-agent')
        url = 'https://artifacts.elastic.co/downloads/beats/elastic-agent{}'.format(self.elastic_agent)
        r = requests.get(url, stream=True)
        with open(self.elastic_agent, 'wb') as f:
            for chunk in r.raw.stream(1024, decode_content=False):
                if chunk:
                    f.write(chunk)
        tar = tarfile.open(self.elastic_agent, "r:gz")
        tar.extractall()
        tar.close()
        self.__logger.info('Successfully downloaded elastic-agent')

    def install_elastic_agent(self, enrollment_key):
        self.__logger.info('Installing elastic-agent')
        commands = '''cd {dir} && ./elastic-agent install -f --kibana-url="{kibana}" --enrollment-token="{key}"'''.format(
            dir=self.elastic_agent.rsplit('.tar.gz',1)[0],
            kibana=self.kibana_host,
            key=enrollment_key,
            insecure='--insecure' if self.enroll_insecure else ''
        )
        process = subprocess.run(commands, shell=True, check=True, capture_output=True)
        self.__logger.info('Installation of elastic-agent response: {}'.format(process))

    def enroll_elastic_agent(self, enrollment_key):
        self.__logger.info('Enrolling elastic-agent')
        commands = '''cd /opt/Elastic/Agent && ./elastic-agent enroll --kibana-url="{kibana}" --enrollment-token="{key}" {insecure}'''.format(
            kibana='https://elastic:some_password@kibana:5601',#self.kibana_host,
            key=enrollment_key,
            insecure='--insecure' if self.enroll_insecure else ''
        )
        process = subprocess.run(commands, shell=True, check=True, capture_output=True)
        self.__logger.info('Enrollment of elastic-agent response: {}'.format(process))

    def run(self):
        self.__logger.info('Running....')
        policy_id = None
        api_key = None
        if self.check_service('kibana'):
            if self.check_service('elasticsearch'):
                if not self.check_if_fleet_is_setup():
                    self.setup_fleet()
                if not self.check_if_fleet_agents_setup():
                    self.setup_fleet_agents()
                for item in self.get_enrollment_api_keys().get('list'):
                    if item.get('name').startswith(self.enrollment_name):
                        if not policy_id and not api_key:
                            api_key = self.get_enrollment_api_key(item.get('id'))
                            policy_id = api_key.get('item').get('policy_id')
                            api_key = api_key.get('item').get('api_key')
                        else:
                            self.delete_enrollment_api_key(item.get('id'))
                if not policy_id and not api_key:
                    policy_id = self.get_policy_id()
                    api_key = self.create_enrollment_api_key(policy_id)
                if not os.path.exists(self.elastic_agent):
                    self.__download_elastic_agent()
                self.install_elastic_agent(api_key)


if __name__ == "__main__":
    if not os.path.exists('/usr/local/share/ca-certificates/ca.crt'):
        shutil.copy('/ca.crt', '/usr/local/share/ca-certificates/ca.crt')
        subprocess.run('update-ca-certificates')
    agent = ConfigureElasticAgent()
    agent.run()
    while True:
        print('Elastic Agent is running .....', flush=True)
        time.sleep(30)
