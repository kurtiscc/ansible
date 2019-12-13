import json
import pytest

from ansible.modules.cloud.oneops import oneops
from ansible.module_utils.oneops import oneops_api
from ansible.module_utils.basic import AnsibleModule
from units.modules.utils import set_module_args

default_module_args = {
    'oneops_host': 'foo.bar.com',
    'api_key': 'foobar'
}


def test_fetch_oneops_api(mocker):
    set_module_args(default_module_args)

    module = oneops.get_oneops_module()

    open_url_mock = mocker.patch('ansible.module_utils.urls.open_url')
    oneops_api.fetch_oneops_api(module, uri='/')
    open_url_mock.assert_called_once_with(url='https://foo.bar.com/', data=None, method='GET',
                                          url_username='foobar', url_password='', force_basic_auth=True)


def test_fetch_oneops_api_with_json(mocker):
    set_module_args(default_module_args)

    module = oneops.get_oneops_module()

    open_url_mock = mocker.patch('ansible.module_utils.urls.open_url')
    oneops_api.fetch_oneops_api(module, uri='/', json={"message": "test"})
    open_url_mock.assert_called_once_with(url='https://foo.bar.com/', data='{"message": "test"}', method='GET',
                                          url_username='foobar', url_password='', force_basic_auth=True)
