## TO DO: ADD PERIOD OF RECORD
##IDEAL STRUCTURE
###{Station: {Parameter: [date, value, flags]}}


import datetime
try:
    #python 2.x
    from dataObjects import dataObjects
except:
    #python 3.x
    from .dataObjects import dataObjects

class WxData(dataObjects):
    def __init__(self, data, duration,  *args, **kwargs):
        '''
        Data object that holds and organizes all weather data returned by ACIS
        using the StnData request.

        Meta: {Duration, Aggregation, PeriodOfRecord,DateRequested}
        Data: Station:Parameter:({date,value,flags}
        '''

        self['meta'] = {}   #Wx data return from ACIS does not have a 'meta' section
        if not self.get('data'):
            self['data'] = []
        kwargs['duration'] = duration
        super(WxData, self).__init__(data, *args, **kwargs)
        self._addStandardMetadataElements()

    @property
    def stationIDList(self):
        '''
        List of all stationIDs within dataset
        '''
        return [k['meta']['uid'] for k in self['data']]

    def getStationData(self, stationID):
        '''
        Returns time series of data for a specied station
        '''
        for d in self['data']:
            if d['meta']['uid'] == stationID:
                return [element[0] for element in d['data']]

    @property
    def dateInterval(self):
        return self.metadata['dateInterval']

    @property
    def startDate (self):
        return self.metadata['startDate']

    @property
    def endDate (self):
        return self.metadata['endDate']

    def append(self, newStationData):
        '''
        Appends additional weather data to the wxData objects
        '''
##        for sd in newStationData['data']:
##            self['data'].append(sd)
        self['data'].append(newStationData['data'])

    @property
    def data(self):
        return self['data']


if __name__ == '__main__':

    data =  {u'data': [{u'data': [[u'11.0'], [u'14.0'], [u'4.5'], [u'6.0'], [u'3.5']],
            u'meta': {u'sids': [u'14607 1',
                                u'171175 2',
                                u'CAR 3',
                                u'72712 4',
                                u'KCAR 5',
                                u'USW00014607 6',
                                u'CAR 7']}},
           {u'data': [[u'18.5'], [u'24.0'], [u'10.5'], [u'12.0'], [u'21.0']],
            u'meta': {u'sids': [u'03005 1',
                                u'052281 2',
                                u'USC00052281 6',
                                u'DLLC2 7']}}]}

    moreData =  {u'data': [{u'data': [[u'11.0'], [u'14.0'], [u'4.5'], [u'6.0'], [u'3.5']],
            u'meta': {u'sids': [u'14607 1',
                                u'171175 2',
                                u'CAR 3',
                                u'72712 4',
                                u'KCAR 5',
                                u'USW00014607 6',
                                u'CAR 7']}},
           {u'data': [[u'18.5'], [u'24.0'], [u'10.5'], [u'12.0'], [u'21.0']],
            u'meta': {u'sids': [u'03005 1',
                                u'052281 2',
                                u'USC00052281 6',
                                u'DLLC2 7']}}]}

    s = WxData(data,  duration = 'dly', queryParams = {'sid':'Station 5'}, startDate = '1980-01-01', endDate = '1980-01-05')
    print (s.keys())
    print (s.toJSON())
    print (s.metadata)
    print (s.stationIDList)
    print (s.getStationData('03005 1'))  ##TRY TO RETURN SAME STRUCTURE AS WHAT WAS DONE FOR THE CLIMATE VERIFIER
    s.append(moreData)
    print len(s.data)
