Mailroom
========

Mailroom is a service that allows sending templated e-mails.

Currently supports:
    - [ ] Single e-mail per job
    - [ ] Templating using [Jinja2](https://jinja2docs.readthedocs.io/en/stable/)
    - [ ] Storing templates on server
    - [ ] Send through SMTP + TLS, configurable by env var
    - [ ] Postgres backend
    - [ ] Expose handler function compatible with AWS serverless stack (API Gateway, AWS Lambda)
    - [ ] Supports multiple attachments (i.e. plain text + html text versions)

## Running locally

```sh
# Run with defaults
poetry run mailroom
```

## Send an e-mail

```sh
curl \
    -H content-type:application/json \
    -d '{"template": { "from": "sacuna@gmail.com", "to": ["sacuna@gmail.com"], "subject" : "Hello {{first_name}}", "body": "Greetings {{first_name}} {{last_name}}"}, "data": [{"first_name": "Seba", "last_name": "acuna"}]}' \
    -X POST \
    http://localhost:5000/jobs
```
