from ..core import Core, Settings


class CreateEnrollmentKey(Core):

    method = 'POST'
    endpoint = '/api/fleet/enrollment-api-keys'
    host = Settings.kibana
    kwargs = {
        'json': {
            "name": Settings.enrollment_name,
            "policy_id": None
        }
    }

    def __init__(self, policy_id):
        super().__init__()
        self.kwargs['json']['policy_id'] = policy_id

    def parse_response(self, response):
        return response.json().get('item').get('api_key')
