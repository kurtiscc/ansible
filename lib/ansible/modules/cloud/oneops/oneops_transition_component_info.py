#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_transition_component_info

short_description: A module for fetching details for a OneOps component inside of an assembly

version_added: "2.9"

description:
    - "OneOps documentation: http://oneops.com/overview/documentation.html"

options: TODO

author:
    - Tate Barber (@tatemz)
    - Samuel Hymen (@s0hyman)
'''

EXAMPLES = '''
- name: Get Transition Component Info
  oneops_transition_component_info:
    oneops_host: oneops.example.com
    api_key: 12345abcde
    email: sam.walton@walmart.com
    organization: my-organization
    assembly:
      name: my-assembly
    environment:
      name: my-env
    platform:
      name: my-platform
    component:
      name: my-component
'''

RETURN = '''
TODO
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common import dict_transformations
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api

def get_oneops_transition_component_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_transition_component_module_argument_spec(),
        supports_check_mode=True,
    )


def run_module():
    state = dict(
        changed=False,
        component=dict(),
    )

    module = get_oneops_transition_component_module()

    component, _, _ = oneops_api.OneOpsTransitionComponent.get(module)

    state.update(dict(
        component = component
    ))

    module.exit_json(**state)


def main():
    run_module()


if __name__ == '__main__':
    main()
