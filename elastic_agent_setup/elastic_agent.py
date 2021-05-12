from elastic_agent_setup.settings import Settings
from .preflight import Preflight
from .platform import Linux, MacOS, Windows

import logging
__LOGGER__ = logging.getLogger(__name__)


class ElasticAgent:

    def configure(self, 
        username, 
        password, 
        elasticsearch='https://elasticsearch:9200', 
        kibana='https://kibana:5601',
        certificate_authority=None,
        force_enroll=True,
        verify_ssl=True):
        Settings.credentials = (username, password)
        Settings.elasticsearch = elasticsearch
        Settings.kibana = kibana
        if certificate_authority:
            Settings.certificate_authority = certificate_authority
        Settings.verify_ssl = verify_ssl
        Settings.force_enroll = force_enroll

    def __platform_run(self, subcommand):
        if Settings.platform == 'Darwin':
            return MacOS().run(subcommand=subcommand)
        elif Settings.platform == 'Linux':
            return Linux().run(subcommand=subcommand)
        elif Settings.platform == 'Windows':
            return Windows().run(subcommand=subcommand)

    def install(self, version='7.12.1', enrollment_token=None, preflight_check=False):
        Settings.version = version
        if enrollment_token:
            Settings.enrollment_token = enrollment_token
        if preflight_check:
            response = Preflight().check()
            if response:
                if response.get('policy_id'):
                    Settings.policy_id = response['policy_id']
                if response.get('api_key'):
                    Settings.enrollment_token = response['api_key']
        return self.__platform_run('install')

    def enroll(self, version='7.12.1', enrollment_token=None, preflight_check=False):
        Settings.version = version
        if enrollment_token:
            Settings.enrollment_token = enrollment_token
        if preflight_check:
            response = Preflight().check()
            if response:
                if response.get('policy_id'):
                    Settings.policy_id = response['policy_id']
                if response.get('api_key'):
                    Settings.enrollment_token = response['api_key']
        return self.__platform_run('enroll')
