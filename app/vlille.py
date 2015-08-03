import xml.etree.ElementTree as ET
import requests

stations = {}

def parse():
	e = ET.parse('xml-stations.aspx').getroot()
	for marker in e.findall('marker'):
		station = { 
			'name': marker.get('name'),
			'lat': float(marker.get('lat')),
			'lng': float(marker.get('lng'))
		}
		stations[int(marker.get('id'))] = station
	print(stations)

def get_details(id):
	r = requests.get('http://vlille.fr/stations/xml-station.aspx?borne={}'.format(id))
	station = ET.fromstring(r.text)	
	return  {
		'adress': station.find('adress').text,
		'status': station.find('status').text,
		'bikes': station.find('bikes').text,
		'attachs': station.find('attachs').text,
		'paiement': station.find('paiement').text,
		'lastupd': station.find('lastupd').text
	}

def format_details(details):
	return 'Vous trouverez {} vélos sur {} attaches à {} (dernière mise à jour: {})'.format(details['bikes'],
																							int(details['attachs']) + int(details['bikes']),
																							details['adress'],
																							details['lastupd'])
																							
