import json
import time

from ansible.module_utils import urls
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.module_utils.oneops import module_argument_spec


def fetch_oneops_api(module, uri='/', method='GET', data=None, json=None, headers={}, query_params=None):
    def format_querystring(params=None):
        if not params:
            return ""

        return urlencode(params)

    query_string = format_querystring(query_params)

    url = 'https://%s/%s' % (module.params['oneops_host'], uri.lstrip('/'))
    if query_string != "":
        url = url + "?" + query_string

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
        # You can hit `%s/assemblies/%s/design/platforms/new.json` to get the default json for a platform
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/design/platforms/new.json' % (
                module.params['organization'],
                module.params['assembly']['name'],
            )
        )
        defaults = json.loads(resp.read())
        cms_dj_ci = module_argument_spec.merge_dicts({}, (defaults, {
            'ciName': module.params['platform']['name'],
            'comments': module.params['platform']['comments'],
            'ciAttributes': module_argument_spec.merge_dicts({
                'description': module.params['platform']['description'],
            }, module.params['platform']['attr']),
        }))
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/design/platforms' % (
                module.params['organization'],
                module.params['assembly']['name'],
            ),
            json={'cms_dj_ci': cms_dj_ci}
        )
        return json.loads(resp.read())

    @staticmethod
    def update(module):
        cms_dj_ci = module_argument_spec.merge_dicts({}, ({
            'ciName': module.params['platform']['name'],
            'comments': module.params['platform']['comments'],
            'ciAttributes': module_argument_spec.merge_dicts({
                'description': module.params['platform']['description'],
            }, module.params['platform']['attr']),
        }))
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s/design/platforms/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
            ),
            json={'cms_dj_ci': cms_dj_ci}
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


class OneOpsVariable:
    @staticmethod
    def get_uri(module, root_path=True):
        has_platform = 'platform' in module.params and module.params['platform'] and 'name' in module.params['platform']
        if has_platform and root_path:
            return '%s/assemblies/%s/design/platforms/%s/variables' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name']
            )
        if has_platform and not root_path:
            return '%s/assemblies/%s/design/platforms/%s/variables/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
                module.params['variable']['name'],
            )
        if not has_platform and root_path:
            return '%s/assemblies/%s/design/variables' % (
                module.params['organization'],
                module.params['assembly']['name'],
            )
        if not has_platform and not root_path:
            return '%s/assemblies/%s/design/variables/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['variable']['name'],
            )

    @staticmethod
    def all(module):
        resp, info = fetch_oneops_api(
            module,
            method='GET',
            uri=OneOpsVariable.get_uri(module),
        )
        return json.loads(resp.read())

    @staticmethod
    def get(module):
        resp, info = fetch_oneops_api(
            module,
            method='GET',
            uri=OneOpsVariable.get_uri(module, root_path=False),
        )
        return json.loads(resp.read())

    @staticmethod
    def exists(module):
        resp, info = fetch_oneops_api(
            module,
            method='GET',
            uri=OneOpsVariable.get_uri(module, root_path=False),
        )
        return info['status'] == 200

    @staticmethod
    def build_variable_attr(module):
        attr = dict()
        if module.params['variable']['secure']:
            attr.update({
                'secure': 'true',
                'encrypted_value': module.params['variable']['value'],
            })
        else:
            attr.update({
                'secure': 'false',
                'value': module.params['variable']['value'],
            })
        return attr

    @staticmethod
    def create(module):
        resp, info = fetch_oneops_api(
            module,
            method='POST',
            uri=OneOpsVariable.get_uri(module),
            json={
                'cms_dj_ci': {
                    'ciName': module.params['variable']['name'],
                    'ciAttributes': OneOpsVariable.build_variable_attr(module),
                },
            },
        )
        return json.loads(resp.read())

    @staticmethod
    def update(module):
        resp, info = fetch_oneops_api(
            module,
            method='PUT',
            uri=OneOpsVariable.get_uri(module, root_path=False),
            json={
                'cms_dj_ci': {
                    'ciAttributes': OneOpsVariable.build_variable_attr(module),
                },
            },
        )
        return json.loads(resp.read())

    @staticmethod
    def upsert(module):
        if OneOpsVariable.exists(module):
            return OneOpsVariable.update(module)
        else:
            return OneOpsVariable.create(module)

    @staticmethod
    def delete(module):
        resp, info = fetch_oneops_api(
            module,
            method='DELETE',
            uri=OneOpsVariable.get_uri(module, root_path=False),
        )
        return json.loads(resp.read())


