import os, base64
import smtplib
from email.message import EmailMessage

class EmailAlert:
    def __init__(self, title, from_email, to_email) -> None:
        self.subject = title
        self.fromemail = from_email
        self.toemail = to_email

    def sendAlert(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Add an image to the message object (optional)
        with open(os.path.join(current_dir, "what.png"), "rb") as image_file:
            image = base64.b64encode(image_file.read()).decode("utf-8")


        #read in css and html
        with open(os.path.join(current_dir, "emailCSS.txt")) as css:
            rawcss = css.read()
        with open(os.path.join(current_dir, "htmlMsg.txt")) as html:
            rawhtml = html.read()

        # Create the HTML content
        html_content = rawhtml.format(self.subject, rawcss, "There", "This is a test", image)

        # Connect to the SMTP server and send the email
        smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
        smtp_server.starttls()
        smtp_server.login("luwang827@gmail.com", "kqrfbyrsprgfoiuu")
        smtp_server.sendmail(self.fromemail, self.toemail, html_content)
        smtp_server.quit()

alert = EmailAlert("Yoyo Check it out","luwang827@gmail.com","luwang827@gmail.com")
alert.sendAlert()