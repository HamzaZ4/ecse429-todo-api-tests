import json

import requests

from todo_api import constants


class TodoApiClient:
    def send(self, method, path, headers=None, body=None):
        return requests.request(
            method,
            constants.BASE_URL + path,
            headers=headers,
            data=body,
            timeout=constants.REQUEST_TIMEOUT_SECONDS,
        )

    def get(self, path, headers=None):
        return self.send("GET", path, headers=headers)

    def head(self, path):
        return self.send("HEAD", path)

    def delete(self, path):
        return self.send("DELETE", path)

    def send_json(self, method, path, payload):
        return self.send(method, path, headers=constants.JSON_HEADERS, body=json.dumps(payload))

    def send_xml(self, method, path, xml_text):
        return self.send(method, path, headers=constants.XML_HEADERS, body=xml_text)

    def post_json(self, path, payload):
        return self.send_json("POST", path, payload)

    def put_json(self, path, payload):
        return self.send_json("PUT", path, payload)

    def post_raw(self, path, content_type, body):
        headers = {"Content-Type": content_type} if content_type else {}
        return self.send("POST", path, headers=headers, body=body)

    def create_todo(self, title="a todo", **fields):
        # a lot of tests just need SOME todo to exist first, so do the assert here
        # instead of making every single test repeat it
        response = self.post_json(constants.TODOS_PATH, {"title": title, **fields})
        assert response.status_code == constants.CREATED, response.text
        return response.json()

    def get_todo(self, todo_id):
        return self.get(f"{constants.TODOS_PATH}/{todo_id}")

    def todo_path(self, todo_id):
        return f"{constants.TODOS_PATH}/{todo_id}"
