try:    #python 2.x
    import StationDict
    reload(StationDict)
    import Station
    reload(Station)
    from StationDict import StationDict
    from Station import Station

except: #python 3.x
    from .dataObjects import dataObjects

class WxData(StationDict):
    def __init__(self, queryParameters, dateInterval, aggregation, wxParameters):
        '''
        Data object that holds and organizes all weather data returned by ACIS
        using the StnData request.

        '''
        super(WxData, self).__init__(queryParameters = queryParameters)
        self.dateInterval = dateInterval
        self.aggregation = aggregation
        self.wxParameters = wxParameters

    def _addStation(self, newData):
        '''
        Adds additional station/weather data to the wxData object unless there is an
        'error' tag. In that case, no data is appended.
        '''
        #Duck Type - check is data dictionary exists
        #If not, then add the data dictionary in exception
        try:
            self[newData['meta']['uid']].keys()
        except:
            self[newData['meta']['uid']]={}

        #If no data, then set to None. Otherwise, add the station data and station metadata
        if newData.get('error'):
            self[newData['meta']['uid']]['data'] = None
        else:
            self[newData['meta']['uid']] = Station(stationMetadata = newData['meta'])
            self[newData['meta']['uid']]._setStationData(
                    stationData = newData['data'], climateParameters = self.wxParameters)


    def _dumpToList(self):
        '''
        INFO
        ----
        Dumps all info to a very flat list/matric

        NOTE:
        ----
        Method currently assumes that each station has the same set of parameters
        for the same date range.
        '''

        try:
            self.stationIDs
        except:
            self._dataAsList = 'NO DATA'
            return

        #Create header row
        header = ['UID','Longitude', 'Latitude', 'Sids1', 'Sids2','Sids3', 'Name', 'Elevation', 'Date']
        for p in self.wxParameters:
            header.extend([p + '_value', p+'_ACISFlag',p+'_SourceFlags'])

        self._dataAsList = [header]
        for station in self:
            lat = station.latitude
            lon = station.longitude
            name = station.name
            elev = station.elev
            sid1 = station.sid1
            sid2 = station.sid2
            sid3 = station.sid3
            for date in station.data.observationDates:
                a = [str(station.uid), lon, lat,sid1,sid2,sid3,name,elev, date]
                for param in self.wxParameters:
                    a.extend([station.data[param][date].wxOb, station.data[param][date].ACIS_Flag, station.data[param][date].sourceFlag])
                    self._dataAsList.append(a)
        return self._dataAsList

if __name__ == '__main__':
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

    s = WxData(queryParameters, dateInterval = 'mly', aggregation = 'avg', wxParameters = ['mint','maxt'])
    s._addStation(wxObs)
    s._addStation(moreWxObs)
    print s.wxParameters
    print s.stationIDs
    s.export(filePathAndName = r'test.csv')
    print s

    #WxData is indexable
    print s[66180].data['maxt']['2012-01-01'].wxOb

    #Iterate through each station, parameter and weather observation
    for station in s:
        for p in station.data:
            print p
            for ob in p:
                print ob
    print s.stationNames
