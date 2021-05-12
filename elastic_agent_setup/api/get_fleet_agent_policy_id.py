from ..core import Core, Settings


class GetFleetAgentPolicyId(Core):

    method = 'GET'
    endpoint = '/api/fleet/agent_policies?page=1&perPage=100'
    host = Settings.kibana

    def parse_response(self, response):
        return [item.get('id') for item in response.json().get('items') if item.get('is_default')][0]
