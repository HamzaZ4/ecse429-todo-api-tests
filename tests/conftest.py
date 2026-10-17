import pytest

from todo_api.client import TodoApiClient
from todo_api.server import TodoServer, resolve_jar_path


@pytest.fixture(scope="session")
def jar_path():
    return resolve_jar_path()


@pytest.fixture(autouse=True)
def running_server(jar_path):
    # every test gets its own server process so nothing from one test can leak
    # into the next one -- means tests don't care what order they run in
    server = TodoServer(jar_path)
    server.start()
    yield server
    server.stop()


@pytest.fixture
def client():
    return TodoApiClient()
