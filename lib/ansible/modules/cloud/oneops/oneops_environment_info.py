#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_environment_info

short_description: A module for fetching details for a OneOps environment inside of an assembly

version_added: "2.9"

description:
    - "OneOps documentation: http://oneops.com/overview/documentation.html"

options: TODO

author:
    - Tate Barber (@tatemz)
    - Samuel Hymen (@s0hyman)
'''

EXAMPLES = '''
- name: Get Environment Info
  oneops_environment_info:
    oneops_host: oneops.example.com
    api_key: 12345abcde
    email: sam.walton@walmart.com
    organization: my-organization
    assembly:
      name: my-assembly
    environment:
      name: my-environment
'''

RETURN = '''
TODO
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api
from ansible.module_utils.common import dict_transformations


def get_oneops_environment_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_environment_module_argument_spec(),
        supports_check_mode=True,
    )

def run_module():
    state = dict(
        changed=False,
        environment=dict(),
    )

    module = get_oneops_environment_module()

    env, _, _ = oneops_api.OneOpsEnvironment.get(module);

    state.update(dict(
        environment=env
    ))

    module.exit_json(**state)


def main():
    run_module()


if __name__ == '__main__':
    main()
