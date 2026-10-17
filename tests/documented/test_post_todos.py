from todo_api import constants
from todo_api.payloads import todo_payload
from todo_api.state import assert_no_other_changes, capture_state


def test_post_todo_with_all_fields_creates_it(client):
    response = client.post_json(constants.TODOS_PATH, todo_payload("write report", True, "details"))

    assert response.status_code == constants.CREATED
    body = response.json()
    assert (body["title"], body["doneStatus"], body["description"]) == ("write report", "true", "details")


def test_post_todo_with_only_title_uses_defaults(client):
    body = client.create_todo("only a title")

    assert body["doneStatus"] == "false"
    assert body["description"] == ""


def test_post_todo_returns_location_header_of_new_todo(client):
    response = client.post_json(constants.TODOS_PATH, todo_payload())

    new_id = response.json()["id"]
    assert response.headers["Location"].endswith(f"todos/{new_id}")


def test_posted_todo_can_be_read_back(client):
    created = client.create_todo("read me back")

    fetched = client.get_todo(created["id"]).json()["todos"][0]

    assert fetched["title"] == "read me back"


def test_post_todo_changes_only_the_new_todo(client):
    before = capture_state(client)

    created = client.create_todo("side effect check")

    assert_no_other_changes(before, capture_state(client), todos=[created["id"]])


def test_post_todo_ids_increase_with_each_creation(client):
    first = int(client.create_todo("first")["id"])
    second = int(client.create_todo("second")["id"])

    assert second == first + 1
