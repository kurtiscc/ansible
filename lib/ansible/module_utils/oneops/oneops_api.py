import json

from ansible.module_utils import urls


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
