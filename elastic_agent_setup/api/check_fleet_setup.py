from ..core import Core, Settings


class CheckFleetSetup(Core):

    method = 'GET'
    endpoint = '/api/fleet/setup'
    host = Settings.kibana

    def parse_response(self, response):
        if response.json().get('isInitialized'):
            return True
        else:
            return False
