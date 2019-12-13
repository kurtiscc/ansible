#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: oneops_environment

short_description: A module for provisioning a OneOps environment inside of an assembly

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
            - The name of the organization to create the environment in
        required: true
        type: str
    assembly:
        description:
            - A hash/dictionary of assembly configuration used to add the environment
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the assembly the environment will be under
                required: true
                type: str
    environment:
        description:
            - A hash/dictionary of environment configuration used to create the environment
        required: true
        type: dict
        suboptions:
            name:
                description:
                    - A name for the environment
                required: true
                type: str
            description:
                description:
                    - A useful description for your platform
                required: false
                type: str
                default: "This environment created by the OneOps Ansible module"
            profile:
                description:
                    - The profile for the environment
                required: true
                type: str
            availability:
                description:
                    - Single or redundant availability
                required: false
                choices: ['single', 'redundant']
                default: 'redundant'
            monitoring:
                description:
                    - Turn on/off monitoring
                type: bool
                required: false
                default: False
            autoscale:
                description:
                    - Turn on/off autoscale
                type: bool
                required: false
                default: false
            autoreplace:
                description:
                    - Turn on/off autoreplace
                type: bool
                required: false
                default: false
            autorepair:
                description:
                    - Turn on/off autorepair
                type: bool
                required: false
                default: false
            global_dns:
                description:
                    - Turn on/off global_dns
                type: bool
                required: false
                default: true
            subdomain:
                description:
                    - The subdomain for the environment 
                type: str
                required: false
            clouds:
                description:
                    - A list of hashes/dictionaries of cloud configuration used to deploy the environment
                required: false
                type: dict
                suboptions:
                    name:
                        description:
                            - A valid name of a registered cloud
                        required: true
                        type: str
                    priority:
                        description:
                            - Make this cloud primary or secondary
                        required: false
                        choices: [1, 2]
                        default: 1
                    dpmt_order:
                        description:
                            - Order of deployment for this cloud
                        required: false
                        type: int
                        default: 1
                    pct_scale:
                        description:
                            - Percentage of instances to be deployed in this cloud
                        required: false
                        type: int
                        default: 100

author:
    - Tate Barber (@tatemz)
    - Samuel Hymen (@s0hyman)
'''

EXAMPLES = '''
# Create a new environment
- name: Create my-environment in my-assembly
  oneops:
    oneops_host: oneops.example.com
    api_key: 12345abcde
    email: sam.walton@walmart.com
    organization: my-organization
    assembly:
      name: my-assembly
    environment:
      name: my-environment
      comments: A comment attached to my environment that can be read in OneOps UI
      description: A description of my environment
      profile: DEV
      clouds:
        - name: dev-cloud-1
    state: created
'''

RETURN = '''
environment:
    description: The environment object from the OneOps API
    returned: when success
    type: complex
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.oneops import module_argument_spec
from ansible.module_utils.oneops import oneops_api


def get_oneops_environment_module():
    return AnsibleModule(
        argument_spec=module_argument_spec.get_oneops_environment_module_argument_spec(),
        supports_check_mode=True,
    )


def create_environment(module, state):
    if not oneops_api.OneOpsEnvironment.exists(module):
        environment = oneops_api.OneOpsEnvironment.create(module)
        state.update(dict(
            changed=True,
            environment=environment,
        ))
    else:
        state.update(dict(
            environment=oneops_api.OneOpsEnvironment.get(module),
        ))

    module.exit_json(**state)


def delete_environment(module, state):
    if oneops_api.OneOpsEnvironment.exists(module):
        environment = oneops_api.OneOpsEnvironment.get(module)
        oneops_api.OneOpsEnvironment.delete(module)
        state.update(dict(
            changed=True,
            environment=environment
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
        environment=dict(),
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = get_oneops_environment_module()

    if module.params['state'] == 'created':
        return create_environment(module, state)

    if module.params['state'] == 'absent':
        return delete_environment(module, state)

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
