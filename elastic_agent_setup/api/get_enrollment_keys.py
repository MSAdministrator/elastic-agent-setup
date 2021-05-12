from ..core import Core, Settings


class GetEnrollmentKeys(Core):

    method = 'GET'
    endpoint = '/api/fleet/enrollment-api-keys'
    host = Settings.kibana

    def parse_response(self, response):
        return response.json()
