import os
import subprocess
import time
from pathlib import Path

import requests

from todo_api import constants


class ServiceNotRunningError(AssertionError):
    pass


class ServiceAlreadyRunningError(AssertionError):
    # something's already listening on 4567 before we even tried to start our own jar.
    # could be a leftover process from a crashed run, no way to know what state it's in
    pass


def resolve_jar_path():
    configured = os.environ.get(constants.JAR_ENVIRONMENT_VARIABLE)
    candidates = [Path(configured)] if configured else []
    project_root = Path(__file__).resolve().parent.parent
    candidates.append(project_root / constants.JAR_FILE_NAME)
    candidates.append(project_root.parent / constants.JAR_FILE_NAME)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"can't find {constants.JAR_FILE_NAME} -- set {constants.JAR_ENVIRONMENT_VARIABLE} to its "
        f"full path, or just drop the jar in {project_root}"
    )


def is_service_up():
    try:
        requests.get(constants.BASE_URL + constants.TODOS_PATH, timeout=0.5)
        return True
    except requests.RequestException:
        return False


def require_service_running():
    if not is_service_up():
        raise ServiceNotRunningError(f"nothing is answering at {constants.BASE_URL}, start the jar first")


class TodoServer:
    def __init__(self, jar_path):
        self._jar_path = jar_path
        self._process = None

    def start(self):
        if is_service_up():
            raise ServiceAlreadyRunningError(
                f"{constants.BASE_URL} is already taken, stop whatever is running there first"
            )
        self._process = subprocess.Popen(
            ["java", "-jar", str(self._jar_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        # give it a bit to actually come up before we give up on it
        deadline = time.monotonic() + 15
        while not is_service_up():
            if time.monotonic() > deadline:
                raise ServiceNotRunningError("the todo manager never came up")
            time.sleep(0.05)

    def stop(self):
        try:
            requests.get(constants.BASE_URL + "/shutdown", timeout=constants.REQUEST_TIMEOUT_SECONDS)
        except requests.RequestException:
            pass  # probably already dead, that's fine

        if self._process is not None:
            try:
                self._process.wait(timeout=constants.SERVER_STOP_TIMEOUT_SECONDS)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait()
            self._process = None

        deadline = time.monotonic() + constants.SERVER_STOP_TIMEOUT_SECONDS
        while is_service_up():
            if time.monotonic() > deadline:
                raise ServiceNotRunningError("the todo manager didn't actually stop")
            time.sleep(0.05)
