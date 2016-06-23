##You can differentiate based on the GHCN station id. The RAW stations start out with ?USR? and SNOTEL stations start with ?USS?. Here are two examples:
##USR0000NLIT ? RAWS
##USS0020L02S ? SNOTEL

class Station(object):
    '''
    Blank values are converted to 'NA'
    '''
    def __init__(self, stationInfo):
        default = 'NA'
        self.name = stationInfo.get('name', default)
        self.sids = stationInfo.get('sids', default)
        self.latitude = stationInfo.get('ll', default)[1]
        self.longitude = stationInfo.get('ll', default)[0]
        self.stateCode = stationInfo.get('state', default)
        self.elev = stationInfo.get('elev', default)
        self.dateRange = stationInfo.get('valid_daterange', default)
        self.uid = stationInfo.get('uid', default)



if __name__=='__main__':
    stationInfo = {'name': 'Elliot Ridge', 'll': [-106.42, 39.86], 'sids': ['USS0006K29S 6'], 'state': 'CO', 'valid_daterange': [['1983-01-12', '2016-04-05']], 'uid': 77459}
    s = Station(stationInfo)
    print s.name
    print s.longitude
    print s.elev
