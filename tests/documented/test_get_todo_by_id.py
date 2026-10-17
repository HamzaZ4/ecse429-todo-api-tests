from todo_api import constants


def test_get_existing_todo_returns_it(client):
    response = client.get_todo(constants.TODO_WITH_RELATIONSHIPS_ID)

    assert response.status_code == constants.OK
    todo = response.json()["todos"][0]
    assert todo["title"] == "scan paperwork"


def test_get_default_todo_lists_its_relationships(client):
    todo = client.get_todo(constants.TODO_WITH_RELATIONSHIPS_ID).json()["todos"][0]

    assert todo["tasksof"] == [{"id": "1"}]
    assert todo["categories"] == [{"id": "1"}]


def test_head_existing_todo_returns_ok_without_body(client):
    response = client.head(client.todo_path(constants.TODO_WITH_RELATIONSHIPS_ID))

    assert response.status_code == constants.OK
    assert response.text == ""
