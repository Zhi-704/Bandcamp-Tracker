from dotenv import load_dotenv
from os import environ as ENV
import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

load_dotenv()

SENDER = f"Sender Name <{ENV["SES_SENDER"]}>"

RECIPIENTS = [
    {"email": "trainee.eyuale.lemma@sigmalabs.co.uk", "name": "Eyuale Lemma"},
]

AWS_REGION = "eu-west-2"

# The subject line for the email.
SUBJECT = "Apollo - Daily PDF report"

# The full path to the file that will be attached to the email.
ATTACHMENT = "./daily_report.pdf"

# The character encoding for the email.
CHARSET = "utf-8"

# Create a new SES resource and specify a region.
client = boto3.client(
    "ses",
    region_name=AWS_REGION,
    aws_access_key_id=ENV["ACCESS_KEY"],
    aws_secret_access_key=ENV["SECRET_ACCESS_KEY"],
)

for recipient in RECIPIENTS:
    recipient_email = recipient["email"]
    recipient_name = recipient["name"]

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = f"""Good morning, {
        recipient_name},\r\nPlease see the attached file for your daily generated Bandcamp sales report!"""

    # The HTML body of the email.
    BODY_HTML = f"""\
    <html>
    <head></head>
    <body>
    <h1>Good morning, {recipient_name}!</h1>
    <p>Please see the attached file for your daily generated Bandcamp sales report!</p>
    </body>
    </html>
    """

    # Create a multipart/mixed parent container.
    msg = MIMEMultipart("mixed")
    # Add subject, from and to lines.
    msg["Subject"] = SUBJECT
    msg["From"] = SENDER
    msg["To"] = recipient_email

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart("alternative")

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), "plain", CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), "html", CHARSET)

    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    # Define the attachment part and encode it using MIMEApplication.
    with open(ATTACHMENT, "rb") as attachment:
        att = MIMEApplication(attachment.read())

    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    att.add_header(
        "Content-Disposition", "attachment", filename=os.path.basename(ATTACHMENT)
    )

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    # Add the attachment to the parent container.
    msg.attach(att)

    try:
        # Provide the contents of the email.
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[recipient_email],
            RawMessage={
                "Data": msg.as_string(),
            },
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(
            f"Error sending email to {recipient_email}: {
                e.response['Error']['Message']}"
        )
    else:
        print(
            f"Email sent to {recipient_email}! Message ID: {
                response['MessageId']}"
        )
