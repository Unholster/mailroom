from collections import defaultdict
from email.message import EmailMessage
from email.mime.text import MIMEText
import json
import logging
import smtplib
from typing import Iterable, Tuple, List
from decouple import config
from flask import request
from flask_lambda import FlaskLambda
from .dicttemplate import DictTemplate


logger = logging.getLogger(__name__)

app = FlaskLambda(__name__)


MAIL_URL = config('MAIL_URL', '')


def debug_info():
    '''Prints out startup info for debugging'''
    print('Starting Mailroom')
    print('=================')
    print(f'MAIL_URL = "{MAIL_URL}"')
    print('=================')


@app.route('/jobs', methods=['POST'])
def post_jobs():
    ''''Receives an e-mail send job'''
    try:
        payload = request.json
    except Exception:
        return errors_response(['Must provide JSON payload'])

    errors = validate(
        ('template' in payload, 'Must include `template`'),
        ('data' in payload, 'Must include `data`'),
    )

    if errors:
        return errors_response(errors)

    sent = failed = 0

    for data in payload['data']:
        try:
            send_email(make_email(
                template=DictTemplate(payload['template']),
                data=data,
            ))
            sent += 1
        except Exception as e:
            logger.exception(e)
            failed += 1

    return (
        json.dumps(
            {
                'sent': f'Sent {sent} emails',
                'failed': f'Could not send {failed} emails'
            },
            indent=4, sort_keys=True
        ),
        200,
        {'Content-Type': 'application/json'},
    )


def send_email(message: EmailMessage) -> None:
    print(message)


def make_email(template: DictTemplate, data: dict) -> EmailMessage:
    rendered = defaultdict(str, template.render(**data))

    message = EmailMessage()
    message['subject'] = rendered['subject']
    message.add_alternative(rendered['text'], subtype='text')
    message.add_alternative(rendered['html'], subtype='html')
    return message


def validate(*rules: Iterable[Tuple[bool, str]]) -> List[str]:
    '''Validates a set of rules and returns an array of errors'''
    return [
        error_message
        for check, error_message in rules
        if not check
    ]


def errors_response(errors: List[str]) -> Tuple:
    '''Returns a 400 Flask response with error messages'''
    return (
        json.dumps({'errors': errors}, indent=4, sort_keys=True),
        400,
        {'Content-Type': 'application/json'},
    )


if __name__ == '__main__':
    debug_info()
    app.run(debug=True)
