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
TODO
'''

RETURN = '''
TODO
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
