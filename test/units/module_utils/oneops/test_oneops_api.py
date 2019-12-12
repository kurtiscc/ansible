import json
import pytest

from ansible.module_utils.oneops import oneops_api

mock_module_params = {
    'oneops_host': 'foo.bar.com',
    'api_key': 'foobar'
}

def test_fetch_oneops_api(mocker):
    open_url_mock = mocker.patch('ansible.module_utils.urls.open_url')
    oneops_api.fetch_oneops_api(mock_module_params, uri='/')
    open_url_mock.assert_called_once_with(url='https://foo.bar.com/', data=None, method='GET',
                                     url_username='foobar', url_password='', force_basic_auth=True)