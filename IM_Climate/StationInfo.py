import json
try:    #python 2.x
    from dataObjects import dataObjects
except: #python 3.x
    from .dataObjects import dataObjects

class StationInfo(dataObjects):
    def __init__(self, info, *args, **kwargs):
        super(StationInfo, self).__init__(info, **kwargs)
        self['data'] = self['meta'] #swap keys
        self['meta'] = {} #clear out the existing meta key
        self._addStandardMetadataElements()

    @property
    def stationIDs(self):
        '''
        Returns a list of all station IDs
        '''
        return [z['uid'] for z in self['data']]

    @property
    def stationNames(self):
        '''
        Returns a list of all station IDs
        '''
        return [str(z['name']) for z in self['data']]


    def match(self, string):
        '''Matches provided string to full station metadata.
            Returns list of matched station metadata'''
        matches = []
        for meta in self['data']:
            if str(meta).lower().find(string.lower()) >= 0:
                matches.append(meta)
        return matches

    def getStationMetadata(self, stationID):
        '''
        Returns all station metadata
        '''
        for station in self['data']:
            if stationID == station['uid']:
                return station

    def toGeoJSON(self):

        '''
        Provides a list of stations in GeoJSON format
        '''
        ##        {
        ##	"type": "FeatureCollection",
        ##	"geometries": [{
        ##		"type": "Feature",
        ##		"id": "<StationID>",
        ##		"properties": {
        ##			"UnitCode": "<UnitCode>",
        ##			"StationCode": "<StationCode>",
        ##			"stationName": "<StationName>",
        ##			"SourceName": "<SourceName>"
        ##		},
        ##		"geometry": {
        ##			"type": "Point",
        ##			"coordinates": [Longitude_deg,
        ##			Latitude_deg]
        ##		}
        ##	}]
        ##}
        geometeries= []
        for station in self.stationIDs:
            stationMetadata = self.getStationMetadata(stationID = station)
            st = {'type':'Feature', 'id':station, 'properties':stationMetadata,
                    'geometry': {'type': 'point',
                    'coordinates': [[stationMetadata['ll'][0]],stationMetadata['ll'][1]] }}
            geometeries.append(st)
        data = {
        	"type": "FeatureCollection",
        	"geometries": geometeries}
        return json.dumps(data)

if __name__ == '__main__':
    stations =  {u'meta': [{u'elev': 10549.9,
            u'll': [-106.17, 39.49],
            u'name': u'Copper Mountain',
            u'valid_daterange': [[u'1983-01-12', u'2016-04-05']],
            u'sids': [u'USS0006K24S 6'],
            u'state': u'CO',
            u'uid': 67175},
           {u'elev': 10520.0,
            u'll': [-106.42, 39.86],
            u'name': u'Elliot Ridge',
            u'valid_daterange': [[u'1983-01-12', u'2016-04-05']],
            u'sids': [u'USS0006K29S 6'],
            u'state': u'CO',
            u'uid': 77459}]}
    queryParams = {'Example':'Example'}
    s = StationInfo(stations, queryParams = queryParams)
##    print(s.stationIDs)
##    print(s.stationNames)
##    print(s.toJSON())
##    print(s.metadata)
##    print s.match('ell')
##    print(s.getStationMetadata(stationID = 67175))
    print s.toGeoJSON()