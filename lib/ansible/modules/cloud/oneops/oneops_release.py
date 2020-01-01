#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_release

short_description: A module for provisioning a OneOps release inside of an assembly

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
            - The name of the organization to create the release in
        required: true
        type: str
    assembly:
        description:
            - A hash/dictionary of assembly configuration used to add the release
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the assembly the release will be under
                required: true
                type: str
    release:
        description:
            - A hash/dictionary of release configuration used to create the release
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the release
                required: true
                type: str
            comments:
                description:
                    - Comments for your release. Visible in the OneOps UI
                required: false
                type: str
                default: "This release created by the OneOps Ansible module"
            description:
                description:
                    - A useful description for your release
                required: false
                type: str
                default: "This release created by the OneOps Ansible module"
            pack:
                description:
                    - A hash/dictionary of release OneOps pack configuration used to create the release
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
# Create a new release
- name: Create my-release in my-org in OneOps
  oneops:
    oneops_host: oneops.example.com
    api_key: 12345abcde
    email: sam.walton@walmart.com
    organization: my-organization
    release:
        name: my-release
        comments: A comment attached to my release that can be read in OneOps UI
        description: A description of my release
        pack: 
            source: my-source
            name: my-pack
            major_version: '1'
            version: '1'
'''

RETURN = '''
release:
    description: The release object from the OneOps API
    returned: when success
    type: complex
'''

import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api


def get_oneops_release_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_release_module_argument_spec(),
        supports_check_mode=True,
    )


def wait_for_release_close(module, release):
    # Check to see if new environment can be made
    info = None
    while release and release['releaseState'] == 'open' and info and info.status != 200:
        release = oneops_api.OneOpsRelease.latest(module)
        info = oneops_api.fetch_oneops_api(
            module,
            uri='%s/assemblies/%s/transition/environments/new.json' % (
                module.params['organization'],
                module.params['assembly']['name'],
            ),
        )
        time.sleep(5)
    return release


def close_release(module, state):
    try:
        release = oneops_api.OneOpsRelease.latest(module)
    except AttributeError:
        release = None

    if release and release['releaseState'] == 'open':
        oneops_api.OneOpsRelease.commit(module, release['releaseId'])
        release = wait_for_release_close(module, release)
        state.update(dict(changed=True, release=release))

    module.exit_json(**state)


def discard_release(module, state):
    try:
        release = oneops_api.OneOpsRelease.latest(module)
    except AttributeError:
        release = None

    if release and release['releaseState'] == 'open':
        state.update(dict(changed=True, release=release))
        oneops_api.OneOpsRelease.discard(module, release['releaseId'])

    module.exit_json(**state)


def run_module():
    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    state = dict(
        changed=False,
        release=dict(),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = get_oneops_release_module()

    if module.params['release']['state'] == 'closed':
        return close_release(module, state)

    if module.params['release']['state'] == 'discarded':
        return discard_release(module, state)

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
