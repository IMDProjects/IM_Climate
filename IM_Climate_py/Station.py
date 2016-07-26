class WxOb(dict):
    ''''
    A dictionary containing a weather observation for a specific station, parameter and date
    WxOb is indexable like a standard dictionary although values can also
    be accessed as properties:
        -WxOb.date
        -WxOb.wxOb, etc).
        -WxOb.ACIS_Flag
        -WxOb.sourceFlag
    '''
    def __init__(self, values):
        self['date'] = values[0]
        self['wxOb']  = values[1]
        self['ACIS_Flag'] = values[2]
        self['sourceFlag'] = values[3]

    @property
    def date(self):
        return self['date']
    @property
    def wxOb(self):
        return self['wxOb']
    @property
    def ACIS_Flag(self):
        return self['ACIS_Flag']
    @property
    def sourceFlag(self):
        return self['sourceFlag']

class ParameterSeries(dict):
    '''
    Dictionary of all weather observations for a particular climate parameter
    A particular wx observation is indexable by date.
    ParameterSeries has been extended to be iterable like a list
    '''

    def __init__(self, pData, dates, parameter):
        self.parameter = parameter
        for index, value in enumerate(pData):
            date = [dates[index]]
            wo = date
            wo.extend(value)
            self[date[0]] = WxOb(wo)

    def __iter__(self):
        for k in sorted(self.keys()):
            yield self[k]


class StationData(dict):
    '''
    Dictionary(-like) object containing all climate parameter data (i.e., one or more
    parameter series) for a specific station.
    StationData has been extended to include the ability to iterate like a list
    '''
    def __init__(self, stationData, climateParameters):
        self.observationDates = tuple([d[0] for d in stationData])
        for index, p in enumerate(climateParameters):
            self[p] = ParameterSeries(([d[index+1] for d in stationData]), dates = self.observationDates, parameter = p)
    @property
    def climateParameters(self):
        return self.keys()

    def __iter__(self):
        for param in self.keys():
            yield self[param]


class Station(object):
    '''
    Object containing all station information and data
    Blank values are converted to 'NA'
    Each station has metadata properties (e.g., uid, elev, sids, etc) and data
    '''
    def __init__(self, stationMeta, stationData = None):
        self._setStationMetadata(stationMeta)
        self._tags = ['name', 'latitude', 'longitude', 'sid1', 'sid2','sid3', 'stateCode', 'elev', 'uid', 'dateRange']
        if stationData:
            self._setStationData(stationData['stationData'], stationData['climateParameters'] )

    def _setStationData(self, stationData, climateParameters):
        self.data = StationData(stationData, climateParameters)


    def _setStationMetadata(self, stationInfo, climateParameters = None):
        '''
        Sets the station metadata. Values that are not present are set to 'NA'
        '''

        default = 'NA'
        self.name = stationInfo.get('name', default)
        try:
            self.sid1 = stationInfo['sids'][0]
        except:
            self.sid1 = default
        try:
            self.sid2 = stationInfo['sids'][1]
        except:
            self.sid2 = default
        try:
            self.sid3 = stationInfo['sids'][2]
        except:
            self.sid3 = default
        self.latitude = stationInfo.get('ll', default)[1]
        self.longitude = stationInfo.get('ll', default)[0]
        self.stateCode = stationInfo.get('state', default)
        self.elev = stationInfo.get('elev', default)
        self.dateRange = stationInfo.get('valid_daterange', default)
        self.uid = stationInfo.get('uid', default)
        self.sids = stationInfo.get('sids', default)
        self._setStationSource()


    def _setStationSource(self):
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
        return str(self.uid) + ' : ' +  self.stationSource +  ' : ' + self.name + ' : ' + self.sid1

##    def __repr__(self):
##        '''
##        '''
##
##        z =  str([self.__dict__[t] for t in self._tags])
##        return z

if __name__=='__main__':

    #WxOb
    data = ['2012-02-01',u'32.0', u' ', u'U']
    wx = WxOb(data)
    print wx
    ##############################

    #ParameterSeries
    data = [[u'21.5', u' ', u'U'],
         [u'29.5', u' ', u'U'],
         [u'32.0', u' ', u'U'],
         [u'27.5', u' ', u'U'],
         [u'35.5', u' ', u'U']]
    dates = (u'2012-01-01', u'2012-01-02', u'2012-01-03', u'2012-01-04', u'2012-01-05')
    parameter = 'maxt'
    ps = ParameterSeries(data,dates,parameter)
    print ps

    #################################

    #StationData
    data = [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
         [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
         [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
         [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
         [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]]
    parameters = ['maxt', 'mint']
    sd = StationData(data,parameters)
    print sd
    ####################

    #Station
    meta= {'name': 'Elliot Ridge', 'll': [-106.42, 39.86], 'sids': [u'USS0006K29S 6'], 'state': 'CO', 'valid_daterange': [['1983-01-12', '2016-04-05']], 'uid': 77459}
    data =  [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
           [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
           [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]]
    climateParams = ['maxt', 'mint' ]

    s = Station(stationMeta = meta)
    s._setStationData(data, climateParams)
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

