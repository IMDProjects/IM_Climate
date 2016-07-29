from StationDateRange import StationDateRange
from StationData import StationData
from ACIS import missingValue



class Station(object):
    '''
    Object containing all station metadata (e.g., uid, elev, sids, etc) and weather data by parameter
    Blank metadata values are converted to 'NA'
    '''
    def __init__(self, stationMeta, climateParameters, stationData = None):
        self.climateParameters = climateParameters
        self._setStationMetadata(stationMeta)
        self._tags = ['name', 'latitude', 'longitude', 'sid1', 'sid2','sid3', 'stateCode', 'elev', 'uid', 'dateRange']
        if stationData:
            self._addStationWxData(stationData)

    def _addStationWxData(self, stationData):
        '''
        Method to add weather data to Station object
        '''
        self.data = StationData(stationData, self.climateParameters)


    def _setStationMetadata(self, stationInfo):
        '''
        Sets the station metadata. Values that are not present are set to 'NA'
        '''

        default = missingValue
        self.name = stationInfo.get('name', default).encode()
        try:
            self.sid1 = str(stationInfo['sids'][0]).encode()
        except:
            self.sid1 = default
        try:
            self.sid2 = str(stationInfo['sids'][1]).encode()
        except:
            self.sid2 = default
        try:
            self.sid3 = str(stationInfo['sids'][2]).encode()
        except:
            self.sid3 = default
        self.latitude = stationInfo.get('ll', default)[1]
        self.longitude = stationInfo.get('ll', default)[0]
        self.stateCode = stationInfo.get('state', default).encode()
        self.elev = stationInfo.get('elev', default)
        #self.dateRange = stationInfo.get('valid_daterange', default)
        self.dateRange = StationDateRange(stationInfo.get('valid_daterange', default), self.climateParameters)
        self.uid = stationInfo.get('uid', default)
        self.sids = str(stationInfo.get('sids', default)).encode()
        self._setStationSource()


    def _setStationSource(self):
        '''
        This method is incomplete at present...not sure of how to determine other
        sources. Take at face value.
        '''
        for sid in self.sids:
            if sid[0:3] == 'USC':
                self.stationSource = 'COOP'
            if sid[0:3] == 'USR':
                self.stationSource = 'RAWS'
            elif sid[0:3] == 'USS':
                self.stationSource = 'SNOTEL'
            else:
                self.stationSource = 'UNKNOWN'

    def __repr__(self):
        '''
        Pretty representation of Station object
        '''
        return str(self.uid) + ' : ' +  self.stationSource +  ' : ' + self.name + ' : ' + self.sid1



if __name__=='__main__':

    meta= {'name': 'Elliot Ridge', 'll': [-106.42, 39.86], 'sids': [u'USS0006K29S 6'], 'state': 'CO', 'valid_daterange': [['1983-01-12', '2016-04-05']], 'uid': 77459}
    data =  [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
           [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
           [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]]
    climateParams = ['maxt', 'mint' ]

    s = Station(stationMeta = meta, climateParameters = climateParams)
    s._addStationWxData(data)
    print s.name
    print s.longitude
    print s.elev
    print s.sids
    print s.stationSource
    print s.data['mint']
    print s
    print s._tags
    for w in s.data['mint']:
        print w.date
    for param in s.data:
        for wxOs in param:
            wxOs.date

