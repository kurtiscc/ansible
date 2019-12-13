import json

from ansible.module_utils import urls
from ansible.module_utils.oneops import module_argument_spec


def fetch_oneops_api(module, uri='/', method='GET', data=None, json=None, headers={}):
    url = 'https://%s/%s' % (module.params['oneops_host'], uri.lstrip('/'))

    if not data and json:
        data = module.jsonify(json)

    headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })

    module.params.update(dict(
        url_username=module.params['api_key'],
        url_password='',
    ))

    return urls.fetch_url(module=module, url=url, method=method, data=data, headers=headers)


class OneOpsAssembly:
    @staticmethod
    def all(module):
        response = fetch_oneops_api(
            module,
            uri='%s/assemblies' % (
                module.params['organization'],
            )
        )
        return json.loads(response.read())

    @staticmethod
    def get(module):
        resp, info = fetch_oneops_api(
            module,
            uri='%s/assemblies/%s' % (
                module.params['organization'],
                module.params['assembly']['name']
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def exists(module):
        resp, info = fetch_oneops_api(
            module,
            uri='%s/assemblies/%s' % (
                module.params['organization'],
                module.params['assembly']['name']
            )
        )
        return info['status'] == 200

    @staticmethod
    def create(module):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies' % (
                module.params['organization']
            ),
            json={
                'cms_ci': {
                    'comments': module.params['assembly']['comments'],
                    'ciName': module.params['assembly']['name'],
                    'ciAttributes': {
                        'description': module.params['assembly']['description'],
                        'owner': module.params['email']
                    }
                }
            }
        )
        return json.loads(resp.read())

    @staticmethod
    def update(module):
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s' % (
                module.params['organization'],
                module.params['assembly']['name']
            ),
            json={
                'cms_ci': {
                    'comments': module.params['assembly']['comments'],
                    'ciName': module.params['assembly']['name'],
                    'ciAttributes': {
                        'description': module.params['assembly']['description'],
                        'owner': module.params['email']
                    }
                }
            }
        )
        return json.loads(resp.read())

    @staticmethod
    def upsert(module):
        if OneOpsAssembly.exists(module):
            return OneOpsAssembly.update(module)
        else:
            return OneOpsAssembly.create(module)

    @staticmethod
    def delete(module):
        resp, info = fetch_oneops_api(
            module,
            method="DELETE",
            uri='%s/assemblies/%s' % (
                module.params['organization'],
                module.params['assembly']['name']
            )
        )
        return json.loads(resp.read())


# end class OneOpsAssembly


class OneOpsPlatform:

    @staticmethod
    def all(module):
        resp, info = fetch_oneops_api(
            module,
            uri='%s/assemblies/%s/design/platforms' % (
                module.params['organization'],
                module.params['assembly']['name'],
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def get(module):
        resp, info = fetch_oneops_api(
            module,
            uri='%s/assemblies/%s/design/platforms/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def exists(module):
        resp, info = fetch_oneops_api(
            module,
            uri='%s/assemblies/%s/design/platforms/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
            )
        )
        return info['status'] == 200

    @staticmethod
    def create(module):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/design/platforms' % (
                module.params['organization'],
                module.params['assembly']['name'],
            ),
            json={
                'cms_dj_ci': {
                    'comments': module.params['platform']['comments'],
                    'ciName': module.params['platform']['name'],
                    'ciAttributes': {
                        'description': module.params['platform']['description'],
                        'source': module.params['platform']['pack']['source'],
                        'pack': module.params['platform']['pack']['name'],
                        'major_version': module.params['platform']['pack']['major_version'],
                        'version': module.params['platform']['pack']['version'],
                    }
                }
            }
        )
        return json.loads(resp.read())

    @staticmethod
    def update(module):
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s/design/platforms/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
            ),
            json={
                'cms_dj_ci': {
                    'comments': module.params['platform']['comments'],
                    'ciName': module.params['platform']['name'],
                    'ciAttributes': {
                        'description': module.params['platform']['description'],
                        'source': module.params['platform']['pack']['source'],
                        'pack': module.params['platform']['pack']['name'],
                        'major_version': module.params['platform']['pack']['major_version'],
                        'version': module.params['platform']['pack']['version'],
                    }
                }
            }
        )
        return json.loads(resp.read())

    @staticmethod
    def upsert(module):
        if OneOpsPlatform.exists(module):
            return OneOpsPlatform.update(module)
        else:
            return OneOpsPlatform.create(module)

    @staticmethod
    def delete(module):
        resp, info = fetch_oneops_api(
            module,
            method="DELETE",
            uri='%s/assemblies/%s/design/platforms/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
            )
        )
        return json.loads(resp.read())


