#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_transition_attachment_info

short_description: A module for fetching details for a OneOps attachment inside of a transition

version_added: "2.9"

description:
    - "OneOps documentation: http://oneops.com/overview/documentation.html"

options: TODO

author:
    - Tate Barber (@tatemz)
    - Samuel Hymen (@s0hyman)
'''

EXAMPLES = '''
TODO
'''

RETURN = '''
TODO
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api
from ansible.module_utils.common import dict_transformations


def get_oneops_attachment_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_transition_attachment_info_module_argument_spec(),
        supports_check_mode=True,
    )

def run_module():
    state = dict(
        changed=False,
        attachment=dict(),
    )

    module = get_oneops_attachment_module()

    attachment, _, _ = oneops_api.OneOpsTransitionAttachment.get(module)

    state.update(dict(
        attachment = attachment
    ))

    module.exit_json(**state)


def main():
    run_module()


if __name__ == '__main__':
    main()
