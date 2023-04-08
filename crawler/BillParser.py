from base64 import urlsafe_b64decode, urlsafe_b64encode
import os
import pickle
from html.parser import HTMLParser
import re
import datetime
import base64


# Gexa Parser
class HTMLParser_Electricity(HTMLParser):
    # Define a variable to hold the weekly usage value
    weekly_usage = []
    
    def handle_data(self, data):
        # Search for the string "kWh" and extract the number before it
        match = re.search(r'(\d+)\s*kWh', data)
        if match:
            self.weekly_usage.append(match.group(1))

#WaterBill Parser 3120
class HTMLParser_WaterBill3120(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_due = None
        self._current_tag = None
        self.due_date = None

    def handle_starttag(self, tag, attr):
        self._current_tag = tag

    def handle_data(self, data):
        if self._current_tag == 'br' and re.search(r"Current Due:\s*([-+]?\d+(\.\d+)?)", data.strip()) :
            self.current_due = re.search(r"Current Due:\s*([-+]?\d+(\.\d+)?)", data.strip()).group(1)
        if self._current_tag == 'br' and re.search(r"Due Date:\s+(\d{2}/\d{2}/\d{2})", data.strip()) :
            self.due_date = re.search(r"Due Date:\s+(\d{2}/\d{2}/\d{2})", data.strip()).group(1)

#WaterBill Parser 2348
class HTMLParser_WaterBill2348(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_table = False
        self.in_row = False
        self.in_column = False
        self.table_data = []
        self.total_amount_due = None
        self.due_date = None

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        elif tag == 'tr':
            self.in_row = True
            self.current_row = []
        elif tag == 'td':
            self.in_column = True

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
        elif tag == 'tr':
            self.in_row = False
            self.table_data.append(self.current_row)
        elif tag == 'td':
            self.in_column = False

    def handle_data(self, data):
        if self.in_column:
            self.current_row.append(data.strip())