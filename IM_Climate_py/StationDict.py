import json
##try:    #python 2.x
from dataObjects import dataObjects
from Station import Station
##except: #python 3.x
##    from .dataObjects import dataObjects

class StationDict(dataObjects):
    def __init__(self, info, *args, **kwargs):
        super(StationDict, self).__init__(info, *args, **kwargs)
        self['data'] = self['meta'] #swap keys
        self['meta'] = {} #clear out the existing meta key

        self._tags = ['name', 'll', 'sids', 'state', 'elev', 'uid']

        self._setStation()
        self._addStandardMetadataElements()
        self._addMetadata(kwargs)


    def _toText(self):
        '''
        INFO
        ----
        Method to format the station list to csv


        ARGUMENTS
        ---------
        filePathAndName

        RETURNS
        --------
        None
        '''
        self._dataAsList = []
        headers = ['name', 'll', 'sids', 'state', 'elev', 'uid']


        self._dataAsList.append(headers)
        for station in self:
            info = [station[t] for t in self._tags]
            self._dataAsList.append(info)

    def _setStation(self):
        '''
        Fills all cases where an attribute is not returned in the JSON file with
        an 'NA'
        '''
        for x in range(0,len(self['data'])):
            self['data'][x] = Station(self['data'][x])

    @property
    def stationIDs(self):
        '''
        Returns a list of all station IDs
        '''
        return [z.uid for z in self]

    @property
    def stationNames(self):
        '''
        Returns a list of all station IDs
        '''
        return [str(z.name) for z in self]


    def __iter__(self):
        '''
        Allows one to iterate over the station list as a dictionary
        '''
        for station in self['data']:
            yield station

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
    queryParams = {'Example':'ExampleData'}
    sl = StationDict(info = stations, queryParams = queryParams)
    print(sl.stationIDs)
    print(sl.stationNames)
    print(sl.metadata)
    #print(sl.getStationMetadata(stationID = 67175))
    sl.export(r'C:\TEMP\test.csv')
    for station in sl:
        print station.latitude
##    print(s.toJSON())

