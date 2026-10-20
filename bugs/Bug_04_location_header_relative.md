# Bug 04: Location header after POST is missing its leading slash

**Executive summary (<=80 chars):** Location header after POST has no leading slash (todos/3)

Lowest-impact bug of the five. POST /todos returns 201 with a Location
header, which is supposed to point at the new resource -- but it comes back
as `todos/3` instead of `/todos/3`. Without the leading slash that's a
*relative* reference, not an absolute path, so depending on what you resolve
it against it can point somewhere else entirely.

Steps: POST `{"title":"a"}` to /todos, then check the Location header on the
response. You get `todos/3`, expected `/todos/3` (or a full URL, that'd work
too).

Impact is low -- most clients probably just read the id out of the JSON
body and ignore Location anyway -- but a client that actually follows the
header per spec could build the wrong URL.

Tests: `test_expected_location_header_starts_with_slash` fails (checks
`.startswith("/")`), `test_actual_location_header_has_no_leading_slash`
passes (checks `.startswith("todos/")`, i.e. the actual broken format).
