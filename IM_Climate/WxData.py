import datetime
try:
    #python 2.x
    from dataObjects import dataObjects
except:
    #python 3.x
    from .dataObjects import dataObjects

class WxData(dataObjects):
    def __init__(self, data, duration,  *args, **kwargs):
        self['meta'] = {}   #Wx data return from ACIS does not have a 'meta' section
        kwargs['duration'] = duration
        super(WxData, self).__init__(data, *args, **kwargs)

        if duration == 'dly':
            self._addDailyDates()
        elif duration == 'mly':
            self._addMonthlyDates()
        elif duration == 'yly':
            self._addYearlyDates()
        else:
            raise Exception('Invalid dateInteval')
        self._addStandardMetadataElements()


    def _addYearlyDates(self):
        dateList = []
        for year in range(int(self.startDate), int(self.endDate) + 1):
            dateList.append(str(year))
        self._verifyDates(dateList)

    def _addDailyDates(self):
        '''
        Creates list of all daily dates
        '''
        d1 = self._parseDate(self.startDate)
        d2 = self._parseDate(self.endDate)
        dateList = []
        diff = d2 - d1
        for i in range(diff.days + 1):
            dateList.append((d1 + datetime.timedelta(i)).isoformat())
        self._verifyDates(dateList)


    def _addMonthlyDates(self):
        dateList = []
        for year in range(int(self.startDate), int(self.endDate) + 1):
            for month in range (1,13):
                dateList.append(str(year) + '-' + str(month))
        self._verifyDates(dateList)

    def _verifyDates(self, dateList):
        '''
        Confirms length of date list matches length of time series
        '''
        if len(dateList) == len(self.getStationData( self.stationIDList[0])):
            self._addMetadata(dateList = dateList)
        else:
            raise Exception('Dates do not match data')

    @property
    def dateList(self):
        return self['meta']['dateList']

    @property
    def stationIDList(self):
        '''
        List of all stationIDs within dataset
        '''
        return [k['meta']['sids'][0] for k in self['data']]

    def getStationData(self, stationID):
        '''
        Returns time series of data for a specied station
        '''
        for d in self['data']:
            if d['meta']['sids'][0] == stationID:
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

    s = WxData(data,  duration = 'dly', queryParams = {'sid':'Station 5'}, startDate = '1980-01-01', endDate = '1980-01-05')
    print (s.keys())
    print (s.toJSON())
    print (s.metadata)
    print (s.stationIDList)
    print (s.getStationData('03005 1'))
