#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_transition_deployment

short_description: A module for provisioning a OneOps deployment inside of an assembly

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
            - The name of the organization to create the deployment in
        required: true
        type: str
    assembly:
        description:
            - A hash/dictionary of assembly configuration used to add the deployment
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the assembly the deployment will be under
                required: true
                type: str
    deployment:
        description:
            - A hash/dictionary of deployment configuration used to create the deployment
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the deployment
                required: true
                type: str
            comments:
                description:
                    - Comments for your deployment. Visible in the OneOps UI
                required: false
                type: str
                default: "This deployment created by the OneOps Ansible module"
            description:
                description:
                    - A useful description for your deployment
                required: false
                type: str
                default: "This deployment created by the OneOps Ansible module"
            pack:
                description:
                    - A hash/dictionary of deployment OneOps pack configuration used to create the deployment
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
# Create a new deployment
- name: Create my-deployment in my-org in OneOps
  oneops:
    oneops_host: oneops.example.com
    api_key: 12345abcde
    email: sam.walton@walmart.com
    organization: my-organization
    deployment:
        name: my-deployment
        comments: A comment attached to my deployment that can be read in OneOps UI
        description: A description of my deployment
        pack: 
            source: my-source
            name: my-pack
            major_version: '1'
            version: '1'
'''

RETURN = '''
deployment:
    description: The deployment object from the OneOps API
    returned: when success
    type: complex
'''

import time

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api


def get_oneops_transition_deployment_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_transition_deployment_module_argument_spec(),
        supports_check_mode=True,
    )


def is_deployment_active_or_pending(deployment):
    return deployment["deploymentState"] == "active" or deployment["deploymentState"] == "pending"


def get_needed_deployment(module):
    try:
        deployment_bom, status, errors = oneops_api.OneOpsEnvironmentDeployment.bom(module)
    except AttributeError:
        deployment_bom = None

    return deployment_bom if deployment_bom and deployment_bom['release']['releaseState'] == 'open' and \
                             deployment_bom['rfcs']['cis'] else None


def wait_for_deployment_completion(module, deployment):
    while not deployment or "deploymentState" not in deployment or is_deployment_active_or_pending(deployment):
        time.sleep(5)
        deployment, status, errors = oneops_api.OneOpsEnvironmentDeployment.latest(module)
        if not deployment:
            module.fail_json(
                msg='Error fetching deployment in the %s environment while waiting for completion' %
                    module.params['environment']['name'],
                status=status, errors=errors)
    return deployment


def create_new_deployment_and_wait_for_completion(module, release):
    deployment, status, errors = oneops_api.OneOpsEnvironmentDeployment.create(module, release)
    if errors:
        module.fail_json(
            msg='Error creating deployment in the %s environment' %module.params['environment']['name'],
            status=status, errors=errors)
    deployment = wait_for_deployment_completion(module, deployment)
    return deployment


def ensure_completed_deployment_of_latest_release(module, state):
    needed_deployment = get_needed_deployment(module)

    if needed_deployment:
        # TODO: Determine if there is already the needed deployment in the paused state
        # TODO: Determine if we need to wait on a previous deployment (possibly not the one we need)
        deployment = create_new_deployment_and_wait_for_completion(module, needed_deployment['release'])
        state.update(dict(changed=True, deployment=deployment))

    module.exit_json(**state)


def run_module():
    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    state = dict(
        changed=False,
        deployment=dict(),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = get_oneops_transition_deployment_module()

    if module.params['deployment']['state'] == 'completed':
        return ensure_completed_deployment_of_latest_release(module, state)

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
