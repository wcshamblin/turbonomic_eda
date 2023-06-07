Role Name
=========

This role is intended to be used with Turbonomic and Event Driven Ansible to resize AWS EC2 instance via actions generated from Turbonomic

Requirements
------------

- Amazon.Aws collection
- AWS command line interface
- Working Turbonomic environment with Event Driven Ansible
- Authentication method for AWS based on the ec2 module.  See [Amazon.Aws](https://docs.ansible.com/ansible/latest/collections/amazon/aws/docsite/aws_ec2_guide).html#authentication

Role Variables
--------------

 - ec2_region: Region ec2 instance is deployed to
 - instance_type: Instance Type/Size of ec2 instance to resize to
 - instance_id: AWS ec2 instance id

Dependencies
------------

Example Playbook
----------------

    - hosts: all
      gather_facts: false
      roles:
         - resize_ec2_instance

License
-------

GPL-2.0-or-later
