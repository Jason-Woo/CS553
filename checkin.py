class Checkin(object):

	def __init__(self,user,location_id,checkin_time,longitude=0,latitude=0):
		self.user = user
		self.location_id = location_id
		self.checkin_time = checkin_time
		self.longitude = longitude
		self.latitude = latitude