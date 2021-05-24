from ..core import Core, Settings


class CheckService(Core):

    method = 'GET'
    endpoint = None

    def __init__(self, service):
        super().__init__()
        if service == 'elasticsearch':
            self.host = Settings.elasticsearch
            self.endpoint = '/_cluster/health?wait_for_status=yellow'
        elif service == 'kibana':
            self.host = Settings.kibana
            self.endpoint = '/api/status'

    def parse_response(self, response):
        return response.json()
