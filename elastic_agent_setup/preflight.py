from .api import *


class Preflight:

    def check(self):
        from .settings import Settings
        policy_id = None
        api_key = None
        if CheckService('kibana').run():
            if CheckService('elasticsearch').run():
                if not CheckFleetSetup().run():
                    SetupFleet().run()
                if not CheckFleetAgentsSetup().run():
                    SetupFleetAgents().run()
                for item in GetEnrollmentKeys().run().get('list'):
                    if item.get('name').startswith(Settings.enrollment_name):
                        if not policy_id and not api_key:
                            api_key_response = GetEnrollmentKey(item.get('id')).run()
                            policy_id = api_key_response.get('item').get('policy_id')
                            api_key = api_key_response.get('item').get('api_key')
                        else:
                            DeleteEnrollmentKey(item.get('id')).run()
                if not policy_id and not api_key:
                    policy_id = GetFleetAgentPolicyId().run()
                    api_key = CreateEnrollmentKey(policy_id).run()
        return {
            'policy_id': policy_id,
            'api_key': api_key
        }
