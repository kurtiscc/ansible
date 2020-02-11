#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_attachment

short_description: A module for provisioning a OneOps attachment inside of an assembly

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
            - The name of the organization to create the attachment in
        required: true
        type: str
    assembly:
        description:
            - A hash/dictionary of assembly configuration used to add the attachment
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the assembly the attachment will be under
                required: true
                type: str
    attachment:
        description:
            - A hash/dictionary of attachment configuration used to create the attachment
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the attachment
                required: true
                type: str
            comments:
                description:
                    - Comments for your attachment. Visible in the OneOps UI
                required: false
                type: str
                default: "This attachment created by the OneOps Ansible module"
            description:
                description:
                    - A useful description for your attachment
                required: false
                type: str
                default: "This attachment created by the OneOps Ansible module"
            pack:
                description:
                    - A hash/dictionary of attachment OneOps pack configuration used to create the attachment
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
# Create a new attachment
- name: Create my-attachment in my-org in OneOps
  oneops:
    oneops_host: oneops.example.com
    api_key: 12345abcde
    email: sam.walton@walmart.com
    organization: my-organization
    attachment:
        name: my-attachment
        comments: A comment attached to my attachment that can be read in OneOps UI
        description: A description of my attachment
        pack: 
            source: my-source
            name: my-pack
            major_version: '1'
            version: '1'
'''

RETURN = '''
attachment:
    description: The attachment object from the OneOps API
    returned: when success
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api
from ansible.module_utils.common import dict_transformations


def get_oneops_attachment_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_attachment_module_argument_spec(),
        supports_check_mode=True,
    )


def ensure_attachment(module, state):
    old_attachment = dict()

    # Get original attachment if it exists
    if oneops_api.OneOpsAttachment.exists(module):
        old_attachment, status, errors = oneops_api.OneOpsAttachment.get(module)
        if not old_attachment:
            module.fail_json(
                msg='Error fetching existing attachment %s before updating it' % module.params['attachment']['name'],
                status=status, errors=errors)

    # Update and store the attachment
    new_attachment, status, errors = oneops_api.OneOpsAttachment.upsert(module)
    if not new_attachment:
        module.fail_json(
            msg='Error creating/updating attachment %s' % module.params['attachment']['name'],
            status=status, errors=errors)

    # Compare the original vs the new attachment
    diff = dict_transformations.recursive_diff(old_attachment, new_attachment)

    state.update(dict(
        # Compare both the attachment diff and the atts_diff (if an update)
        changed=diff is not None,
        attachment=new_attachment,
    ))

    module.exit_json(**state)


def delete_attachment(module, state):
    if oneops_api.OneOpsAttachment.exists(module):
        attachment, status, errors = oneops_api.OneOpsAttachment.get(module)
        if not attachment:
            module.fail_json(
                msg='Error fetching existing attachment %s before deleting it' % module.params['attachment']['name'],
                status=status, errors=errors)

        _, status, errors = oneops_api.OneOpsAttachment.delete(module)
        if errors:
            module.fail_json(
                msg='Error deleting attachment %s' % module.params['attachment']['name'],
                status=status, errors=errors)

        state.update(dict(
            changed=True,
            attachment=attachment,
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
        attachment=dict(),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = get_oneops_attachment_module()

    if module.params['attachment']['state'] == 'present':
        return ensure_attachment(module, state)

    if module.params['attachment']['state'] == 'absent':
        return delete_attachment(module, state)

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
