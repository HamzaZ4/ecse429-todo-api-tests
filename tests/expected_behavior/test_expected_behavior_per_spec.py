# what the spec/docs say should happen. these fail on purpose right now -- each
# failure here is one of the bugs written up in bugs/

from todo_api import constants
from todo_api.payloads import todo_payload
from todo_api.state import assert_no_other_changes, capture_state


def test_expected_rejected_post_does_not_consume_an_id(client):
    first = int(client.create_todo("first")["id"])
    client.post_json(constants.TODOS_PATH, {})

    second = int(client.create_todo("second")["id"])

    assert second == first + 1


def test_expected_put_keeps_relationships_of_the_todo(client):
    client.put_json(client.todo_path(constants.TODO_WITH_RELATIONSHIPS_ID), todo_payload("replaced"))

    todo = client.get_todo(constants.TODO_WITH_RELATIONSHIPS_ID).json()["todos"][0]
    assert todo.get("tasksof") == [{"id": "1"}]
    assert todo.get("categories") == [{"id": "1"}]


def test_expected_done_status_is_returned_as_boolean(client):
    created = client.post_json(constants.TODOS_PATH, {"title": "t", "doneStatus": True}).json()

    assert created["doneStatus"] is True


def test_expected_location_header_starts_with_slash(client):
    response = client.post_json(constants.TODOS_PATH, todo_payload())

    assert response.headers["Location"].startswith("/")


def test_expected_id_in_put_body_message_mentions_id_not_allowed(client):
    todo = client.create_todo("x")

    response = client.put_json(client.todo_path(todo["id"]), {"title": "y", "id": todo["id"]})

    assert "not allowed" in response.json()["errorMessages"][0].lower()
