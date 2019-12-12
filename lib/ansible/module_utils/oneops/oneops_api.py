from ansible.module_utils import urls

def fetch_oneops_api(module_params, uri='/', method='GET', data=None, json=None):
  url = 'https://%s/%s' %(module_params['oneops_host'], uri.lstrip('/'))

  if not data and json:
    data = module.jsonify(json)

  return urls.open_url(url=url, method=method, data=data, force_basic_auth=True, url_username=module_params['api_key'], url_password='')
