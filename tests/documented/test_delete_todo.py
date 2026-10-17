from todo_api import constants
from todo_api.state import assert_no_other_changes, capture_state


def test_delete_existing_todo_succeeds(client):
    todo = client.create_todo("delete me")

    response = client.delete(client.todo_path(todo["id"]))

    assert response.status_code == constants.OK


def test_deleted_todo_can_no_longer_be_read(client):
    todo = client.create_todo("gone soon")
    client.delete(client.todo_path(todo["id"]))

    assert client.get_todo(todo["id"]).status_code == constants.NOT_FOUND


def test_delete_removes_only_the_target_todo(client):
    todo = client.create_todo("target")
    before = capture_state(client)

    client.delete(client.todo_path(todo["id"]))

    assert_no_other_changes(before, capture_state(client), todos=[todo["id"]])


def test_deleting_the_same_todo_twice_fails_the_second_time(client):
    todo = client.create_todo("delete twice")
    client.delete(client.todo_path(todo["id"]))

    assert client.delete(client.todo_path(todo["id"])).status_code == constants.NOT_FOUND
