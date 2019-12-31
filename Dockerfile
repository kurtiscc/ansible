ARG docker_namespace=walmartlabs
ARG concord_ansible_version=latest

FROM $docker_namespace/concord-ansible:$concord_ansible_version
USER root

RUN pip install --upgrade ansible

RUN mkdir -p /usr/share/ansible/plugins/modules/cloud \
  && mkdir -p /usr/share/ansible/plugins/module_utils \
  && touch /usr/share/ansible/plugins/modules/__init__.py \
  && touch /usr/share/ansible/plugins/modules/cloud/__init__.py \
  && touch /usr/share/ansible/plugins/module_utils/__init__.py

COPY ./lib/ansible/modules/cloud/oneops /usr/share/ansible/plugins/modules/cloud/oneops
COPY ./lib/ansible/module_utils/oneops /usr/share/ansible/plugins/module_utils/oneops

USER concord
