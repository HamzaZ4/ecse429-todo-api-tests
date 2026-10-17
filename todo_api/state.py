# before/after snapshots of everything, so the side-effect tests can prove nothing
# else got touched by a single /todos call

from todo_api import constants


class SystemState:
    def __init__(self, todos, projects, categories):
        self.todos = todos
        self.projects = projects
        self.categories = categories


def capture_state(client):
    todos = _get_by_id(client, constants.TODOS_PATH, "todos")
    projects = _get_by_id(client, constants.PROJECTS_PATH, "projects")
    categories = _get_by_id(client, constants.CATEGORIES_PATH, "categories")
    return SystemState(todos, projects, categories)


def _get_by_id(client, path, key):
    response = client.get(path)
    assert response.status_code == constants.OK, f"could not read {path}: {response.text}"
    by_id = {}
    for entity in response.json()[key]:
        by_id[entity["id"]] = entity
    return by_id


def assert_no_other_changes(before, after, todos=(), projects=(), categories=()):
    # anything NOT in these id lists has to look exactly the same before and after
    _check_unchanged("todos", before.todos, after.todos, set(todos))
    _check_unchanged("projects", before.projects, after.projects, set(projects))
    _check_unchanged("categories", before.categories, after.categories, set(categories))


def _check_unchanged(name, before, after, allowed_ids):
    all_ids = set(before) | set(after)
    for entity_id in all_ids - allowed_ids:
        assert before.get(entity_id) == after.get(entity_id), (
            f"{name} {entity_id} changed from {before.get(entity_id)} to {after.get(entity_id)} "
            "and it wasn't supposed to"
        )
