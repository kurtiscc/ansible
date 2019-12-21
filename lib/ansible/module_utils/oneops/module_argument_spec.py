from ansible.module_utils.common import dict_transformations
from ansible.module_utils.common._collections_compat import Sequence


def merge_dicts(base_dict, merging_dicts):
    """This function merges a base dictionary with one or more other dictionaries.
    The base dictionary takes precedence when there is a key collision.
    merging_dicts can be a dict or a list or tuple of dicts.  In the latter case, the
    dictionaries at the front of the list have higher precedence over the ones at the end.
    """
    if not merging_dicts:
        merging_dicts = ({},)

    if not isinstance(merging_dicts, Sequence):
        merging_dicts = (merging_dicts,)

    new_dict = {}
    for d in merging_dicts:
        new_dict = dict_transformations.dict_merge(new_dict, d)

    new_dict = dict_transformations.dict_merge(new_dict, base_dict)

    return new_dict


def get_oneops_argument_spec_fragment_base():
    return dict(
        oneops_host=dict(type='str', required=True),
        api_key=dict(type="str", required=True),
        email=dict(type="str", required=True),
    )


def get_oneops_argument_spec_fragment_organization():
    return dict(
        organization=dict(type='str', required=True),
    )


def get_oneops_argument_spec_fragment_assembly():
    return dict(
        assembly=dict(type='dict', required=True, options=dict(
            name=dict(type='str', required=True),
            comments=dict(type='str', required=False, default="This assembly created by the OneOps Ansible module"),
            description=dict(type='str', required=False, default="This assembly created by the OneOps Ansible module"),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        ))
    )


def get_oneops_argument_spec_fragment_platform(required=True):
    return dict(
        platform=dict(type='dict', required=required, options=dict(
            name=dict(type='str', required=True),
            comments=dict(type='str', required=False, default="This platform created by the OneOps Ansible module"),
            description=dict(type='str', required=False, default="This platform created by the OneOps Ansible module"),
            attr=dict(type='dict', required=False, default=dict()),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        ))
    )


def get_oneops_argument_spec_fragment_variable():
    return dict(
        variable=dict(type='dict', required=True, options=dict(
            name=dict(type='str', required=True),
            value=dict(type='str', required=False, default=''),
            secure=dict(type='bool', required=False, default=False, choices=[True, False]),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        ))
    )


def get_oneops_argument_spec_fragment_component():
    return dict(
        component=dict(type='dict', required=True, options=dict(
            name=dict(type='str', required=True),
            template_name=dict(type='str', required=True),
            comments=dict(type='str', required=False, default="This component created by the OneOps Ansible module"),
            attr=dict(type='dict', required=False, default=dict()),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        ))
    )


def get_oneops_argument_spec_fragment_release():
    return dict(
        release=dict(type='dict', required=True, options=dict(
            description=dict(type='str', required=False, default='This release comitted by OneOps Ansible module'),
            state=dict(type='str', default='closed', choices=['closed', 'discarded']),
        ))
    )


def get_oneops_argument_spec_fragment_environment():
    return dict(
        environment=dict(type='dict', required=True, options=dict(
            name=dict(type='str', required=True),
            comments=dict(type='str', required=False, default="This environment created by the OneOps Ansible module"),
            description=dict(type='str', required=False,
                             default="This environment created by the OneOps Ansible module"),
            pull_design=dict(type='bool', required=False, default=False, choices=[True, False]),
            clouds=dict(type='list', required=False, elements='dict', options=dict(
                name=dict(type='str', required=True),
                priority=dict(type='int', required=False, default=1, choices=[1, 2]),
                dpmt_order=dict(type='int', required=False, default=1),
                pct_scale=dict(type='int', required=False, default=100),
            ), default=[]),
            attr=dict(type='dict', required=False, default=dict()),
            state=dict(type='str', default='present', choices=['present', 'absent']),
        ))
    )


def get_oneops_argument_spec_fragment_transition_platform():
    return dict(
        platform=dict(type='dict', required=True, options=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', default='enabled', choices=['enabled', 'disabled']),
        ))
    )


def get_oneops_argument_spec_fragment_transition_component():
    return dict(
        component=dict(type='dict', required=True, options=dict(
            name=dict(type='str', required=True),
            attr=dict(type='dict', required=False, default=dict()),
            state=dict(type='str', required=False, default='updated', choices=['updated', 'touched']),
        ))
    )


def get_oneops_argument_spec_fragment_transition_release():
    return dict(
        release=dict(type='dict', required=True, options=dict(
            description=dict(type='str', required=False, default='This release comitted by OneOps Ansible module'),
            snapshot_only=dict(type='bool', required=False, default=False, choices=[True, False]),
            excluded_platforms=dict(type='list', required=False, default=[], elements='dict',
                                   options=get_oneops_argument_spec_fragment_platform()['platform']['options']),
            state=dict(type='str', default='closed', choices=['closed', 'discarded']),
        ))
    )


def get_oneops_argument_spec_fragment_transition_deployment():
    return dict(
        deployment=dict(type='dict', required=True, options=dict(
            comments=dict(type='str', required=False, default='This deployment created by OneOps Ansible module'),
            state=dict(type='str', default='completed', choices=['completed']),
        ))
    )


def get_oneops_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base()
    ))


def get_oneops_assembly_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
    ))


def get_oneops_platform_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
        get_oneops_argument_spec_fragment_platform(),
    ))


def get_oneops_variable_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
        get_oneops_argument_spec_fragment_platform(required=False),
        get_oneops_argument_spec_fragment_variable(),
    ))


def get_oneops_component_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
        get_oneops_argument_spec_fragment_platform(),
        get_oneops_argument_spec_fragment_component(),
    ))


def get_oneops_release_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
        get_oneops_argument_spec_fragment_release(),
    ))


def get_oneops_environment_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
        get_oneops_argument_spec_fragment_environment(),
    ))


def get_oneops_transition_platform_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
        get_oneops_argument_spec_fragment_environment(),
        get_oneops_argument_spec_fragment_transition_platform(),
    ))


def get_oneops_transition_component_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
        get_oneops_argument_spec_fragment_environment(),
        get_oneops_argument_spec_fragment_transition_platform(),
        get_oneops_argument_spec_fragment_transition_component(),
    ))


def get_oneops_transition_release_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
        get_oneops_argument_spec_fragment_environment(),
        get_oneops_argument_spec_fragment_transition_release(),
    ))



def get_oneops_transition_deployment_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
        get_oneops_argument_spec_fragment_environment(),
        get_oneops_argument_spec_fragment_transition_deployment(),
    ))
