# Use the sendgridAPI to send an email to breached users

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_breach_email(user):

    message = Mail(
        from_email='leaguelimiter@gmail.com',
        to_emails=user['email'],
        subject=f'Your accountability buddy {user["name"]} has breached their daily game limit.',
        html_content=f'<strong> {user["name"]} has now played more than {user["maxGames"]} games today. Shame them, kindly.</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

