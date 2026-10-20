# Bug 05: confusing error message when you put an id in a PUT body

**Executive summary:** Supplying id in PUT body gives confusing 'id should be ID' error

Noticed this while writing the PUT validation tests. If you send an `id`
field in a PUT /todos/:id body, you get back 400 with the message "Failed
Validation: id should be ID". That message doesn't actually tell you
anything useful -- it reads like a type error, not "you're not allowed to
put an id in the body." Compare that to POST /todos with an id in the body,
which gives a much clearer "Not allowed to create with id."

Repro steps:
1. Create any todo, grab its id.
2. PUT /todos/<id> with `{"title":"y","id":"<id>"}`.
3. 400 comes back, read `errorMessages[0]`.

Only a bad error message so I'm calling impact low, but it's inconsistent
between the two methods (POST explains itself, PUT doesn't) and doesn't
actually tell the caller what to fix.

Covered by `test_expected_id_in_put_body_message_mentions_id_not_allowed`
(fails -- checks for "not allowed" in the message) and
`test_actual_id_in_put_body_message_says_id_should_be_id` (passes -- checks
for the real, confusing message text).
