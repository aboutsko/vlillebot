import requests
import json
import os

class CannotSendResponseError(Exception):
	pass

ENDPOINT = 'https://api.telegram.org/'
TOKEN = os.getenv('TOKEN')
URI = ENDPOINT + TOKEN

def send_message(update, message):
	try:
		response_id = update['message']['chat']['id']
		requests.post('{}/sendMessage'.format(URI),
						  data={
							  'chat_id': response_id,
							  'text': message
						  })
	except:
		raise CannotSendResponseError


def send_location(update, lat, lng):
	try:
		response_id = update['message']['chat']['id']
		requests.post('{}/sendLocation'.format(URI),
						  data={
							  'latitude': lat,
							  'longitude': lng,
							  'chat_id': response_id
						  })
	except:
		raise CannotSendResponseError

def get_updates(offset):
	return requests.get('{}/getUpdates?offset={}'.format(URI, offset)).json()
