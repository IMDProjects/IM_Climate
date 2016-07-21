import csv
from datetime import date

from Station import Station



class StationDict(dict):
    def __init__(self, data = None, queryParameters = None):
        self.dateRequested = date.today().isoformat()
        if queryParameters:
            self.queryParameters = queryParameters
        if data:
            for x in range(0,len(data['meta'])):
                self._addStation(data['meta'][x])

    def _writeToCSV(self):
        '''
        INFO
        ----
        Writes a 2-dimensional list to a CSV text file
        Comma-delimits values.

        ARGUMENTS
        ---------
        filePathAndName - file name and path
        dataAsList - 2-dimensional list

        RETURNS
        -------
        None

        '''
        with open(self._filePathAndName,'w') as csvFile:
            writer = csv.writer(csvFile, lineterminator='\n' )
            writer.writerows(self._dataAsList)
        csvFile.close()


    def export(self, filePathAndName, format='csv'):
        '''
        INFO
        ----
        Method providing option to export data into various formats

        ARGUMENTS
        ---------
        filePathAndName - Destination where file is to be saved
        format  = Export format. Default = csv


        RETURNS
        --------
        None
        '''
        self._filePathAndName = filePathAndName
        if format == 'csv':
            self._dumpToList()
            self._writeToCSV()


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
        tags = ['name', 'latitude', 'longitude', 'sid1', 'sid2','sid3', 'stateCode', 'elev', 'uid']
        self._dataAsList = []

        self._dataAsList.append(tags)
        for station in self:
            info = [station.__dict__[t] for t in tags]
            self._dataAsList.append(info)
        return self._dataAsList

    def _addStation(self, info):
        self[info['uid']] = Station(info)

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

    def __repr__(self):
        '''
        Pretty formatting of the StationDict object
        '''
        a = self._dumpToList()
        a = map(str,a)
        return '\n'.join(a)


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
    print sl


