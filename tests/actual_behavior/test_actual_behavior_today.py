# this is the other half: what the app ACTUALLY does right now. these pass today,
# and that's the point -- if one of these ever starts failing it means someone fixed
# the matching bug and the test_expected_* version should start passing instead

from todo_api import constants
from todo_api.payloads import todo_payload
from todo_api.state import assert_no_other_changes, capture_state


# bug 1
def test_actual_rejected_post_consumes_an_id(client):
    first = int(client.create_todo("first")["id"])
    client.post_json(constants.TODOS_PATH, {})

    second = int(client.create_todo("second")["id"])

    assert second == first + 2


# bug 2 - PUT silently removes the todo's relationships
def test_actual_put_removes_relationships_of_the_todo(client):
    client.put_json(client.todo_path(constants.TODO_WITH_RELATIONSHIPS_ID), todo_payload("replaced"))

    todo = client.get_todo(constants.TODO_WITH_RELATIONSHIPS_ID).json()["todos"][0]
    assert "tasksof" not in todo
    assert "categories" not in todo


def test_actual_put_leaves_the_project_and_category_themselves_intact(client):
    before = capture_state(client)

    client.put_json(client.todo_path(constants.TODO_WITH_RELATIONSHIPS_ID), todo_payload("replaced"))

    after = capture_state(client)
    assert before.categories["1"]["title"] == after.categories["1"]["title"]
    assert before.projects["1"]["title"] == after.projects["1"]["title"]


# bug 3 - doneStatus goes in as a bool but comes back out as a string
def test_actual_done_status_is_returned_as_string(client):
    created = client.post_json(constants.TODOS_PATH, {"title": "t", "doneStatus": True}).json()

    assert created["doneStatus"] == "true"


# bug 4 - Location header has no leading slash
def test_actual_location_header_has_no_leading_slash(client):
    response = client.post_json(constants.TODOS_PATH, todo_payload())

    assert response.headers["Location"].startswith("todos/")


# bug 5 - the error message for id-in-body doesn't say "not allowed", it's just confusing
def test_actual_id_in_put_body_message_says_id_should_be_id(client):
    todo = client.create_todo("x")

    response = client.put_json(client.todo_path(todo["id"]), {"title": "y", "id": todo["id"]})

    assert constants.MESSAGE_ID_IN_BODY in response.json()["errorMessages"][0]
