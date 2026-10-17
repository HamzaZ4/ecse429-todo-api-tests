from todo_api import constants


def test_get_todos_returns_the_two_default_todos(client):
    response = client.get(constants.TODOS_PATH)

    assert response.status_code == constants.OK
    titles = {todo["title"] for todo in response.json()["todos"]}
    assert titles == {"scan paperwork", "file paperwork"}


def test_get_todos_returns_done_status_as_a_string(client):
    todo = client.get(constants.TODOS_PATH).json()["todos"][0]

    assert todo["doneStatus"] in ("true", "false")


def test_head_todos_returns_headers_without_a_body(client):
    response = client.head(constants.TODOS_PATH)

    assert response.status_code == constants.OK
    assert response.text == ""
