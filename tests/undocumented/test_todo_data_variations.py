from todo_api import constants


def test_very_long_title_is_accepted(client):
    created = client.create_todo("x" * constants.LONG_TITLE_LENGTH)

    assert len(client.get_todo(created["id"]).json()["todos"][0]["title"]) == constants.LONG_TITLE_LENGTH


def test_special_characters_in_title_round_trip(client):
    created = client.create_todo(constants.SPECIAL_CHARACTERS_TITLE)

    assert client.get_todo(created["id"]).json()["todos"][0]["title"] == constants.SPECIAL_CHARACTERS_TITLE


def test_done_status_can_be_toggled_with_amend(client):
    todo = client.create_todo("toggle")

    client.post_json(client.todo_path(todo["id"]), {"doneStatus": True})

    assert client.get_todo(todo["id"]).json()["todos"][0]["doneStatus"] == "true"
