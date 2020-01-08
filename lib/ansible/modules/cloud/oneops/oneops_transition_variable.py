#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_transition_variable

short_description: A module for provisioning a OneOps variable inside of a transition

version_added: "2.9"

description:
    - "OneOps documentation: http://oneops.com/overview/documentation.html"

options:
    oneops_host:
        description:
            - The hostname of the OneOps instance
        required: true
        type: str
    api_key:
        description:
            - A user's API key for communicating with the OneOps API
        required: true
        type: str
    email:
        description:
            - A user's email for communicating with the OneOps API
        required: true
        type: str
    organization:
        description:
            - The name of the organization to create the variable in
        required: true
        type: str
    assembly:
        description:
            - A hash/dictionary of assembly configuration used to add the variable
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the assembly the variable will be under
                required: true
                type: str
    variable:
        description:
            - A hash/dictionary of variable configuration used to create the variable
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the variable
                required: true
                type: str
            comments:
                description:
                    - Comments for your variable. Visible in the OneOps UI
                required: false
                type: str
                default: "This variable created by the OneOps Ansible module"
            description:
                description:
                    - A useful description for your variable
                required: false
                type: str
                default: "This variable created by the OneOps Ansible module"
            pack:
                description:
                    - A hash/dictionary of variable OneOps pack configuration used to create the variable
                required: false
                type: dict
                suboptions:
                    source:
                        description:
                            - The source of the OneOps pack
                        required: false
                        type: str
                        default: "oneops"
                    name:
                        description:
                            - The name of the OneOps pack
                        required: false
                        type: str
                        default: "custom"
                    major_version:
                        description:
                            - The major version number of the OneOps pack
                        required: false
                        type: str
                        default: "1"
                    version:
                        description:
                            - The minor version number of the OneOps pack
                        required: false
                        type: str
                        default: "1"

author:
    - Tate Barber (@tatemz)
    - Samuel Hymen (@s0hyman)
'''

EXAMPLES = '''
# Create a new variable
- name: Create my-variable in my-org in OneOps
  oneops:
    oneops_host: oneops.example.com
    api_key: 12345abcde
    email: sam.walton@walmart.com
    organization: my-organization
    variable:
        name: my-variable
        comments: A comment attached to my variable that can be read in OneOps UI
        description: A description of my variable
        pack: 
            source: my-source
            name: my-pack
            major_version: '1'
            version: '1'
'''

RETURN = '''
variable:
    description: The variable object from the OneOps API
    returned: when success
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api
from ansible.module_utils.common import dict_transformations


def get_oneops_variable_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_transition_variable_module_argument_spec(),
        supports_check_mode=True,
    )


def ensure_transition_variable(module, state):
    old_variable = dict()

    # Get original variable if it exists
    if oneops_api.OneOpsTransitionVariable.exists(module):
        old_variable, status, errors = oneops_api.OneOpsTransitionVariable.get(module)
        if not old_variable:
            module.fail_json(
                msg='Error fetching existing transition variable %s' % module.params['variable']['name'],
                status=status, errors=errors)

    # Update and store the variable
    new_variable, status, errors = oneops_api.OneOpsTransitionVariable.upsert(module)
    if errors:
        module.fail_json(
            msg='Error updating existing transition variable %s' % module.params['variable']['name'],
            status=status, errors=errors)

    # Compare the original vs the new variable
    diff = dict_transformations.recursive_diff(old_variable, new_variable)

    # Collect unreleased changes if variable is was updated
    atts_diff = None
    if new_variable['rfcAction'] == 'update':
        atts_diff = dict_transformations.recursive_diff(old_variable['ciBaseAttributes'],
                                                        new_variable['ciBaseAttributes'])

    state.update(dict(
        # Compare both the variable diff and the atts_diff (if an update)
        changed=(diff is not None or atts_diff is not None),
        variable=new_variable,
    ))

    module.exit_json(**state)

def run_module():
    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    state = dict(
        changed=False,
        variable=dict(),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = get_oneops_variable_module()

    if module.params['variable']['state'] == 'present':
        return ensure_transition_variable(module, state)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**state)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**state)


def main():
    run_module()


if __name__ == '__main__':
    main()
