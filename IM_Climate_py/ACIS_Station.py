from ACIS_StationDateRange import ACIS_StationDateRange
from StationData import StationData
from ACIS import ACIS
from Station import Station



class ACIS_Station(Station):
    '''
    Object containing all station metadata (e.g., uid, elev, sids, etc) and weather data by parameter
    Blank metadata values are converted to 'NA'
    '''
    def __init__(self, stationMeta, climateParameters, stationData = None):
        super(ACIS_Station, self).__init__(stationMeta, climateParameters, stationData)
        self._tags = ['name', 'latitude', 'longitude', 'sid1', 'sid1_type',
            'sid2', 'sid2_type', 'sid3', 'sid3_type', 'state',
            'elev', 'uid', 'minRange', 'maxRange']

    def _addStationWxData(self, stationData):
        '''
        Method to add weather data to Station object
        '''
        self.data = StationData(stationData, self.climateParameters)


    def _setStationMetadata(self, stationInfo):
        '''
        Sets the station metadata. Values that are not present are set to 'NA'
        '''

        default = self.missingValue
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
        self.sid1_type = self._setStationType(self.sid1)
        self.sid2_type = self._setStationType(self.sid2)
        self.sid3_type = self._setStationType(self.sid3)
        self.latitude = stationInfo.get('ll', default)[1]
        self.longitude = stationInfo.get('ll', default)[0]
        self.state = stationInfo.get('state', default).encode()
        self.elev = stationInfo.get('elev', default)
        self.validDateRange = ACIS_StationDateRange(stationInfo.get('valid_daterange', default), self.climateParameters)
        self.maxRange = self.validDateRange.maxRange
        self.minRange = self.validDateRange.minRange
        self.uid = stationInfo.get('uid', default)
        self.sids = str(stationInfo.get('sids', default)).encode()

    def _setStationType(self, sid):
        acis = ACIS()
        if sid <> self.missingValue:
            stationType = acis.stationSources[str(sid.split()[1])]['description'].encode()
            if stationType == 'GHCN':
                try:
                    stationType = acis.stationSources['6']['subtypes'][self.sid1[0:3]].encode()
                except:
                    pass # Keep it GHCN
            return stationType
        else:
            return self.missingValue




if __name__=='__main__':

    meta= {'name': 'Elliot Ridge', 'll': [-106.42, 39.86], 'sids': [u'USS0006K29S 6'], 'state': 'CO', 'valid_daterange': [['1983-01-12', '2016-04-05']], 'uid': 77459}
    data =  [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
           [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
           [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]]
    climateParams = ['maxt', 'mint' ]

    s = ACIS_Station(stationMeta = meta, climateParameters = climateParams)
    s._addStationWxData(data)
    print s.name
    print s.longitude
    print s.elev
    print s.sids
    print s.sid1_type
    print s.data['mint']
    print s


