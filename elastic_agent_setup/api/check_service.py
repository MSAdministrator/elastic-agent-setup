from ..core import Core


class CheckService(Core):

    method = 'GET'
    endpoint = None

    def __init__(self, service):
        if service == 'elasticsearch':
            self.endpoint = '/_cluster/health?wait_for_status=yellow'
        elif service == 'kibana':
            self.endpoint = '/api/status'

    def parse_response(self, response):
        return response.json()
