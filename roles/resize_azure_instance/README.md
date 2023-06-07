Role Name
=========

resize_azure_instance

Requirements
------------

- Azure.Azcollection collection
- Working Turbonomic environment with Event Driven Ansible
- Authentication method for Azure based on the azure module.  See [Azure Guide](https://docs.ansible.com/ansible/latest/scenario_guides/guide_azure.html).html#authentication

Role Variables
--------------

  - resource_group: Azure Resource Group the Virtual Machine is deployed to
  - instance_size: Size of instance to resize to
  - instance_name: Name of the Azure Instance

Dependencies
------------

Example Playbook
----------------

    - hosts: all
      gather_facts: false
      roles:
         - resize_azure_instance
         
License
-------

GPL-2.0-or-later