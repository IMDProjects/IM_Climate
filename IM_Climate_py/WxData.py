try:    #python 2.x
    from dataObjects import dataObjects
except: #python 3.x
    from .dataObjects import dataObjects

class WxData(dataObjects):
    def __init__(self, dateInterval, aggregation, data = None, *args, **kwargs):
        '''
        Data object that holds and organizes all weather data returned by ACIS
        using the StnData request.

        This object differs from the ACIS data structure

        Meta: {dateInterval, Aggregation, PeriodOfRecord, DateRequested}
        Data: Station:Parameter:({date,value,flags}
        '''

        self['meta'] = {}
        self['data'] = {}
        self['meta']['dateInterval'] = dateInterval
        self['meta']['aggregation'] = aggregation
        super(WxData, self).__init__(*args, **kwargs)
        self._addStandardMetadataElements()

    @property
    def stationIDs(self):
        '''
        List of all stationIDs within dataset
        '''
        return self['data'].keys()

    def getStationData(self, stationID, parameter):
        '''
        Returns time series of data for a specied station and parameter
        '''
        return self['data'][stationID][parameter]

    @property
    def dateInterval(self):
        return self.metadata['dateInterval']

    @property
    def startDate (self):
        return self.metadata['startDate']

    @property
    def endDate (self):
        return self.metadata['endDate']

    def add(self, newData, parameter):
        '''
        Appends additional weather data to the wxData object unless there is an
        'error' tag. In that case, no data is appended for the
        '''


        #Duck Type - check is parameter dictionary exists
        #If not, then add the parameter dictionary in exception
        try:
            self['data'][newData['meta']['uid']].keys()
        except:
            self['data'][newData['meta']['uid']]={}

        #return if there isn't any data to append
        if newData.get('error'):
            self['data'][newData['meta']['uid']][parameter] = None
        else:
            self['data'][newData['meta']['uid']][parameter] = tuple(newData['data'])


    @property
    def data(self):
        return self['data']

    def getStationParameters(self, stationID):
        return self['data'][stationID].keys()

    def toCSV(self, filePathAndName):
        '''
        INFO
        ----
        Writes a comm-adelimited text file
        '''
        super(WxData,self).toCSV(filePathAndName)
        for station in self.stationIDs:
            for parameter in self.getStationParameters(station):
                for data in self.getStationData(stationID = station, parameter = parameter):
                    self.outFile.writelines(str(station) + self._sp + parameter
                        + self._sp + self._sp.join(data) + '\n')
        self.outFile.close()

    @property
    def dateInterval(self):
        return self['meta']['dateInterval']

    @property
    def aggregation(self):
        return self['meta']['aggregation']



if __name__ == '__main__':

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

    s = WxData(dateInterval = 'mly', aggregation = 'avg')
    s.add(wxObs, 'avgt')
    print s
    print (s.keys())
    print (s.toJSON())
    print (s.metadata)
    print (s.getStationData(3940, 'avgt'))
    s.add(moreWxObs, 'mint')
    s.add(moreWxObs, 'Maxt')
    print (s.getStationData(3941, 'mint'))
    print (s.stationIDs)
    s.toCSV(filePathAndName = r'test.csv')
