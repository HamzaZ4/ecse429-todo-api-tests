from todo_api import constants
from todo_api.payloads import todo_payload
from todo_api.state import assert_no_other_changes, capture_state


def test_post_amend_changes_only_the_given_field(client):
    todo = client.create_todo("original", description="keep me")

    response = client.post_json(client.todo_path(todo["id"]), {"title": "renamed"})

    assert response.status_code == constants.OK
    amended = client.get_todo(todo["id"]).json()["todos"][0]
    assert (amended["title"], amended["description"]) == ("renamed", "keep me")


def test_post_amend_changes_only_the_target_todo(client):
    todo = client.create_todo("target")
    before = capture_state(client)

    client.post_json(client.todo_path(todo["id"]), {"doneStatus": True})

    assert_no_other_changes(before, capture_state(client), todos=[todo["id"]])


def test_put_replaces_all_fields(client):
    todo = client.create_todo("original", description="old description")

    response = client.put_json(client.todo_path(todo["id"]), {"title": "replaced"})

    assert response.status_code == constants.OK
    replaced = client.get_todo(todo["id"]).json()["todos"][0]
    assert (replaced["title"], replaced["description"]) == ("replaced", "")


def test_put_changes_only_the_target_todo(client):
    todo = client.create_todo("target")
    before = capture_state(client)

    client.put_json(client.todo_path(todo["id"]), todo_payload("replaced"))

    assert_no_other_changes(before, capture_state(client), todos=[todo["id"]])


def test_put_without_title_is_rejected(client):
    todo = client.create_todo("needs title")

    response = client.put_json(client.todo_path(todo["id"]), {"description": "no title"})

    assert response.status_code == constants.BAD_REQUEST
