import urllib2, urllib
import json

#http://synopticlabs.org/api/mesonet/reference/
#MESO WEST DOES NOT TRACK DATA PRIOR TO 199701010000


keyfile = open('mesowest_key.txt')
key = keyfile.read()
##class Mesowest(object):
##    def __init__(self):
##        super(Mesowest,self).__init__()
##        self._input_dict = {}
##        self.webServiceSource = None

t = urllib.urlopen('http://api.mesowest.net/v2/auth?apikey='+key)
token = json.loads(t.read())
token = token['TOKEN']
#url = 'http://api.mesowest.net/v2/stations/metadata?&county=larimer&state=co&status=active&token=' + token #Station metadata for those in larimer Count
url =  'http://api.mesowest.net/v2/stations/timeseries?&stid=RFRC2&start=200601010000&end=200601031215&token=' + token             #STID = KFNL for Fort Collins

connection = urllib.urlopen(url)
data =  json.loads(connection.read())
print data.keys()
print data['SUMMARY']
#print data['UNITS']
print data['STATION']

##if __name__ == '__main__':
##    m = Mesowest()
##    m