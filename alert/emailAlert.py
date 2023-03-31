import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class EmailAlert:
    def __init__(self, title, from_email, to_email) -> None:
        self.subject = title
        self.fromemail = from_email
        self.toemail = to_email

    def sendAlert(self):
        # Add an image to the message object (optional)
        image = "<img src=\"meow.png.jpg\" alt=\"My Image\">"

        # Create a multipart message object
        message = MIMEMultipart("related")
        message["Subject"] = "Test email with custom CSS styling"
        message["From"] = "sender@example.com"
        message["To"] = "recipient@example.com"

        #read in css and html
        current_dir = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(current_dir, "emailCSS.txt")) as css:
            rawcss = css.read()
        with open(os.path.join(current_dir, "htmlMsg.txt")) as html:
            rawhtml = html.read()

        # Create the HTML content
        html_content = rawhtml.format(self.subject, rawcss, "There", "This is a test", image)

        # Add the HTML content to the message object
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)



        # Connect to the SMTP server and send the email
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login("luwang827@gmail.com", "kqrfbyrsprgfoiuu")
        smtp_server.sendmail(self.fromemail, self.toemail, html_content)
        smtp_server.quit()

alert = EmailAlert("Yoyo Check it out","luwang827@gmail.com","jason.datac@gmail.com")
alert.sendAlert()