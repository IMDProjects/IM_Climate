from datetime import date
import datetime

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
        self['date'] = values[0].encode()
        self['wxOb']  = values[1].encode()
        self['ACIS_Flag'] = values[2].encode()
        self['sourceFlag'] = values[3].encode()


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
        '''
        Allow iteration over StationData (like a list)
        '''
        for param in self.keys():
            yield self[param]


class Station(object):
    '''
    Object containing all station metadata (e.g., uid, elev, sids, etc) and weather data
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

        default = 'NA'
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
        Pretty presentation of Station
        '''
        return str(self.uid) + ' : ' +  self.stationSource +  ' : ' + self.name + ' : ' + self.sid1


class StationDateRange(dict):
    '''
    Dictionary containing the valid date ranges for each weather parameter
    '''
    def __init__(self, dateRanges, climateParameters):
        if not climateParameters:
            return

        #Assign Begin and End Dates to Each Parameter
        for index, p in enumerate(climateParameters):
            try:
                b =  dateRanges[index][0]
                e = dateRanges[index][1]
                self[p] = {'begin': date(int(b[0:4]), int(b[5:7]), int(b[9:10])),
                    'end': date(int(e[0:4]), int(e[5:7]), int(e[9:10]))}
            except:
                self[p] = {'begin': 'NA', 'end': 'NA'}

        #Calculate the range of dates based on all parameters

        self.begin = date(2100,1,1)
        self.end =  date(1492,1,1)

        for p in self.items():
            if p[1]['begin'] <> 'NA':
                if p[1]['begin'] < self.begin:
                    self.begin = p[1]['begin']
            if p[1]['end'] <> 'NA':
                if p[1]['end'] > self.end:
                    self.end = p[1]['end']

        if self.begin == date(2100,1,1):
            self.begin = 'NA'
        if self.end == date(1492,1,1):
            self.end = 'NA'

    def __repr__(self):
        try:
            return str({'begin': self.begin.isoformat(), 'end':  self.end.isoformat()})
        except:
            return str({'begin': 'NA', 'end':  'NA'})
if __name__=='__main__':

    #StationDateRange

    dateRanges = [[u'1999-10-01', u'2016-07-24'],
                                 [u'1999-10-28', u'2016-07-23'],
                                 []]
    parameters = ['mint', 'maxt', 'avgt']

    dr = StationDateRange(dateRanges = dateRanges, climateParameters = parameters)
    print dr.begin
    print dr.end
    print dr

    ############################################################################
    ############################################################################
    #WxOb
    data = ['2012-02-01',u'32.0', u' ', u'U']
    wx = WxOb(data)
    print wx

    ############################################################################
    ############################################################################
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

    ############################################################################
    ############################################################################
    #StationData
    data = [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
         [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
         [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
         [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
         [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]]
    parameters = ['maxt', 'mint']
    sd = StationData(data,parameters)
    print sd

    ############################################################################
    ############################################################################
    #Station
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