# end class OneOpsDesignVariable

class OneOpsComponent:

    @staticmethod
    def all(module):
        resp, info = fetch_oneops_api(
            module,
            uri='%s/assemblies/%s/design/platforms/%s/components' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def get(module):
        resp, info = fetch_oneops_api(
            module,
            uri='%s/assemblies/%s/design/platforms/%s/components/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
                module.params['component']['name'],
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def exists(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/design/platforms/%s/components/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
                module.params['component']['name'],
            )
        )
        return info['status'] == 200

    @staticmethod
    def create(module):
        # You can hit `%s/assemblies/%s/design/platforms/%s/components/new.json?template_name=%s` to get the default json for a component
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/design/platforms/%s/components/new.json?template_name=%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
                module.params['component']['template_name'],
            )
        )
        defaults = json.loads(resp.read())
        cms_dj_ci = module_argument_spec.merge_dicts({}, (defaults, {
            'ciName': module.params['component']['name'],
            'comments': module.params['component']['comments'],
            'rfcAction': 'add',
            'ciAttributes': module.params['component']['attr'],
        }))
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/design/platforms/%s/components' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
            ),
            json={
                'template_name': module.params['component']['template_name'],
                'cms_dj_ci': cms_dj_ci,
            }
        )
        return json.loads(resp.read())

    @staticmethod
    def update(module):
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s/design/platforms/%s/components/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
                module.params['component']['name'],
            ),
            json={
                'cms_dj_ci': {
                    'ciName': module.params['component']['name'] or None,
                    'comments': module.params['component']['comments'] or None,
                    'ciAttributes': module.params['component']['attr'] or {},
                },
            },
        )
        return json.loads(resp.read())

    @staticmethod
    def upsert(module):
        if OneOpsComponent.exists(module):
            return OneOpsComponent.update(module)
        else:
            return OneOpsComponent.create(module)

    @staticmethod
    def delete(module):
        resp, info = fetch_oneops_api(
            module,
            method="DELETE",
            uri='%s/assemblies/%s/design/platforms/%s/components/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['platform']['name'],
                module.params['component']['name'],
            ),
        )
        return json.loads(resp.read())


# end class OneOpsComponent

class OneOpsRelease:

    @staticmethod
    def all(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/design/releases' % (
                module.params['organization'],
                module.params['assembly']['name'],
            )
        )
        return json.loads(resp.reads())

    @staticmethod
    def get(module, release):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/design/releases/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                release
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def latest(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/design/releases/latest' % (
                module.params['organization'],
                module.params['assembly']['name']
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def commit(module, release):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/design/releases/%s/commit' % (
                module.params['organization'],
                module.params['assembly']['name'],
                release
            ),
            json={'desc': module.params['release']['description']}
        )
        return json.loads(resp.read())

    @staticmethod
    def discard(module, release):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/design/releases/%s/discard' % (
                module.params['organization'],
                module.params['assembly']['name'],
                release
            )
        )
        return json.loads(resp.read())


