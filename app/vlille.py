import xml.etree.ElementTree as ET
import requests

class StationDetail(object):
	'''
	Holds details of a station
	'''
	def __init__(self, id, adress, status, bikes, attachs, paiement, lastupd):
		self.id = id
		self.adress = adress
		self.status = status
		self.bikes = int(bikes)
		self.attachs = int(attachs)
		self.total = self.bikes + self.attachs
		self.paiement = paiement
		self.lastupd = lastupd
	
	def __str__(self):
		return '''Vous trouverez
				   {} vélos pour
				   {} attaches au
				   {} (dernière mise à jour: {})'''.format(self.bikes,
														   self.total,
														   self.adress,
														   self.lastupd)


class Station(object):
	'''
	Holds global information of a station
	'''
	def __init__(self, id, name, latitude, longitude):
		self.id = id
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
		
	def get_details(self):
		'''
		Fetches details on one vlille station, returning a dict with details
		Returns:
			(StationDetail): the details of the station
		'''
		r = requests.get('http://vlille.fr/stations/xml-station.aspx?borne={}'.format(self.id))
		station = ET.fromstring(r.text)
		return StationDetail(self.id,
							 station.find('adress').text,
							 station.find('status').text,
							 station.find('bikes').text,
							 station.find('attachs').text,
							 station.find('paiement').text,
							 station.find('lastupd').text)
																							

class Vlille(object):
	'''
	Class used to access vlille data
	'''
	stations_path = 'xml-stations.aspx'
	stations = {}
	
	@classmethod
	def parse(cls):
		'''
		Called to parse a local file containing the definition of all vlille (location and id)
		'''
		e = ET.parse(cls.stations_path).getroot()
		for marker in e.findall('marker'):
			station = Station(int(marker.get('id')),
							  marker.get('name'),
							  float(marker.get('lat')),
							  float(marker.get('lng')))
			cls.stations[station.id] = station
