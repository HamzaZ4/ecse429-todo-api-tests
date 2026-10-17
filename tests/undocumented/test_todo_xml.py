from todo_api import constants
from todo_api.payloads import parse_xml, todo_xml


def test_post_todo_as_xml_creates_it(client):
    response = client.send_xml("POST", constants.TODOS_PATH, todo_xml("from xml", False))

    assert response.status_code == constants.CREATED
    assert parse_xml(response.text).findtext("title") == "from xml"


def test_get_todos_as_xml_returns_xml(client):
    response = client.get(constants.TODOS_PATH, headers=constants.ACCEPT_XML_HEADERS)

    assert response.status_code == constants.OK
    assert parse_xml(response.text).tag == "todos"


def test_post_xml_without_title_is_rejected(client):
    response = client.send_xml("POST", constants.TODOS_PATH, "<todo><description>x</description></todo>")

    assert response.status_code == constants.BAD_REQUEST


def test_post_malformed_xml_is_rejected(client):
    response = client.send_xml("POST", constants.TODOS_PATH, "<todo><title>unclosed")

    assert response.status_code == constants.BAD_REQUEST
