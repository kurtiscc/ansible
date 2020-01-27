#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_variable_info

short_description: A module for fetching details for a OneOps variable inside of an assembly

version_added: "2.9"

description:
    - "OneOps documentation: http://oneops.com/overview/documentation.html"

options: TODO

author:
    - Tate Barber (@tatemz)
    - Samuel Hymen (@s0hyman)
'''

EXAMPLES = '''
- name: Get Assembly Variable
  oneops_variable_info:
    oneops_host: oneops.example.com
    api_key: 12345abcde
    email: sam.walton@walmart.com
    organization: my-organization
    assembly:
      name: my-assembly
    variable:
      name: my-variable
'''

RETURN = '''
TODO
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api
from ansible.module_utils.common import dict_transformations

def get_oneops_variable_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_variable_module_argument_spec(),
        supports_check_mode=True,
    )

def run_module():

    state = dict(
        changed=False,
        variable=dict(),
    )

    module = get_oneops_variable_module()

    variable, _, _ = oneops_api.OneOpsVariable.get(module)
    state.update(dict(
        variable=variable,
    ))

    module.exit_json(**state)

def main():
    run_module()


if __name__ == '__main__':
    main()
