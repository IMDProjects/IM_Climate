import csv
from datetime import date
from ACIS import ACIS



class StationDict(dict):

    '''
    Object containing all station metadata and associated data
    StationDict is composed of the following nested objects:
        Station
            StationData
                ParameterSeries
                    WxOb
    '''
    def __init__(self, climateParameters, queryParameters = None, dateInterval = None, aggregation = None):

        self.dateRequested = date.today().isoformat()
        self.queryParameters = queryParameters
        self.dateInterval = dateInterval
        self.aggregation = aggregation
        self.climateParameters = climateParameters

    def _writeToCSV(self):
        '''
        INFO
        ----
        Writes a 2-dimensional list to a CSV text file
        Comma-delimits values.

        RETURNS
        -------
        None

        '''
        with open(self._filePathAndName,'w') as csvFile:
            writer = csv.writer(csvFile, lineterminator='\n' )
            writer.writerows(self._dataAsList)
        csvFile.close()



    def exportMeta(self, filePathAndName, format='csv'):
        '''
        INFO
        ----
        Method providing option to export station metadata into various formats.
        Currently only supports csv

        ARGUMENTS
        ---------
        filePathAndName - Destination where file is to be saved
        format  = Export format. Default = csv

        RETURNS
        --------
        None
        '''
        self._export(dumpMethod = self._dumpMetaToList, filePathAndName = filePathAndName, format = format)

    def exportData(self, filePathAndName, format='csv'):
        '''
        INFO
        ----
        Method providing option to export station data into various formats.
        Currently only supports csv

        ARGUMENTS
        ---------
        filePathAndName - Destination where file is to be saved
        format  = Export format. Default = csv

        RETURNS
        --------
        None
        '''
        self._export(dumpMethod = self._dumpDataToList, filePathAndName = filePathAndName, format = format)


    def export(self, filePathAndName, format='csv'):
        '''
        INFO
        ----
        This is a "smart" export. If weather data exists for at least one station, then
            then the export is of the weather data (plus limited station metadata fields).
            If only station metadata exists, then export is of the
            station metadata only.

        ARGUMENTS
        ---------
        filePathAndName - Destination where file is to be saved
        format  = Export format. Default = csv

        RETURNS
        --------
        None
        '''
        for station in self:
            try:
                if station.data:
                    self._export(dumpMethod = self._dumpDataToList, filePathAndName = filePathAndName, format = format)
                    return
            except:
                self._export(dumpMethod = self._dumpMetaToList, filePathAndName = filePathAndName, format = format)
                return

    def _export(self, dumpMethod, filePathAndName, format):
        '''
        Generlized method to export station meta or station data to a fille.
        '''
        self._filePathAndName = filePathAndName
        dumpMethod()
        self._writeToCSV()

    def _dumpMetaToList(self):
        '''
        INFO
        ----
        Re-formats the station information to a list

        RETURNS
        --------
        None
        '''
        tags = self[self.stationIDs[0]]._tags
        self._dataAsList = [tags]
        for station in self:
            #info = [station.__dict__[t] for t in tags]
            self._dataAsList.append(station._dumpToList())
        return self._dataAsList


    def _dumpDataToList(self):
        '''
        INFO
        ----
        Dumps station data to a very flat list/matrix

        NOTE:
        ----
        Method currently assumes that each station has the same set of parameters
        for the same date range.
        '''
        acis = ACIS()
        self._dataAsList = None
        try:
            self.stationIDs
        except:
            self._dataAsList = 'NO DATA'
            return

        #Create header row
        header = ['uid','longitude', 'latitude', 'sid1', 'sid2','sid3', 'state', 'elev', 'name', 'date']
        for p in self.climateParameters:
            header.extend([acis.supportedParameters[p]['label'], p+'_acis_flag', p+'_source_flag'])

        self._dataAsList = [header]
        for station in self:
            lat = station.latitude
            lon = station.longitude
            name = station.name
            elev = station.elev
            sid1 = station.sid1
            sid2 = station.sid2
            sid3 = station.sid3
            state = station.state
            for date in station.data.observationDates:
                a = [str(station.uid), lon, lat, sid1, sid2, sid3, state,  elev, name, date]
                for param in self.climateParameters:
                    a.extend([station.data[param][date].wxOb, station.data[param][date].ACIS_Flag, station.data[param][date].sourceFlag])
                self._dataAsList.append(a)
        return self._dataAsList



    def _addStation(self, stationSubClass, stationID, stationMeta, stationData = None):
        '''
        Hidden method to add a station to the StationDict object.
        '''
        self[stationID] = stationSubClass(stationMeta = stationMeta, climateParameters = self.climateParameters, stationData = stationData)

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
        a = self._dumpMetaToList()
        a = map(str,a)
        return '\n'.join(a)


if __name__ == '__main__':
    from ACIS_Station import ACIS_Station
    climateParams = ['mint']
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
    sl = StationDict(queryParameters = queryParams, climateParameters =  climateParams)
    for s in stations['meta']:
        sl._addStation(stationSubClass = ACIS_Station, stationID = s['uid'],  stationMeta =  s)
    print(sl.stationIDs)
    print(sl.stationNames)
    print(sl.queryParameters)
    sl.export(r'C:\TEMP\test2.csv')
    for station in sl:
        print station.latitude
    print sl[77459].name
    print sl

    #################################

    climateParams = ['mint', 'maxt']
    queryParameters = {'query':'params'}
    dateInterval = 'mly'
    aggregation = 'avg'

    #Station #1
    wxObs = {u'data': [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
           [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
           [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]],
 u'meta': {u'elev': 9600.1,
           u'll': [-105.9864, 39.56],
           u'name': u'SODA CREEK COLORADO',
           u'sids': [u'USR0000CSOD 6'],
           u'uid': 66180}}

    #Station #2,
    moreWxObs = {u'data': [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
           [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
           [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]],
 u'meta': {u'elev': 9600.1,
           u'll': [-105.9864, 39.56],
           u'name': u'ILL CREEK COLORADO',
           u'sids': [u'USR0000CSOD 6'],
           u'uid': 1233}}

    wx = StationDict(queryParameters = queryParameters, dateInterval = 'mly', aggregation = 'avg', climateParameters = ['mint','maxt'])
    wx._addStation(stationSubClass= ACIS_Station, stationID = wxObs['meta']['uid'],  stationMeta =  wxObs['meta'], stationData = wxObs['data'])
    wx._addStation(stationSubClass = ACIS_Station, stationID = wxObs['meta']['uid'], stationMeta =  moreWxObs['meta'], stationData =  moreWxObs['data'])
    print wx._dumpDataToList()
    print wx.climateParameters
    print wx.stationIDs
    wx.export(filePathAndName = r'test.csv')
    print wx

    #StationDict is indexable
    print wx[66180].data['maxt']['2012-01-01'].wxOb

    #Iterate through each station, parameter and weather observation
    for station in wx:
        for p in station.data:
            print p
            for ob in p:
                print ob
    print wx.stationNames
