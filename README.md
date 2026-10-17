# ECSE 429 Part A: todo manager API test suite (Python / pytest)

Scope: `/todos` and `/todos/:id`, plus the side effect PUT has on a todo's relationships.

## Setup
    pip install -r requirements.txt
    export TODO_JAR=/full/path/runTodoManagerRestAPI-1.5.5.jar   # or just put the jar in this folder
Java has to be installed, and nothing else can be listening on port 4567.

## Run
    pytest                                      # random order, pytest-randomly picks a seed and prints it
    pytest -p randomly --randomly-seed=1234      # re-run a specific order
    pytest -p no:randomly                        # fixed order
    pytest tests/documented                      # just one group

## How it works
Every test starts its own fresh copy of the jar and shuts it down afterwards, so nothing carries over between tests and the order they run in doesn't matter (startup takes about half a second).

`tests/documented` covers the behaviour that's actually in the swagger docs. `tests/undocumented` covers error handling, XML, and the odder data cases that aren't in the docs.

The spec asks for two separate modules wherever the app's behaviour doesn't match the docs: `tests/expected_behavior` writes down what the docs say should happen (these fail on purpose), and `tests/actual_behavior` writes down what actually happens (these pass). Each pair is one bug.

`todo_api/state.py` takes a snapshot of todos/projects/categories before and after a call, so the side-effect tests can prove nothing else got touched.

Bug write-ups are in `bugs/`. `scripts/capabilities.py` turns the Postman collection into a list of curl commands.

## Expected result
58 tests, 53 pass. The 5 that fail are the `test_expected_*` ones in `tests/expected_behavior` — they fail on purpose, each one is a documented bug.
