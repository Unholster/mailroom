from collections import defaultdict
from email.message import EmailMessage
import json
import logging
import smtplib
from typing import Iterable, Tuple, List
from decouple import config
from flask import request, Flask
from yarl import URL
from .datatemplate import DataTemplate


logger = logging.getLogger(__name__)

application = app = Flask(__name__)


MAIL_URL = config('MAIL_URL', '', cast=URL)


def debug_info():
    '''Prints out startup info for debugging'''
    print('Starting Mailroom')
    print('=================')
    print(f'MAIL_URL = "{MAIL_URL}"')
    print('=================')

    assert \
        MAIL_URL is None or MAIL_URL.scheme in ('smtp'), \
        'MAIL_URL must use smtp:// scheme'


@app.route('/jobs', methods=['POST'])
def post_jobs():
    ''''Receives an e-mail send job'''
    try:
        payload = request.json
    except Exception as e:
        logger.exception(e)
        return errors_response(['Must provide JSON payload'])

    validation_errors = validate(
        ('template' in payload, 'Must include `template`'),
        ('data' in payload, 'Must include `data`'),
    )

    try:
        template = DataTemplate(payload['template'])
    except Exception as e:
        validation_errors.append([f'Could not parse template: {e}'])

    if validation_errors:
        return errors_response(validation_errors)

    succeeded = []
    errors = []

    for item in payload['data']:
        try:
            data = defaultdict(str, template.render(**item))
            print(data)
            send_message(
                from_address=data['from'],
                to_address=data['to'],
                message=make_message(data)
            )
            succeeded.append(True)
        except Exception as e:
            errors.append(e)

    return (
        json.dumps(
            {
                'message': 'Sent {} emails'.format(len(succeeded)),
                'errors': [str(e) for e in errors],
            },
            indent=4, sort_keys=True
        ),
        200,
        {'Content-Type': 'application/json'},
    )


def send_message(
    from_address: str,
    to_address: str,
    message: EmailMessage
) -> None:
    '''Sends an email message to the server specified by MAIL_URL'''

    if not MAIL_URL:
        print(message)
        return

    with smtplib.SMTP(MAIL_URL.host, MAIL_URL.port) as connection:
        connection.set_debuglevel(1)
        connection.starttls()
        if MAIL_URL.user:
            connection.login(
                MAIL_URL.user,
                MAIL_URL.password
            )
        connection.send_message(message)


def make_message(data: dict) -> EmailMessage:
    message = EmailMessage()
    message['subject'] = data['subject']
    message['to'] = data['to']
    message['from'] = data['from']
    message.add_alternative(data['text'], subtype='text')
    message.add_alternative(data['html'], subtype='html')
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
