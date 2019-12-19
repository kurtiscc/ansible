#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_assembly

short_description: A module for provisioning a OneOps assembly inside of an organization

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
            - The name of the organization to create the assembly in
        required: true
        type: str
    assembly:
        description:
            - A hash/dictionary of assembly configuration used to create the assembly
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the assembly
                required: true
                type: str
            comments:
                description:
                    - Comments for your assembly. Visible in the OneOps UI
                required: false
                type: str
                default: "This assembly created by the OneOps Ansible module"
            description:
                description:
                    - A useful description for your assembly
                required: false
                type: str
                default: "This assembly created by the OneOps Ansible module"

author:
    - Tate Barber (@tatemz)
    - Samuel Hymen (@s0hyman)
'''

EXAMPLES = '''
# Create a new Assembly
- name: Create my-assembly in my-org in OneOps
  oneops:
    oneops_host: oneops.example.com
    api_key: 12345abcde
    email: sam.walton@walmart.com
    organization: my-organization
    assembly:
        name: my-assembly
        comments: A comment attached to my assembly that can be read in OneOps UI
        description: A description of my assembly
'''

RETURN = '''
assembly:
    description: The assembly object from the OneOps API
    returned: when success
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api
from ansible.module_utils.common import dict_transformations


def get_oneops_assembly_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_assembly_module_argument_spec(),
        supports_check_mode=True
    )


def commit_latest_design_release(module, state):
    try:
        release = oneops_api.OneOpsRelease.latest(module)
    except AttributeError:
        release = None

    if release and release['releaseState'] == 'open':
        state.update(dict(changed=True))
        oneops_api.OneOpsRelease.commit(module, release['releaseId'])

    return state


def ensure_assembly(module, state):
    old_assembly = dict()
    if oneops_api.OneOpsAssembly.exists(module):
        old_assembly = oneops_api.OneOpsAssembly.get(module)
    new_assembly = oneops_api.OneOpsAssembly.upsert(module)
    diff = dict_transformations.recursive_diff(old_assembly, new_assembly)
    state.update(dict(
        changed=diff is not None,
        assembly=new_assembly,
    ))
    state = commit_latest_design_release(module, state)
    module.exit_json(**state)


def delete_assembly(module, state):
    if oneops_api.OneOpsAssembly.exists(module):
        assembly = oneops_api.OneOpsAssembly.get(module)
        oneops_api.OneOpsAssembly.delete(module)
        state.update(dict(
            changed=True,
            assembly=assembly
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
        assembly=dict(),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = get_oneops_assembly_module()

    if module.params['assembly']['state'] == 'present':
        return ensure_assembly(module, state)

    if module.params['assembly']['state'] == 'absent':
        return delete_assembly(module, state)

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