# end class OneOpsPlatform


class OneOpsCloud:
    @staticmethod
    def all(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/clouds' % (
                module.params['organization'],
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def get(module, cloud):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/clouds/%s' % (
                module.params['organization'],
                cloud
            )
        )
        return json.loads(resp.read())


# end class OneOpsCloud

class OneOpsEnvironment:

    @staticmethod
    def all(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments' % (
                module.params['organization'],
                module.params['assembly']['name'],
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def get(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def exists(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
            )
        )
        return info['status'] == 200

    @staticmethod
    def build_environment_config(module):
        platforms = OneOpsPlatform.all(module)
        platform_availability = module_argument_spec.merge_dicts({}, list(
            map(lambda platform: dict({platform['ciId']: 'redundant'}), platforms)))

        def build_cloud_dict(cloud_def):
            cloud = OneOpsCloud.get(module, cloud_def['name'])
            return dict({cloud['ciId']: dict({
                'priority': '1',
                'dpmt_order': '1',
                'pct_scale': '100'
            })})

        clouds = dict()

        if module.params['environment']['clouds']:
            clouds = module_argument_spec.merge_dicts({}, list(
                map(build_cloud_dict, module.params['environment']['clouds'])))

        return {
            'clouds': clouds,
            'platform_availability': platform_availability,
            'cms_ci': {
                "ciName": module.params['environment']['name'],
                'nsPath': '%s/%s' % (
                    module.params['organization'],
                    module.params['assembly']['name']
                ),
                'ciAttributes': {
                    'debug': 'false',
                    'codpmt': 'false',
                    'profile': module.params['environment']['profile'],
                    'description': module.params['environment']['description'],
                    'availability': module.params['environment']['availability'],
                    'monitoring': 'true' if module.params['environment']['monitoring'] else 'false',
                    'autoscale': 'true' if module.params['environment']['autoscale'] else 'false',
                    'adminstatus': 'active',
                    'global_dns': 'true' if module.params['environment']['global_dns'] else 'false',
                    'verify': 'default',
                    'subdomain': module.params['environment']['subdomain'],
                    'logging': 'false',
                    'dpmtdelay': '60',
                    'autoreplace': 'true' if module.params['environment']['autoreplace'] else 'false',
                    'autorepair': 'true' if module.params['environment']['autorepair'] else 'false',
                }
            }
        }

    @staticmethod
    def create(module):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/transition/environments' % (
                module.params['organization'],
                module.params['assembly']['name'],
            ),
            json=OneOpsEnvironment.build_environment_config(module)
        )
        return json.loads(resp.read())

    @staticmethod
    def update(module):
        json = OneOpsEnvironment.build_environment_config(module)
        del json['cms_ci']['nsPath']
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s/transition/environments/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name']
            ),
            json=json
        )
        return json.loads(resp.read())

    @staticmethod
    def upsert(module):
        if OneOpsEnvironment.exists(module):
            return OneOpsEnvironment.update(module)
        else:
            return OneOpsEnvironment.create(module)

    @staticmethod
    def delete(module):
        resp, info = fetch_oneops_api(
            module,
            method="DELETE",
            uri='%s/assemblies/%s/transition/environments/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name']
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def pull_design(module):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/transition/environments/%s/pull' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name']
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def commit(module):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/transition/environments/%s/commit' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name']
            ),
            json={
                'desc': 'This release comitted by OneOps Ansible module'
            }
        )
        return json.loads(resp.read())

    @staticmethod
    def discard(module):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/transition/environments/%s/discard' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name']
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def enable(module):
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s/transition/environments/%s/enable' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name']
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def disable(module):
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s/transition/environments/%s/disable' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name']
            )
        )
        return json.loads(resp.read())

# end class OneOpsEnvironment
