import json
import re
from dateutil.parser import parse

credit_regex = 'credit card'
exclude_regex = 'statement|declined|received|credited|stmt|otp|debit'

last_digits_regex = '(?:ending\s|(?:x*))*(\d{4})'

rupees_regex = '(?:rs\.?|inr)\s*(\d+(?:[.,]\d+)*)'

date_regex = '(\d{4}-\d{2}-\d{2})|(\d{2}/\d{2}/\d{2})'

time_regex = '(?:\s|:)(\d{2}:\d{2}:\d{2})'

def timestamp_parse(text):

	date = re.search(date_regex, text)

	if date is None:
		return None

	date = date.group()

	time = re.search(time_regex, text)

	if not time is None:
		datetime = date + ' ' + time.group(1)
		strftime = '%d-%b-%Y %H:%M%p'
	else:
		datetime = date
		strftime = '%d-%b-%Y'

	if '/' in datetime:
		dayfirst = True
	else:
		dayfirst = False

	datetime = parse(datetime,dayfirst=dayfirst).strftime(strftime)

	return datetime

def parse_json_msg(msg_dict):

	valid_msgs = []

	for message in msg_dict:

		data_map = {}

		text = message['text'].lower()

		if not re.search(credit_regex, text):
			continue

		if 	re.search(exclude_regex, text):
			continue

		amount = re.search(rupees_regex, text)

		if amount is None:
			continue

		amount = amount.group(1)

		data_map['amount'] = amount

		last_digits = re.search(last_digits_regex, text).group(1)

		if last_digits is None:
			continue

		last_digits = 'xxxx' + last_digits

		data_map['last_digits'] = last_digits

		transaction_time = timestamp_parse(text)

		data_map['transaction_time'] = transaction_time

		data_map['number'] = message['number']
		data_map['sms_timestamp'] = parse(message['datetime']).strftime('%d-%b-%Y %H:%M%p')
		data_map['timestamp'] = message['timestamp']

		sender = message['number']

		if '-' in sender:
			sender = sender.split('-')[1]

		data_map['sender'] = sender

		valid_msgs.append(data_map)

	valid_msgs = sorted(valid_msgs, key=lambda k: k['timestamp'],reverse=True)

	return valid_msgs
