# Bug 03: doneStatus goes in as a boolean, comes back out as a string

**Executive summary:** doneStatus sent as boolean is returned as the string "true"/"false"

Small one but it'll trip up anyone treating the API as strictly typed.
doneStatus only accepts a real boolean on the way in -- if you send a string
like "maybe" instead, you get rejected with "doneStatus should be BOOLEAN".
Fine so far. But every response gives doneStatus back as a *string*, not a
boolean, even though you just sent it in as one.

To see it: POST `{"title":"t","doneStatus":true}` and look at what comes
back -- `"doneStatus":"true"`, with quotes around it. Expected `true`, got
`"true"`.

Medium impact. It's inconsistent (accepts bool, returns string), it breaks
a round trip, and any strict JSON schema check on the response is going to
flag this as the wrong type.

`test_expected_done_status_is_returned_as_boolean` fails on purpose (checks
`is True`). `test_actual_done_status_is_returned_as_string` passes and pins
the string behaviour (checks `== "true"`).
