# https://github.com/sendgrid/sendgrid-python
import base64
from src.config import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType
from datetime import datetime, timedelta
from ics import Calendar, Event
import uuid

# Replace with your SendGrid API key


def send():
    message = Mail(
        from_email="bejoygm@gmail.com",
        to_emails="bejoyrock@gmail.com",
        subject="Calendar Event Invitation",
        plain_text_content="Please find the meeting details below.",
        html_content="<p>Please find the meeting details below.</p>",
    )

    # ics_content = gen_ics_file()
    event_start = datetime.now()
    event_end = event_start + timedelta(hours=1)

    ics_content = f"BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Your Company//CalDAV Calendar//EN\nBEGIN:VEVENT\nUID:{uuid.uuid4()}\nDTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}\nORG:Your Company\nSUMMARY:Meeting\nDTSTART:{event_start.strftime('%Y%m%dT%H%M%S')}\nDTEND:{event_end.strftime('%Y%m%dT%H%M%S')}\nEND:VEVENT\nEND:VCALENDAR"

    ics_content = base64.b64encode(ics_content.encode()).decode()

    # Create an attachment for the.ics file
    attachment = Attachment()
    attachment.file_content = FileContent(ics_content)
    attachment.file_name = FileName("meeting.ics")
    attachment.type = FileType("text/calendar")

    message.add_attachment(attachment)

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        print(str(e))


def gen_ics_file():
    c = Calendar()
    e = Event()
    e.summary = "My cool event"
    e.description = "A meaningful description"
    e.begin = datetime.fromisoformat("2022-06-06T12:05:23+02:00")
    e.end = datetime.fromisoformat("2022-06-06T13:05:23+02:00")
    c.events.add(e)
    return c.serialize()