# end class OneOpsDesignRelease


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
        # Build cms_csi
        resp, info = fetch_oneops_api(
            module,
            uri='%s/assemblies/%s/transition/environments/new.json' % (
                module.params['organization'],
                module.params['assembly']['name'],
            ),
        )
        env_defaults = json.loads(resp.read())
        cms_ci = module_argument_spec.merge_dicts({}, (env_defaults, {
            'ciName': module.params['environment']['name'],
            'comments': module.params['environment']['comments'],
            'ciAttributes': module_argument_spec.merge_dicts({}, (
                {'description': module.params['environment']['description']},
                module.params['environment']['attr'])),
        }))

        del cms_ci['ciClassName']

        # Build clouds
        def build_cloud_dict(cloud_def):
            cloud = OneOpsCloud.get(module, cloud_def['name'])
            return dict({str(cloud['ciId']): dict({
                'priority': str(cloud_def['priority']),
                'dpmt_order': str(cloud_def['dpmt_order']),
                'pct_scale': str(cloud_def['pct_scale']),
            })})

        clouds = dict()

        if module.params['environment']['clouds']:
            clouds = module_argument_spec.merge_dicts({}, list(
                map(build_cloud_dict, module.params['environment']['clouds'])))

        # Build platform_availability
        platforms = OneOpsPlatform.all(module)
        platform_availability = module_argument_spec.merge_dicts({}, list(
            map(lambda platform: dict({platform['ciId']: cms_ci['ciAttributes']['availability']}), platforms)))

        return {
            'cms_ci': cms_ci,
            'clouds': clouds,
            'platform_availability': platform_availability,
        }

    @staticmethod
    def create(module):
        json_payload = OneOpsEnvironment.build_environment_config(module)
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/transition/environments' % (
                module.params['organization'],
                module.params['assembly']['name'],
            ),
            json=json_payload
        )
        return json.loads(resp.read())

    @staticmethod
    def update(module):
        json_payload = OneOpsEnvironment.build_environment_config(module)
        del json_payload['cms_ci']['nsPath']
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s/transition/environments/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name']
            ),
            json=json_payload
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
            json={'desc': module.params['release']['description']},
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
                module.params['environment']['name'],
            ),
        )
        return json.loads(resp.read())

    @staticmethod
    def enable(module, platform_ids=None):
        query_params = None
        if platform_ids:
            query_params = list(map(lambda platform_id: ('platformCiIds[]', platform_id), platform_ids))
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s/transition/environments/%s/enable' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
            ),
            query_params=query_params,
        )
        return json.loads(resp.read())

    @staticmethod
    def disable(module, platform_ids=None):
        query_params = None
        if platform_ids:
            query_params = list(map(lambda platform_id: ('platformCiIds[]', platform_id), platform_ids))
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s/transition/environments/%s/disable' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name']
            ),
            query_params=query_params,
        )
        return json.loads(resp.read())


# end class OneOpsEnvironment


class OneOpsEnvironmentRelease:
    @staticmethod
    def all(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/releases' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
            ),
        )

        return json.loads(resp.read())

    @staticmethod
    def get(module, release):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/releases/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                release,
            ),
        )
        return json.loads(resp.read())

    @staticmethod
    def latest(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/releases/latest' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
            ),
        )
        return json.loads(resp.read())

    @staticmethod
    def exists(module, release):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/releases/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                release,
            ),
        )
        return info['status'] == 200

    @staticmethod
    def bom(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/releases/bom' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
            ),
        )
        return json.loads(resp.read())

    @staticmethod
    def discard(module, release):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/transition/environments/%s/releases/%s/discard' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                release,
            ),
        )
        return json.loads(resp.read())


# end class OneOpsEnvironmentRelease

