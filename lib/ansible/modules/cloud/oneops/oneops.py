#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops

short_description: A module for provisioning and scaling OneOps computes

version_added: "2.4"

description:
    - "OneOps documentation: http://oneops.com/overview/documentation.html"

options:
    oneops_host:
        description:
            - The hostname of the OneOps instance
        required: true
    api_key:
        description:
            - A user's API key for communicating with the OneOps instance
        required: true

author:
    - Tate Barber (@tatemz)
'''

EXAMPLES = '''
# Run the OneOps module
- name: Test the OneOps modules
  oneops:
    oneops_host: oneops.example.com
'''

RETURN = '''
'''

from ansible.module_utils.basic import AnsibleModule


def get_oneops_module_argument_spec():
    return dict(
        oneops_host=dict(type='str', required=True),
        api_key=dict(type="str", required=True)
    )


def get_oneops_ansible_module():
    return AnsibleModule(
        argument_spec=get_oneops_module_argument_spec(),
        supports_check_mode=True
    )


def run_module():
    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = get_oneops_ansible_module()

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
