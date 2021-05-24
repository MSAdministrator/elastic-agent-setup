from ..core import Core, Settings


class DeleteEnrollmentKey(Core):

    method = 'DELETE'
    endpoint = '/api/fleet/enrollment-api-keys/{api_key_id}'
    host = Settings.kibana

    def __init__(self, api_key_id):
        super().__init__()
        self.endpoint = self.endpoint.format(api_key_id=api_key_id)

    def parse_response(self, response):
        return True

