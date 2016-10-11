import csv
from datetime import date
import common
from Station import DailyStation
from Station import MonthlyStation

class DailyStationDict(dict):

    '''
    Object containing all station metadata and associated data
    StationDict is composed of the following nested objects:
        Station (or derivative subclass)
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
        self._dataTags = ['uid', 'name', 'longitude', 'latitude', 'sid1', 'sid1_type',
            'sid2', 'sid2_type', 'sid3', 'sid3_type', 'state',
            'elev'] #station metadata to include with data export
        self.StationClass = DailyStation

    def _writeToCSV(self):
        '''
        INFO
        ----
        Writes a 2-dimensional list to a CSV text file
        Comma-delimits values.  If there is no data, then there is no attempt to
        creat a file.

        RETURNS
        -------
        None

        '''
        if self._dataAsList:
            with open(self._filePathAndName,'w') as csvFile:
                writer = csv.writer(csvFile, lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC )
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

    @property
    def wxDataExists(self):
        '''
        Confirms whether there is wxData for at least one station in the dictionary object
        True - Yes
        False - No
        '''
        for station in self:
            try:
                if station.data:
                    return True
            except:
                pass
        return False

    @property
    def stationCounts(self):
        '''
        Summarizes the count of stations with metadata and those with data
        '''
        dCount = 0
        for station in self:
            if station.hasWxData:
                    dCount+=1
        return {'AllStations': len(self.stationIDs), 'StationsWithData': dCount}

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
        if self.wxDataExists:
            self._export(dumpMethod = self._dumpDataToList, filePathAndName = filePathAndName, format = format)
        else:
            self._export(dumpMethod = self._dumpMetaToList, filePathAndName = filePathAndName, format = format)

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
        tags = self[self.stationIDs[0]]._metaTags
        self._dataAsList = [tags]
        for station in self:
            self._dataAsList.append(station._dumpMetaToList())
        return self._dataAsList


    def _dumpDataToList(self):
        '''
        INFO
        ----
        Dumps daily station data to a very flat list/matrix

        NOTE:
        ----
        Method currently assumes that each station has the same set of parameters
        for the same date range.
        '''

        self._dataAsList = None
        try:
            self.stationIDs
        except:
            self._dataAsList = None
            return

        #Create header row
        header = self._dataTags
        header.extend(['date'])

        for p in self.climateParameters:
            header.extend([common.getSupportedParameters()[p]['label'], p+'_acis_flag', p+'_source_flag'])

        self._dataAsList = [header]
        for station in self:
            if station.hasWxData:
                for date in station.data.observationDates:
                    a = [station.uid, station.name, station.longitude, station.latitude,
                         station.sid1, station.sid1_type, station.sid2,
                         station.sid2_type, station.sid3, station.sid3_type,
                         station.state,  station.elev, date]
                    for param in self.climateParameters:
                        a.extend([station.data[param][date].wxOb, station.data[param][date].ACIS_Flag, station.data[param][date].sourceFlag])
                    self._dataAsList.append(a)
        return self._dataAsList



    def _addStation(self, stationID, stationMeta, stationData = None):
        '''
        Method to add a station to the StationDict object.
        '''
        self[stationID] = self.StationClass()
        self[stationID]._set(stationMeta = stationMeta, climateParameters = self.climateParameters, stationData = stationData)

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

    def __str__(self):
        '''
        Pretty formatting of the StationDict object
        '''
        if self.wxDataExists:
            a = self._dumpDataToList()
            a = map(str,a)
        else:
            a = self._dumpMetaToList()
            a = map(str,a)
        return '\n'.join(a)

class MonthlyStationDict(DailyStationDict):
    def __init__(self, *args, **kwargs):
        super(MonthlyStationDict,self).__init__(*args, **kwargs)
        self.StationClass = MonthlyStation

    def _dumpDataToList(self):
        self._dataAsList = None

        #dump data to list only if there are station IDs. If no data, then just exit
        try:
            self.stationIDs
        except:
            return

        #Create header row
        header = self._dataTags[:] #set header to copy of _dataTags values
        header.extend(['date'])

        for p in self.climateParameters:
            header.extend([common.getSupportedParameters()[p[0:p.find('_')]]['label'] + p[p.find('_'):], p+'_CountMissing'])

        self._dataAsList = [header]
        for station in self:
            if station.hasWxData:
                for date in station.data.observationDates:
                    a = [station.uid, station.name, station.longitude, station.latitude,
                         station.sid1, station.sid1_type, station.sid2,
                         station.sid2_type, station.sid3, station.sid3_type,
                         station.state,  station.elev, date]
                    for param in self.climateParameters:
                        a.extend([station.data[param][date].wxOb, station.data[param][date].countMissing, ])
                    self._dataAsList.append(a)
        return self._dataAsList



if __name__ == '__main__':
##    climateParams = ['mint']
##    stations =  {'meta': [{'elev': 10549.9,
##            'll': [-106.17, 39.49],
##            'name': 'Copper Mountain',
##            'valid_daterange': [['1983-01-12', '2016-04-05']],
##            'sids': ['USS0006K24S 6'],
##            'state': 'CO',
##            'uid': 67175},
##           {'elev': 10520.0,
##            'll': [-106.42, 39.86],
##            'name': 'Elliot Ridge',
##            'valid_daterange': [['1983-01-12', '2016-04-05']],
##            'sids': ['USS0006K29S 6'],
##            'state': 'CO',
##            'uid': 77459}]}
##    queryParams = {'Example':'ExampleData'}
##    sl = DailyStationDict(queryParameters = queryParams, climateParameters =  climateParams)
##    for s in stations['meta']:
##        sl._addStation(stationID = s['uid'],  stationMeta =  s)
##    print(sl.stationIDs)
##    print(sl.stationNames)
##    print(sl.queryParameters)
##    sl.export(r'C:\TEMP\test2.csv')
##    for station in sl:
##        print station.latitude
##    print sl[77459].name
##    print sl
##
##    #################################
##
##    climateParams = ['mint', 'maxt']
##    queryParameters = {'query':'params'}
##    dateInterval = 'mly'
##    aggregation = 'avg'
##
##    #Station #1
##    wxObs = {u'data': [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
##           [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
##           [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
##           [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
##           [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]],
## u'meta': {u'elev': 9600.1,
##           u'll': [-105.9864, 39.56],
##           u'name': u'SODA CREEK COLORADO',
##           u'sids': [u'USR0000CSOD 6'],
##           u'uid': 66180}}
##
##    #Station #2,
##    moreWxObs = {u'data': [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
##           [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
##           [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
##           [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
##           [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]],
## u'meta': {u'elev': 9600.1,
##           u'll': [-105.9864, 39.56],
##           u'name': u'ILL CREEK COLORADO',
##           u'sids': [u'USR0000CSOD 6'],
##           u'uid': 1233}}
##
##    wx = DailyStationDict(queryParameters = queryParameters, dateInterval = 'mly', aggregation = 'avg', climateParameters = ['mint','maxt'])
##    wx._addStation(stationID = wxObs['meta']['uid'],  stationMeta =  wxObs['meta'], stationData = wxObs['data'])
##    wx._addStation(stationID = wxObs['meta']['uid'], stationMeta =  moreWxObs['meta'], stationData =  moreWxObs['data'])
##    print wx._dumpDataToList()
##    print wx.climateParameters
##    print wx.stationIDs
##    wx.export(filePathAndName = r'test.csv')
##    print wx
##
##    #StationDict is indexable
##    print wx[66180].data['maxt']['2012-01-01'].wxOb
##
##    #Iterate through each station, parameter and weather observation
##    for station in wx:
##        for p in station.data:
##            print p
##            for ob in p:
##                print ob
##    print wx.stationNames
##    print wx.stationCounts

    #Monthly Station Dict
    climateParams = 'avgt, mint'
    queryParameters = {'query':'params'}
    dateInterval = 'mly'
    aggregation = 'avg'
    reduceCodes = 'mean, max'

    #Station #1
    wxObs = {u'data': [[u'2012-01', [u'22.60', 1], [u'8.7', 2], [u'35.5', 3], [u'25', 4]],
           [u'2012-02', [u'21.52', 5], [u'8.5', 6], [u'32.0', 7], [u'25', 8]],
           [u'2012-03',
            [u'34.60', 0],
            [u'20.1', 0],
            [u'49.0', 0],
            [u'33', 0]],
           [u'2012-04',
            [u'40.20', 0],
            [u'25.9', 0],
            [u'50.5', 0],
            [u'36', 0]],
           [u'2012-05',
            [u'45.40', 0],
            [u'30.5', 0],
            [u'55.5', 0],
            [u'40', 0]]],
 u'meta': {u'elev': 9600.1,
           u'll': [-105.9864, 39.56],
           u'name': u'SODA CREEK COLORADO',
           u'sids': [u'USR0000CSOD 6'],
           u'state': u'CO',
           u'uid': 66180}}
    wx = MonthlyStationDict(queryParameters = queryParameters, dateInterval = 'mly', aggregation = 'avg', climateParameters = ['mint_min','maxt_min', 'mint_max', 'maxt_max'])
    wx._addStation(stationID = wxObs['meta']['uid'],  stationMeta =  wxObs['meta'], stationData = wxObs['data'])
    #print (wx.stationNames)
    print (wx)
    wx.export(r'C:\TEMP\monthlyStationDicTest.csv')
