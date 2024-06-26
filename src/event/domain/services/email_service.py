# https://github.com/sendgrid/sendgrid-python
from typing import List
from src.config import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType


def send(ics: str, to_emails: str, subject: str, content: str):
    message = Mail(
        from_email="bejoygm@gmail.com",  # hardcode the sender for sendgrid test acc
        to_emails=to_emails,
        subject=subject,
        plain_text_content=content,
        html_content=f"<p>{content}</p>",
    )

    # Create an attachment for the.ics file
    attachment = Attachment()
    attachment.file_content = FileContent(ics)
    attachment.file_name = FileName("invite.ics")
    attachment.type = FileType("text/calendar")

    message.add_attachment(attachment)

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(str(e))
