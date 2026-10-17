import pytest

from todo_api import constants
from todo_api.payloads import todo_payload
from todo_api.state import assert_no_other_changes, capture_state


@pytest.mark.parametrize("payload, message", [
    ({}, "title : field is mandatory"),
    ({"title": ""}, "Failed Validation: title : can not be empty"),
    ({"title": "t", "doneStatus": "maybe"}, "Failed Validation: doneStatus should be BOOLEAN"),
])
def test_post_invalid_todo_is_rejected_with_message(client, payload, message):
    response = client.post_json(constants.TODOS_PATH, payload)

    assert response.status_code == constants.BAD_REQUEST
    assert message in response.json()["errorMessages"][0]


def test_post_invalid_todo_does_not_change_state(client):
    before = capture_state(client)

    client.post_json(constants.TODOS_PATH, {})

    assert_no_other_changes(before, capture_state(client))


def test_post_with_unknown_field_is_rejected(client):
    response = client.post_json(constants.TODOS_PATH, {"title": "t", "colour": "red"})

    assert response.status_code == constants.BAD_REQUEST
    assert "Could not find field: colour" in response.json()["errorMessages"][0]


def test_post_with_id_is_rejected(client):
    response = client.post_json(constants.TODOS_PATH, {"title": "t", "id": 50})

    assert response.status_code == constants.BAD_REQUEST


def test_post_with_malformed_json_is_rejected(client):
    response = client.post_raw(constants.TODOS_PATH, constants.JSON_CONTENT_TYPE, "{not json")

    assert response.status_code == constants.BAD_REQUEST


@pytest.mark.parametrize("content_type", ["application/foo", "application/x-www-form-urlencoded"])
def test_post_with_unsupported_content_type_returns_415(client, content_type):
    response = client.post_raw(constants.TODOS_PATH, content_type, "title=x")

    assert response.status_code == constants.UNSUPPORTED_MEDIA_TYPE


@pytest.mark.parametrize("method", ["get", "head", "delete"])
def test_unknown_todo_id_returns_404(client, method):
    response = getattr(client, method)(client.todo_path(constants.UNKNOWN_TODO_ID))

    assert response.status_code == constants.NOT_FOUND


@pytest.mark.parametrize("method", ["post_json", "put_json"])
def test_changing_unknown_todo_returns_404(client, method):
    response = getattr(client, method)(client.todo_path(constants.UNKNOWN_TODO_ID), todo_payload("x"))

    assert response.status_code == constants.NOT_FOUND


@pytest.mark.parametrize("todo_id", ["abc", "-1"])
def test_malformed_todo_id_returns_404(client, todo_id):
    assert client.get_todo(todo_id).status_code == constants.NOT_FOUND


def test_put_with_id_in_body_is_rejected(client):
    todo = client.create_todo("x")

    response = client.put_json(client.todo_path(todo["id"]), {"title": "y", "id": todo["id"]})

    assert response.status_code == constants.BAD_REQUEST
