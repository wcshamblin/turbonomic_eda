# Ansible Collection: turbonomic_eda

This IBM Turbonomic Ansible Collection provides examples that can be used to automate Turbonomic cloud scaling decisions using Event Driven Ansible (EDA). Users are able to quickly realize the value of Turbonomic Hybrid Cloud optimization decisions by leveraging the flexible and powerful automation capabilities of Event Driven Ansible.

## Included in the Collection
- Module to create a webhook workflow within your Turbonomic Instance for use in Automation Policies
- Role for resizing an AWS EC2 instance via the Ansible module amazon.aws.ec2_instance and aws cli
- Role for resizing an Azure Virtual Machine via the Ansible module azure.azcollection.azure_rm_virtualmachine
- Playbooks for Event Driven Ansible to call to execute the roles
- Sample Event Driven Ansible Rulebook

## Prequisite
The following are required on the Event Driven Ansible Rulebook server in order to execute the playbooks and
roles from this collection.

### Install Necessary Ansible Collections

```
ansible-galaxy collection install ansible.eda azure.azcollection amazon.aws
```

### Install Necessary Python Software

```
python3 -m pip install awscli
```

## Installing the Collection

```
ansible-galaxy collection install ibm.turbonomic_eda
```

## Creating the webhook in Turbonomic
The Collection contains roles and playbooks to be used with Event Driven Ansible (EDA). Turbonomic cloud scaling automation policies can be configured to use a webhook workflow to send actions to EDA.

The webhook workflow feature must be enabled in Turbonomic using the steps described [here](https://www.ibm.com/docs/en/tarm/latest?topic=tasks-optional-enabling-disabling-probe-components) to add and enable a `webhook` probe.

Below is a example of a Ansible task to create the webhook workflow in Turbonomic:

```---
- name: Add My Webhook with verify and eda port
  ibm.turbonomic_eda.eda_webhook:
    connection: turbonomic.example.com
    username: administrator
    password: password
    verify: false
    eda_server: eda.example.com
    eda_port: 5000
```

- connection -> Hostname/IP of your Turbonomic instance
- username -> Turbonomic account with administrator access to create the webhook
- password -> Password of Turbonomic account
- verify -> Whether or not to validate the TLS certificate for the Turbonomic hostname
- eda_server -> Hostname/IP of your EDA server
- eda_port -> Port EDA server is listening on

Once the webhook is created, it must be assigned to cloud scaling actions that are to be forwarded to the
EDA server using a Turbonomic automation policy.  Please see [Turbonomic documentation](https://www.ibm.com/docs/en/tarm/latest?topic=policies-creating-automation) for further details on how to create automation policies. The webhook workflow should be selected for the Automation and Orchestration, Action Execution stage to replace the native execution for the entities in the scope of the policy.

Today the collection only supports scaling of AWS EC2 and Azure Virtual Machines which are known as Cloud Scaling Actions in Turbonomic.

## Using the Collection in an Event Driven Ansible Rulebook
Once the webhook is created and configured in Turbonomic to send the action(s) to EDA, you can use the [turbonomic_actions](extensions/eda/rulebooks/turbonomic_actions.yml) rulebook to call the Ansible playbooks and roles to execute the Cloud Scaling Actions.

```
---
- name: Read messages from a Turbonomic webhook and act on them
  hosts: localhost
  sources:
    - ansible.eda.webhook:
        host: 0.0.0.0
        port: 5000

  rules:
    - name: Run EC2 Playbook for Virtual Machine Scale Action
      condition: event.payload.target.className == "VirtualMachine" and event.payload.actionType == "SCALE" and
        event.payload.target.environmentType == "CLOUD" and event.payload.target.discoveredBy.type == "AWS"
      action:
        run_playbook:
          name: ibm.turbonomic_eda.resize_ec2
          extra_vars:
            instance_type: "{{ event['payload']['newEntity']['displayName'] }}"
            instance_id: "{{ event['payload']['target']['vendorIds'][event['payload']['target']['discoveredBy']['displayName']] }}"
            ec2_region: "{{ event['payload']['currentLocation']['vendorIds'][event['payload']['currentLocation']['discoveredBy']['displayName']] }}"
    - name: Run Azure Playbook for Virtual Machine Scale Action
      condition: event.payload.target.className == "VirtualMachine" and event.payload.actionType == "SCALE" and
        event.payload.target.environmentType == "CLOUD" and event.payload.target.discoveredBy.type == "Azure Subscription"
      action:
        run_playbook:
          name: ibm.turbonomic_eda.resize_azure
          extra_vars:
            resource_group: "{{ event['payload']['target']['aspects']['resourceGroup']['displayName'] }}"
            instance_size: "{{ event['payload']['newEntity']['displayName'] }}"
            instance_name: "{{ event['payload']['target']['displayName'] }}"
```

## Requirements

```
    ansible>=2.12.0
    python>=3.9 
    requests>=2.31
```

## Licensing

[Apache-2.0](http://www.apache.org/licenses/LICENSE-2.0)  


## Release Notes

[Please see the change log](https://github.com/IBM/turbonomic-ansible-eda/blob/main/changelogs/changelog.yaml)
