# Bug 02: PUT /todos/:id silently deletes the todo's project and category links

**Executive summary (<=80 chars):** PUT /todos/:id silently deletes the todo's project and category links

This one's the worst of the five, imo. If you PUT a todo that's linked to a
project and a category (todo 1 in the default seed data is), those links
just disappear -- even if your PUT body never mentions relationships at all
and only changes, say, the title. The project and the category are both
still fine, they just stop pointing at the todo. No error, no warning,
just a plain 200 like everything's normal.

Repro:
- GET /todos/1 first. It has `tasksof: [{id: 1}]` and `categories: [{id: 1}]`.
- PUT /todos/1 with `{"title":"n"}`. Get back 200.
- GET /todos/1 again -- both `tasksof` and `categories` are gone.

I'd call the impact here high: a totally normal edit (just renaming a todo)
quietly breaks relationships someone set up on purpose, and the response
gives zero indication that happened.

Proven by `test_expected_put_keeps_relationships_of_the_todo` (fails -- it
asserts the links should still be there) and
`test_actual_put_removes_relationships_of_the_todo` (passes -- it asserts
they're gone, same as the real app does).
