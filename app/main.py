import os
import time
import requests
import math

from .vlille import Vlille, StationDetail
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
				closest_id = None
				
				for identifier, station in Vlille.stations.items():
					distance = math.hypot(location['latitude'] - station.latitude,
						  				  location['longitude'] - station.longitude)
					if not closest_id or distance <= min_distance:
						print('got closest {}'.format(distance))
						details = station.get_details()
						if details.bikes == 0:
							continue
						closest_id = identifier
						closest_station = station
						closest_details = details
						min_distance = distance

				try:
					send_message(update, str(closest_details))
					send_location(update, closest_station.latitude, closest_station.longitude)
				except CannotSendResponseError:
					continue

		time.sleep(0.5)


Vlille.parse()