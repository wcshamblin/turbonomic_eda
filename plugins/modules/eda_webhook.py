#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Ray Mileo <ray.mileo@ibm.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
---
module: eda_webhook
short_description: Module to allow users to create Turbonomic Webhooks to send
  actions to Event Drive Ansible
description:
  - This module provides a method for Turbonomic users to add a webhook to send
    actions to the webhook receiver plug-in for Event Driven Ansible
author: Ray Mileo (@yourGitHubHandle)
options:
  turbo_server:
    description: Hostname of Turbonomic server
    required: true
    type: str
  turbo_user:
    description: User with administrative access to Turbonomic
    required: true
    type: str
  turbo_pass:
    description: Password of Turbonomic user
    required: true
    type: str
  verify:
    description: Whether to validate the Turbonomic's TLS/SSL certificate
    required: false
    default: true
    type: bool
  eda_server:
    description: Hostname of Event Driven Ansible server
    required: true
    type: str
  eda_port:
    description: Port of Event Driven Ansible server
    required: false
    default: 5000
    type: int
  timeout:
    description: Timeout to set for calling Turbonomic's API
    required: false
    default: 15
    type: float

"""
EXAMPLES = """
---
- name: Add My Webhook with verify and eda port
  ibm.turbonomic_eda.eda_webhook:
    connection: turbonomic.example.com
    username: administrator
    password: password
    verify: false
    eda_server: eda2.example.com
    eda_port: 5001
"""
RETURN = """
---
webhook_resp:
    description: Response from creation of webhook
    type: dict
    returned: always
    sample: '{
                  "uuid": "0000001234567890",
                  "displayName": "Webhook To EDA",
                  "className": "Workflow",
                  "description": "Webhook to EDA http://eda.example.com:5000/endpoint",
                  "discoveredBy": {
                      "readonly": false
                  },
                  "type": "WEBHOOK",
                  "typeSpecificDetails": {
                      "url": " http://eda.example.com:5000/endpoint",
                      "method": "POST",
                      "template": "$converter.toJson($action)",
                      "authenticationMethod": "NONE",
                      "trustSelfSignedCertificates": false,
                      "type": "WebhookApiDTO"
                  }
              }'
"""
