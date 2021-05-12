from ..core import Core, Settings


class CheckFleetAgentsSetup(Core):

    method = 'GET'
    endpoint = '/api/fleet/agents/setup'
    host = Settings.kibana

    def parse_response(self, response):
        if response.json().get('isInitialized'):
            return True
        else:
            return False
