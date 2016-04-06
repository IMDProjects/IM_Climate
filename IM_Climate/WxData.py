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
        Appends additional weather data to the wxData object
        '''
        self['data']={newData['meta']['uid']: {parameter : tuple(newData['data'])}}

    @property
    def data(self):
        return self['data']


if __name__ == '__main__':

    dateInterval = 'mly'
    aggregation = 'avg'
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
                   u'uid': 3941}}

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
    print (s.stationIDs)
    print (s.getStationData(3941, 'avgt'))
    s.add(moreWxObs, 'mint')
    print (s.getStationData(3941, 'mint'))
