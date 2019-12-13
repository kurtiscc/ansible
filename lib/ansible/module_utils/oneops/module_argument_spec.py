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
        ))
    )


def get_oneops_argument_spec_fragment_platform():
    return dict(
        platform=dict(type='dict', required=True, options=dict(
            name=dict(type='str', required=True),
            comments=dict(type='str', required=False, default="This platform created by the OneOps Ansible module"),
            description=dict(type='str', required=False, default="This platform created by the OneOps Ansible module"),
            pack=dict(type='dict', required=False, options=dict(
                source=dict(type='str', required=False, default='oneops'),
                name=dict(type='str', required=False, default='custom'),
                major_version=dict(type='str', required=False, default='1'),
                version=dict(type='str', required=False, default='1')
            ), default=dict()),
        ))
    )


def get_oneops_argument_spec_fragment_environment():
    return dict(
        environment=dict(type='dict', required=True, options=dict(
            name=dict(type='str', required=True),
            description=dict(type='str', required=False, default="This environment created by the OneOps Ansible module"),
            profile=dict(type='str', required=True),
            availability=dict(default='redundant', choices=['single', 'redundant']),
            monitoring=dict(type='bool', required=False, default=False),
            autoscale=dict(type='bool', required=False, default=False),
            autoreplace=dict(type='bool', required=False, default=False),
            autorepair=dict(type='bool', required=False, default=False),
            global_dns=dict(type='bool', required=False, default=True),
            subdomain=dict(type='str', required=False),
            clouds=dict(type='list', required=False, elements='dict', options=dict(
                name=dict(type='str', required=True),
                priority=dict(required=False, default=1, choices=[1, 2]),
                dpmt_order=dict(type='int', required=False, default=1),
                pct_scale=dict(type='int', required=False, default=100),
            ), default=[]),
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
        dict(state=dict(default='present', choices=['present', 'created', 'absent']))
    ))


def get_oneops_platform_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
        get_oneops_argument_spec_fragment_platform(),
        dict(state=dict(default='present', choices=['present', 'created', 'absent']))
    ))


def get_oneops_environment_module_argument_spec():
    return merge_dicts(dict(), (
        get_oneops_argument_spec_fragment_base(),
        get_oneops_argument_spec_fragment_organization(),
        get_oneops_argument_spec_fragment_assembly(),
        get_oneops_argument_spec_fragment_environment(),
        dict(state=dict(default='created', choices=['created', 'absent']))
    ))
