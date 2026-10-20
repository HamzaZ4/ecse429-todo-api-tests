# Bug 01: Rejected POST /todos still consumes an id

**Executive summary:** Rejected POST /todos still consumes an id

Found this by accident while poking at the error-handling tests. If a POST to
/todos fails validation (empty body, empty title, bad doneStatus, whatever),
it comes back 400 like it should -- but the id counter on the server still
moves forward. So the next todo you successfully create isn't id+1, it's
id+2, and there's a gap no one asked for.

How to see it:

1. Fresh app, todos 1 and 2 already exist.
2. POST `{}` to /todos -> 400, "title : field is mandatory".
3. POST `{"title":"b"}` -> 201, but its id comes back as 4 instead of 3.

Not a huge deal on its own (impact-wise I'd call it low/medium), but it's the
kind of thing that'll confuse anyone who assumes ids are contiguous, and it
means a client spamming bad requests can burn through the id space for no
reason.

Tests: `test_expected_rejected_post_does_not_consume_an_id` is the one that
fails on purpose (asserts the id gap shouldn't happen).
`test_actual_rejected_post_consumes_an_id` passes and just pins down the real
+2 behaviour.
