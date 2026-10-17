import pytest

from todo_api import constants
from todo_api.server import ServiceNotRunningError, require_service_running


def test_tests_fail_when_the_service_is_not_running(client, running_server):
    running_server.stop()

    with pytest.raises(ServiceNotRunningError):
        require_service_running()


def test_service_is_reachable_when_running(client):
    require_service_running()
    assert client.get(constants.TODOS_PATH).status_code == constants.OK
