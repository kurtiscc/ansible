#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_transition_component

short_description: A module for provisioning a OneOps component inside of an assembly

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
            - The name of the organization to create the component in
        required: true
        type: str
    assembly:
        description:
            - A hash/dictionary of assembly configuration used to add the component
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the assembly the component will be under
                required: true
                type: str
    component:
        description:
            - A hash/dictionary of component configuration used to create the component
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the component
                required: true
                type: str
            comments:
                description:
                    - Comments for your component. Visible in the OneOps UI
                required: false
                type: str
                default: "This component created by the OneOps Ansible module"
            description:
                description:
                    - A useful description for your component
                required: false
                type: str
                default: "This component created by the OneOps Ansible module"
            pack:
                description:
                    - A hash/dictionary of component OneOps pack configuration used to create the component
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
# Create a new component
- name: Create my-component in my-org in OneOps
  oneops:
    oneops_host: oneops.example.com
    api_key: 12345abcde
    email: sam.walton@walmart.com
    organization: my-organization
    component:
        name: my-component
        comments: A comment attached to my component that can be read in OneOps UI
        description: A description of my component
        pack: 
            source: my-source
            name: my-pack
            major_version: '1'
            version: '1'
'''

RETURN = '''
component:
    description: The component object from the OneOps API
    returned: when success
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common import dict_transformations
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api


def touch_component(module, state):
    if oneops_api.OneOpsTransitionComponent.exists(module):
        component, status, errors = oneops_api.OneOpsTransitionComponent.get(module)
        if not component:
            module.fail_json(
                msg='Error fetching existing component %s before touching it' % module.params['component']['name'],
                status=status, errors=errors)
        state.update(component=component)

        # TODO: Figure out why API responds with hint only when querying by component ciId
        if not component['hint'] == 'touch':
            state.update(changed=True)
            _, status, errors = oneops_api.OneOpsTransitionComponent.touch(module)
            if errors:
                module.fail_json(
                    msg='Error touching existing component %s' % module.params['component']['name'],
                    status=status, errors=errors)

    module.exit_json(**state)


def update_component(module, state):
    if oneops_api.OneOpsTransitionComponent.exists(module):
        old_component, status, errors = oneops_api.OneOpsTransitionComponent.get(module)
        if not old_component:
            module.fail_json(
                msg='Error fetching existing transition component %s before updating it' %
                    module.params['component']['name'],
                status=status, errors=errors)

        updated_component, status, errors = oneops_api.OneOpsTransitionComponent.update(module)
        if errors:
            module.fail_json(
                msg='Error updating existing transition component %s' %
                    module.params['component']['name'],
                status=status, errors=errors)

        # We don't need to compare dependents or dependsOn to calculate changed
        old_component.pop('dependents', None)
        old_component.pop('dependsOn', None)

        # Compare the original vs the updated component
        diff = dict_transformations.recursive_diff(old_component, updated_component)

        # Collect unreleased changes if component is was updated
        atts_diff = None
        if updated_component['rfcAction'] == 'update':
            atts_diff = dict_transformations.recursive_diff(old_component['ciBaseAttributes'],
                                                            updated_component['ciBaseAttributes'])

        state.update(dict(
            # Compare both the component diff and the atts_diff (if an update)
            changed=(diff is not None or atts_diff is not None),
            component=updated_component,
        ))

    module.exit_json(**state)


def get_oneops_transition_component_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_transition_component_module_argument_spec(),
        supports_check_mode=True,
    )


def run_module():
    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    state = dict(
        changed=False,
        component=dict(),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = get_oneops_transition_component_module()

    if module.params['component']['state'] == 'updated':
        return update_component(module, state)

    if module.params['component']['state'] == 'touched':
        return touch_component(module, state)

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
