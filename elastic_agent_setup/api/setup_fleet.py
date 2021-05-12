from ..core import Core, Settings


class SetupFleet(Core):

    method = 'POST'
    endpoint = '/api/fleet/setup'
    host = Settings.kibana

    def parse_response(self, response):
        return True
