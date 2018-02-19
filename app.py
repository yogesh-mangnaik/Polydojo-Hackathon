from email.mime.multipart import MIMEMultipart
from email.mime.text      	import MIMEText
from email.mime.base      	import MIMEBase
from email             		import encoders
import csv
import smtplib
import argparse
import io
from credentials import SENDER_EMAIL, SENDER_PASSWORD
from datetime import datetime

def processMail(details):
	YES_TEMPLATE = """
	Greetings {},

	Your railyway-concession form has been approved on {}.
	You can collect it from the railway concession office at the accouting department.
	""" 

	NO_TEMPLATE = """
	Sorry {}, 

	Your request for railway pass concession has been disapproved.
	Please contact the Admin for further queries.
	"""

	smtp = smtplib.SMTP('smtp.gmail.com')
	smtp.ehlo()
	smtp.starttls()
	smtp.login(SENDER_EMAIL, SENDER_PASSWORD)


	name = details['name']
	date = f"{datetime.now():%d-%m-%Y}"
	subject = 'Railyway Concession'
	if details['status'] == 'Yes':
		content = YES_TEMPLATE.format(name, date)
	else:
		content = NO_TEMPLATE.format(name)
	toEmail = details['email']

	msg = MIMEMultipart()
	msg['From'] = SENDER_EMAIL
	msg['To'] = toEmail
	msg['Subject'] = subject
	body = content
	msg.attach(MIMEText(body, 'plain'))

	email_content = msg.as_string()
	smtp.sendmail(SENDER_EMAIL, toEmail, email_content)
