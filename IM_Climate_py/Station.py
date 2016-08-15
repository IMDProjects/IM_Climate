from StationDateRange import StationDateRange
from StationData import StationData
from common import missingValue


class Station(object):
    '''
    Base class for all Station objectves.
    Object containing all station metadata (e.g., uid, elev, sids, etc) and weather data by parameter
    '''
    def __init__(self, stationMeta, climateParameters, stationData = None):
        self.missingValue = missingValue
        self.climateParameters = climateParameters
        self._setStationMetadata(stationMeta)
        self._tags = None #tags defined in child class
        if stationData:
            self._addStationWxData(stationData)

    def _addStationWxData(self, stationData):
        '''
        Method to add weather data to Station object
        '''
        pass #implementation should be in child class


    def _setStationMetadata(self, stationInfo):
        '''
        Sets the station metadata. Values that are not present are set to 'NA'
        '''

        pass #implementation should be in child class


    def _dumpToList(self):
        return [self.__dict__[t] for t in self._tags]

    def __repr__(self):
        '''
        Pretty representation of Station object
        '''
        return str(self._dumpToList())




if __name__=='__main__':

    meta= {'name': 'Elliot Ridge', 'll': [-106.42, 39.86], 'sids': [u'USS0006K29S 6'], 'state': 'CO', 'valid_daterange': [['1983-01-12', '2016-04-05']], 'uid': 77459}
    data =  [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
           [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
           [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]]
    climateParams = ['maxt', 'mint' ]

##    s = Station(stationMeta = meta, climateParameters = climateParams)
##    s._addStationWxData(data)
##    print s.name
##    print s.longitude
##    print s.elev
##    print s.sids
##    print s.stationType
##    print s.data['mint']
##    print s


