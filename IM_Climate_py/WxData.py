try:    #python 2.x
    from dataObjects import dataObjects
    from RequestMetadata import RequestMetadata
except: #python 3.x
    from .dataObjects import dataObjects

class WxData(dict, dataObjects):
    def __init__(self, queryParameters, dateInterval, aggregation, data = None, *args, **kwargs):
        '''
        Data object that holds and organizes all weather data returned by ACIS
        using the StnData request.

        This object differs from the ACIS data structure

        Meta: {dateInterval, Aggregation, PeriodOfRecord, DateRequested}
        Data: Station:Parameter:({date,value,flags}
        '''
        self.metadata = RequestMetadata(queryParameters, dateInterval = dateInterval
            ,aggregation = aggregation)
        if data:
            self.add(data)

    @property
    def stationIDs(self):
        '''
        List of all stationIDs within dataset
        '''
        return self.keys()

    def getStationData(self, stationID, parameter):
        '''
        Returns time series of data for a specied station and parameter
        '''
        return self[stationID][parameter]

    def add(self, newData, parameter):
        '''
        Appends additional weather data to the wxData object unless there is an
        'error' tag. In that case, no data is appended for the
        '''
        #Duck Type - check is parameter dictionary exists
        #If not, then add the parameter dictionary in exception
        try:
            self[newData['meta']['uid']].keys()
        except:
            self[newData['meta']['uid']]={}

        #return if there isn't any data to append
        if newData.get('error'):
            self[newData['meta']['uid']][parameter] = None
        else:
            self[newData['meta']['uid']][parameter] = tuple(newData['data'])

    def getStationParameters(self, stationID):
        return self[stationID].keys()

    def _dumpToList(self):
        '''
        INFO
        ----
        Dumps all info to a list
        '''
        self._dataAsList = []
        for station in self.stationIDs:
            for parameter in self.getStationParameters(station):
                for data in self[station][parameter]:
                    self._dataAsList.append([str(station), parameter, str(data)])

if __name__ == '__main__':
    queryParameters = {'elk':'moose'}
    dateInterval = 'mly'
    aggregation = 'avg'

    #Station #1
    wxObs = {u'data': [[u'1980-01', u'30.92'],
           [u'1980-02', u'35.78'],
           [u'1980-03', u'39.16'],
           [u'1980-04', u'50.30'],
           [u'1980-05', u'57.19'],
           [u'1980-06', u'68.95']],
         u'meta': {u'elev': 5092.0,
                   u'll': [-108.05, 39.45],
                   u'name': u'GRAND VALLEY',
                   u'sids': [u'053508 2', u'USC00053508 6'],
                   u'state': u'CO',
                   u'uid': 3940}}
    #Station #2,
    moreWxObs = {u'data': [[u'1980-01', u'30.92'],
           [u'1980-02', u'35.78'],
           [u'1980-03', u'39.16'],
           [u'1980-04', u'50.30'],
           [u'1980-05', u'57.19'],
           [u'1980-06', u'68.95']],
         u'meta': {u'elev': 5092.0,
                   u'll': [-108.05, 39.45],
                   u'name': u'GRAND VALLEY',
                   u'sids': [u'053508 2', u'USC00053508 6'],
                   u'state': u'CO',
                   u'uid': 3941}}

    s = WxData(queryParameters,dateInterval = 'mly', aggregation = 'avg')
    s.add(wxObs, 'avgt')
    print s
    print (s.keys())
    print (s.metadata.queryParameters)
    print (s.getStationData(3940, 'avgt'))
    s.add(moreWxObs, 'mint')
    s.add(moreWxObs, 'Maxt')
    print (s.getStationData(3941, 'mint'))
    print (s.stationIDs)
    print (s.metadata.dateInterval)
    print (s.metadata.aggregation)
    s.export(filePathAndName = r'C:\TEST\test.csv')
