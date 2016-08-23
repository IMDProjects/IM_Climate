from ACIS_StationDateRange import ACIS_StationDateRange
##from StationData import StationData
from ACIS import ACIS
from Station import Station



class ACIS_Station(Station):
    '''
    Object containing all station metadata (e.g., uid, elev, sids, etc) and weather data by parameter
    Blank metadata values are converted to 'NA'
    '''
    def __init__(self, stationMeta, climateParameters, stationData = None):
        super(ACIS_Station, self).__init__(stationMeta, climateParameters, stationData)
        self.validDateRange = ACIS_StationDateRange(stationMeta.get('valid_daterange', self.missingValue), self.climateParameters)
        self.maxRange = self.validDateRange.maxRange
        self.minRange = self.validDateRange.minRange



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


