class Station(object):
    '''
    Blank values are converted to 'NA'
    '''
    def __init__(self, stationInfo):
        default = 'NA'
        self.name = stationInfo.get('name', default)
        self.sids = map(str, stationInfo.get('sids', default))
        self.latitude = stationInfo.get('ll', default)[1]
        self.longitude = stationInfo.get('ll', default)[0]
        self.stateCode = stationInfo.get('state', default)
        self.elev = stationInfo.get('elev', default)
        self.dateRange = stationInfo.get('valid_daterange', default)
        self.uid = stationInfo.get('uid', default)
        self._setStationSource()

    def _setStationSource(self):
        for sid in self.sids:
            if sid[0:3] == 'USR':
                self.stationSource = 'RAWS'
            elif sid[0:3] == 'USS':
                self.stationSource = 'SNOTEL'
            else:
                self.stationSource = 'UKNOWN'


if __name__=='__main__':
    stationInfo = {'name': 'Elliot Ridge', 'll': [-106.42, 39.86], 'sids': [u'USS0006K29S 6'], 'state': 'CO', 'valid_daterange': [['1983-01-12', '2016-04-05']], 'uid': 77459}
    s = Station(stationInfo)
    print s.name
    print s.longitude
    print s.elev
    print s.sids
    print s.stationSource
