#!/usr/bin/env python
from __future__ import annotations

import json
from urllib.parse import urlunparse

try:
    import requests
except ImportError as imp_exc:
    ANOTHER_LIBRARY_IMPORT_ERROR = imp_exc
else:
    ANOTHER_LIBRARY_IMPORT_ERROR = None

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase

DEFAULT_TIMEOUT = 15
BASE_ENDPOINT = "/api/v3"
webhook_dto = {
    "displayName": "Webhook Call To EDA server",
    "className": "Workflow",
    "description": "Webhook to Event Driven Ansible",
    "discoveredBy": {"readonly": False},
    "type": "WEBHOOK",
    "typeSpecificDetails": {
        "url": "",
        "method": "POST",
        "template": "$converter.toJson($action)",
        "authenticationMethod": "NONE",
        "trustSelfSignedCertificates": False,
        "type": "WebhookApiDTO",
    },
}


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None) -> dict:
        """Main method for action"""
        if ANOTHER_LIBRARY_IMPORT_ERROR:
            raise AnsibleError('The requests library must be installed to use this action') from ANOTHER_LIBRARY_IMPORT_ERROR
        super().run(tmp=tmp, task_vars=task_vars)
        try:
            base_url = urlunparse(
                ("https", self._task.args["connection"], BASE_ENDPOINT, "", "", "")
            )

            files = {
                "username": self._task.args["username"],
                "password": self._task.args["password"],
            }
            eda_server = self._task.args["eda_server"]
        except KeyError as missing_arg:
            return self.missing_arg_error(missing_arg.args)

        eda_port = self._task.args.get("eda_port", 5000)

        # eda_url = f"http://{eda_server}:{eda_port}/endpoint"
        eda_url = urlunparse(
            ("http", f"{eda_server}:{eda_port}", "endpoint", "", "", "")
        )
        webhook_dto["typeSpecificDetails"]["url"] = eda_url
        webhook_dto["displayName"] = f'{webhook_dto["displayName"]}: {eda_url}'

        verify = self._task.args.get("verify", True)
        requests_kwargs = self._task.args.get("kwargs", {})
        with requests.Session() as turbo_conn:
            auth_resp = turbo_conn.post(
                f"{base_url}/login",
                data=files,
                allow_redirects=False,
                verify=verify,
                timeout=DEFAULT_TIMEOUT,
                **requests_kwargs,
            )
            resp_out = {}
            if auth_resp.status_code != 200:
                return self.handle_http_error(auth_resp)

            turbo_conn.headers["Content-Type"] = "application/json"
            call_resp = turbo_conn.post(
                f"{base_url}/workflows",
                data=json.dumps(webhook_dto),
                timeout=DEFAULT_TIMEOUT,
            )

            if call_resp.status_code != 200:
                return self.handle_http_error(call_resp)

            resp_out = {}
            resp_out["webhook"] = call_resp.text

        return resp_out

    def handle_http_error(self, api_response: requests.Response) -> dict:
        """Method to handle http errrors"""
        resp_out = {}
        resp_out["failed"] = True
        resp_out["msg"] = f"{api_response.status_code}: {api_response.reason}"
        resp_out["stderr"] = api_response.text
        resp_out["changed"] = False
        return resp_out

    def missing_arg_error(self, missing_arg):
        """Method to handle missing arguments for action"""
        resp_out = {}
        resp_out["failed"] = True
        resp_out["msg"] = f"Missing required argument {missing_arg}, check ansible task"
        resp_out["stderr"] = f"Missing required argument {missing_arg}"
        resp_out["changed"] = False
        return resp_out
