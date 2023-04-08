from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from base64 import urlsafe_b64decode, urlsafe_b64encode
import os
import pickle
from html.parser import HTMLParser
import datetime
import base64
from BillParser import HTMLParser_Electricity, HTMLParser_WaterBill3120, HTMLParser_WaterBill2348

# replace with the path to your credentials JSON file
current_dir = os.path.dirname(os.path.realpath(__file__))
SCOPES = ['https://mail.google.com/']
our_email = 'luwang827@gmail.com'

def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.path.join(current_dir, "gmailapicred.json"), SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

service = gmail_authenticate()

def get_email_content_by_title(title):
    try:
        # search for emails with the given title
        query = f'subject:"{title}"'
        result = service.users().messages().list(userId='me', q=query).execute()
        messages = result.get('messages', [])

        if not messages:
            print(f'No emails found with title "{title}"')
            return None

        # retrieve the content of the first email
        message_id = messages[0]['id']
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()

        # extract the text content of the email
        payload = message['payload']
        return get_message_body_in_payload(payload)


    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def get_message_body_in_payload(payload):
    if payload['mimeType'] == 'text/plain' or payload['mimeType'] == 'text/html':
        # Decode the message body from base64 encoding
        message_body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        #print("text body: "+message_body)
        return message_body
    elif 'parts' in payload:
        # Recursively iterate over parts and return the first text/plain or text/html part
        for part in payload['parts']:
            message_body = get_message_body_in_payload(part)
            if message_body:
                #print("parts body: "+message_body)
                return message_body




#################################
#######      2348 Gexa    #######
#################################
#Calculate the email subject
today = datetime.date.today()
last_monday = (today - datetime.timedelta(days=today.weekday()) - datetime.timedelta(weeks=1)).strftime("%m-%d-%Y")
last_sunday = (today - datetime.timedelta(days=today.weekday() + 1)).strftime("%m-%d-%Y")
email_title = "Weekly Electricity Usage From "+ last_monday +" To "+last_sunday

html_conent  = get_email_content_by_title(email_title)
'''
if html_conent:

    # Create an instance of the custom HTML parser class and feed it the HTML content
    parser = HTMLParser_Electricity()
    parser.feed(html_content)

    # Get the usage data
    extracted_data = parser.weekly_usage
    last_week_usage, this_week_usage, last_invoice_usage, project_this_month = extracted_data[0], extracted_data[2], extracted_data[-2], extracted_data[-1]
    print("2348 Usage for week "+last_monday+" is :" + this_week_usage)
    print("Projection to this month is :" + project_this_month)
    print("The usage of last month was :" + last_invoice_usage)
    '''


#######################################
#######      3120 water bill    #######
#######################################
water_bill_subject = "City of Plano Water Statement"
water_bill_content = get_email_content_by_title(water_bill_subject)
bill_parser = HTMLParser_WaterBill3120()
bill_parser.feed(water_bill_content)
print(f'The water bill due for 3120 Golden Springs Dr. at {bill_parser.due_date} is: {bill_parser.current_due}')


#######################################
#######      2348 water bill    #######
#######################################
water_bill_subject = "City of Carrollton Statement is available"
water_bill_content = get_email_content_by_title(water_bill_subject)
bill_parser = HTMLParser_WaterBill2348()
bill_parser.feed(water_bill_content)
if len(bill_parser.table_data) >= 2 and len(bill_parser.table_data[0]) >= 2 and len(bill_parser.table_data[1]) >= 1:
    due_date = bill_parser.table_data[0][1]
    total_amount_due = bill_parser.table_data[2][1]
else:
    print("2348 water bill  data is not complete, check email")
print(f'The water bill due for 2348 Janna Way at {due_date} is: {total_amount_due}')