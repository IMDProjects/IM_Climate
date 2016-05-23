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

        self._tags = ['uid', 'name', 'state', 'elev']

        self._fillNULLs()
        ##self._addStandardMetadataElements()

    def _toText(self):
        '''
        INFO
        ----
        Method to format the station list to csv
        Blank values are converted to 'NA'

        ARGUMENTS
        ---------
        filePathAndName

        RETURNS
        --------
        None
        '''
        self._dataAsList = []
        headers = ['ACIS_StationID', 'StationName', 'StateCode','Elevation_ft']


        self._dataAsList.append(headers)
        for station in self['data']:
            info = [station[t] for t in self._tags]
            self._dataAsList.append(info)

    def _fillNULLs(self):
        '''
        Fills all cases where an attribute is not returned in the JSON file with
        an 'NA'
        '''
        for station in self['data']:
            for t in self._tags:
                try:
                    station[t]
                except:
                    station[t] = 'NA'


##    @property
##    def stationIDs(self):
##        '''
##        Returns a list of all station IDs
##        '''
##        return [z['uid'] for z in self['data']]

##    @property
##    def stationNames(self):
##        '''
##        Returns a list of all station IDs
##        '''
##        return [str(z['name']) for z in self['data']]
##
##
##    def match(self, string):
##        '''Matches provided string to full station metadata.
##            Returns list of matched station metadata'''
##        matches = []
##        for meta in self['data']:
##            if str(meta).lower().find(string.lower()) >= 0:
##                matches.append(meta)
##        return matches

##    def getStationMetadata(self, stationID):
##        '''
##        Returns all station metadata
##        '''
##        for station in self['data']:
##            if stationID == station['uid']:
##                return station

##    def _toGeoJSON(self):
##
##        '''
##        Provides a list of stations in GeoJSON format
##        '''
##
##        geometeries= []
##        for station in self.stationIDs:
##            stationMetadata = self.getStationMetadata(stationID = station)
##            st = {'type':'Feature', 'id':station, 'properties':stationMetadata,
##                    'geometry': {'type': 'Point',
##                    'coordinates': [stationMetadata['ll'][0],stationMetadata['ll'][1]] }}
##            geometeries.append(st)
##        data = {
##        	"type": "FeatureCollection",
##        	"features": geometeries}
##        return json.dumps(data)



if __name__ == '__main__':
    stations =  {'meta': [{'elev': 10549.9,
            'll': [-106.17, 39.49],
            'name': 'Copper Mountain',
            'valid_daterange': [['1983-01-12', '2016-04-05']],
            'sids': ['USS0006K24S 6'],
            'state': 'CO',
            'uid': 67175},
           {'elev': 10520.0,
            'll': [-106.42, 39.86],
            'name': 'Elliot Ridge',
            'valid_daterange': [['1983-01-12', '2016-04-05']],
            'sids': ['USS0006K29S 6'],
            'state': 'CO',
            'uid': 77459}]}
    queryParams = {'Example':'Example'}
    s = StationInfo(stations, queryParams = queryParams)
##    print(s.stationIDs)
##    print(s.stationNames)
##    print(s.toJSON())
##    print(s.metadata)
##    print s.match('ell')
##    print(s.getStationMetadata(stationID = 67175))
    s.export(r'C:\TEMP\test.csv')