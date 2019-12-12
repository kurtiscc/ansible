import json
import pytest

from ansible.modules.cloud.oneops import oneops
from units.modules.utils import set_module_args

def validate_missing_params(capfd, module_params={}, results_msg_list=()):
    with pytest.raises(SystemExit):
        set_module_args(module_params)
        oneops.main()

    out, err = capfd.readouterr()
    results = json.loads(out)

    assert results['failed'] is True
    assert all(txt in results['msg'] for txt in results_msg_list)


def test_mandatory_oneops_host(capfd):
    validate_missing_params(capfd=capfd, module_params={},
        results_msg_list=('missing', 'required', 'oneops_host'))
    validate_missing_params(capfd=capfd, module_params={
        'oneops_host': 'foobar.com'},
        results_msg_list=('missing', 'required', 'api_key'))