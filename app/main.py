import os
from app import server
import requests
from collections import namedtuple
import json
import math
import flask
import pickle
import time

from .vlille import parse, get_details, format_details
from .utils import get_last_update, set_last_update
from .telegram import get_updates, send_location, send_message



USAGE = '''Envoyez-moi votre localisation pour trouver le v\'lille le plus proche de vous!'''

def run():
	last_update = get_last_update()
	while True:
		# FETCH
		try:
			print('fetching ...')
			updates = get_updates(str(last_update))
		except Exception as error:
			print(error)
			continue

		# LOOP
		for update in updates['result']:
			if update['update_id'] <= last_update:
				continue

			last_update = update['update_id']
			set_last_update(update['update_id'])
			print('got update {}'.format(update['update_id']))
			if 'location' not in update['message']:
				try:
					send_message(update, USAGE)
				except CannotSendResponseError:
					continue
			else:
				location = update['message']['location']
				min_distance = None
				closest = None

				for identifier, s in stations.items():
					distance = math.hypot(location['latitude'] - s['lat'],
						  				  location['longitude'] - s['lng'])
					if not closest or distance <= min_distance:
						details = get_details(identifier)
						if int(details['bikes']) == 0:
							continue
						print('identifying {}'.format(identifier))
						print('station {}'.format(s))
						closest = identifier
						closest_details = details
						min_distance = distance

				try:
					send_message(update, format_details(closest_details))
					send_location(update, stations[closest]['lat'], stations[closest]['lng'])
				except CannotSendResponseError:
					continue

		time.sleep(5)


parse()
from .vlille import stations