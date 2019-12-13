import json
import pytest

from ansible.module_utils.oneops import module_argument_spec


def test_merge_dicts():
    a = {'foo': 'bar'}
    b = dict(fizz='buzz')
    c = {'bar': 'foo'}
    assert module_argument_spec.merge_dicts(a, (b, c)) == dict(
        foo='bar',
        fizz='buzz',
        bar='foo'
    )

def test_get_oneops_module_argument_spec():
    assert list(module_argument_spec.get_oneops_module_argument_spec().keys()) == [
        'oneops_host',
        'api_key',
    ]

def test_get_oneops_assembly_module_argument_spec():
    assert list(module_argument_spec.get_oneops_assembly_module_argument_spec().keys()) == [
        'oneops_host',
        'api_key',
        'organization',
        'assembly',
        'state',
    ]