class OneOpsEnvironmentDeployment:

    @staticmethod
    def all(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/deployments' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
            ),
        )
        return json.loads(resp.read())

    @staticmethod
    def get(module, deployment_id):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/deployments/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                deployment_id,
            ),
        )
        return json.loads(resp.read())

    @staticmethod
    def latest(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/deployments/latest' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
            ),
        )
        data = json.loads(resp.read())
        return data

    @staticmethod
    def bom(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/deployments/bom' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
            ),
        )
        data = json.loads(resp.read())
        return data

    @staticmethod
    def create(module, release):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/transition/environments/%s/deployments' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
            ),
            json={
                'cms_deployment': {
                    'comments': module.params['deployment']['comments'],
                    'nsPath': release['nsPath'],
                },
            },
        )
        return json.loads(resp.read())

    @staticmethod
    def update(module, deployment, state):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/transition/environments/%s/deployments/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                deployment['deploymentId'],
            ),
            json={
                'cms_deployment': {
                    'deploymentState': state,
                },
            },
        )
        return json.loads(resp.read())

    @staticmethod
    def cancel(module, deployment):
        OneOpsEnvironmentDeployment.update(module, deployment, 'canceled')

    @staticmethod
    def retry(module, deployment):
        OneOpsEnvironmentDeployment.update(module, deployment, 'active')

    @staticmethod
    def pause(module, deployment):
        OneOpsEnvironmentDeployment.update(module, deployment, 'paused')

    @staticmethod
    def resume(module, deployment):
        OneOpsEnvironmentDeployment.update(module, deployment, 'active')


# end class OneOpsEnvironmentDeployment


class OneOpsTransitionPlatform:

    @staticmethod
    def all(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/platforms' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def get(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/platforms/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                module.params['platform']['name'],
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def exists(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/platforms/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                module.params['platform']['name'],
            )
        )
        return info['status'] == 200

    @staticmethod
    def update(module):
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s/transition/environments/%s/platforms/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                module.params['platform']['name'],
            ),
            json={}
        )
        return json.loads(resp.read())

    @staticmethod
    def toggle(module):
        platform = OneOpsTransitionPlatform.get(module)
        OneOpsEnvironment.disable(module, platform_ids=[platform['ciId']])

    @staticmethod
    def enable(module):
        platform = OneOpsTransitionPlatform.get(module)
        OneOpsEnvironment.enable(module, platform_ids=[platform['ciId']])

    @staticmethod
    def disable(module):
        platform = OneOpsTransitionPlatform.get(module)
        OneOpsEnvironment.disable(module, platform_ids=[platform['ciId']])


# end class OneOpsTransitionPlatform


class OneOpsTransitionComponent:

    @staticmethod
    def all(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/platforms/%s/components' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                module.params['platform']['name'],
            )
        )
        return json.loads(resp.read())

    @staticmethod
    def get(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/platforms/%s/components/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                module.params['platform']['name'],
                module.params['component']['name'],
            ),
        )
        return json.loads(resp.read())

    @staticmethod
    def exists(module):
        resp, info = fetch_oneops_api(
            module,
            method="GET",
            uri='%s/assemblies/%s/transition/environments/%s/platforms/%s/components/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                module.params['platform']['name'],
                module.params['component']['name'],
            ),
        )
        return info['status'] == 200

    @staticmethod
    def update(module):
        resp, info = fetch_oneops_api(
            module,
            method="PUT",
            uri='%s/assemblies/%s/transition/environments/%s/platforms/%s/components/%s' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                module.params['platform']['name'],
                module.params['component']['name'],
            ),
            json={
                'cms_dj_ci': {
                    # TODO: Handle locking and owner props https://github.com/oneops/OneOpsAPIClient/blob/master/src/main/java/com/oneops/api/resource/Transition.java#L950
                    'ciAttributes': module.params['component']['attr'] or None
                }
            },
        )
        return json.loads(resp.read())

    @staticmethod
    def touch(module):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/transition/environments/%s/platforms/%s/components/%s/touch' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                module.params['platform']['name'],
                module.params['component']['name'],
            ),
        )
        return json.loads(resp.read())

    @staticmethod
    def deploy(module):
        resp, info = fetch_oneops_api(
            module,
            method="POST",
            uri='%s/assemblies/%s/transition/environments/%s/platforms/%s/components/%s/deploy' % (
                module.params['organization'],
                module.params['assembly']['name'],
                module.params['environment']['name'],
                module.params['platform']['name'],
                module.params['component']['name'],
            ),
        )
        return json.loads(resp.read())

# end class OneOpsTransitionComponent
