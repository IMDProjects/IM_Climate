from dataObjects import dataObjects
from Station import Station

class StationDict(dict, dataObjects):
    def __init__(self, ACIS_Data, queryParameters):
        super(StationDict, self).__init__()
        self._tags = ['name', 'latitude', 'longitude', 'sids', 'stateCode', 'elev', 'uid']
        self.queryParameters= queryParameters
        self._setStation(ACIS_Data)
        self.originalData = ACIS_Data

    def _dumpToList(self):
        '''
        INFO
        ----
        Method to format the station to a list

        ARGUMENTS
        ---------
        filePathAndName

        RETURNS
        --------
        None
        '''
        self._dataAsList = []

        self._dataAsList.append(self._tags)
        for station in self:
            info = [station.__dict__[t] for t in self._tags]
            self._dataAsList.append(info)

    def _setStation(self, info):
        '''
        Fills all cases where an attribute is not returned in the JSON file with
        an 'NA'
        '''
        for x in range(0,len(info['meta'])):
            self[info['meta'][x]['uid']] = Station(info['meta'][x])

    @property
    def stationIDs(self):
        '''
        Returns a list of all station IDs
        '''
        return self.keys()

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
        for station in self.keys():
            yield self[station]



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
    sl = StationDict(stations, queryParameters = queryParams)
    #print sl.metadata
    print(sl.stationIDs)
    print(sl.stationNames)
    print(sl.queryParameters)
    sl.export(r'C:\TEMP\test.csv')
    for station in sl:
        print station.latitude
    print sl[77459].name

