from ..core import Core, Settings


class SetupFleetAgents(Core):

    method = 'POST'
    endpoint = '/api/fleet/agents/setup'
    host = Settings.kibana
    kwargs = {
        'json': {
            'forceRecreate': True
        }
    }

    def parse_response(self, response):
        print(response.json(), flush=True)
        return True
