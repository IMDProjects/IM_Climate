try:    #python 2.x
    import StationDict
    reload(StationDict)
    from StationDict import StationDict
    from Station import Station


except: #python 3.x
    from .dataObjects import dataObjects

class WxData(StationDict):
    def __init__(self, queryParameters, dateInterval, aggregation, wxParameters):
        '''
        Data object that holds and organizes all weather data returned by ACIS
        using the StnData request.

        '''
        super(WxData, self).__init__(queryParameters = queryParameters)
        self.dateInterval = dateInterval
        self.aggregation = aggregation
        self.wxParameters = wxParameters



if __name__ == '__main__':
    queryParameters = {'query':'params'}
    dateInterval = 'mly'
    aggregation = 'avg'

    #Station #1
    wxObs = {u'data': [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
           [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
           [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]],
 u'meta': {u'elev': 9600.1,
           u'll': [-105.9864, 39.56],
           u'name': u'SODA CREEK COLORADO',
           u'sids': [u'USR0000CSOD 6'],
           u'uid': 66180}}

    #Station #2,
    moreWxObs = {u'data': [[u'2012-01-01', [u'21.5', u' ', u'U'], [u'5', u' ', u'U']],
           [u'2012-01-02', [u'29.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-03', [u'32.0', u' ', u'U'], [u'19', u' ', u'U']],
           [u'2012-01-04', [u'27.5', u' ', u'U'], [u'12', u' ', u'U']],
           [u'2012-01-05', [u'35.5', u' ', u'U'], [u'18', u' ', u'U']]],
 u'meta': {u'elev': 9600.1,
           u'll': [-105.9864, 39.56],
           u'name': u'ILL CREEK COLORADO',
           u'sids': [u'USR0000CSOD 6'],
           u'uid': 1233}}

    wx = WxData(queryParameters, dateInterval = 'mly', aggregation = 'avg', wxParameters = ['mint','maxt'])
    wx._addStation(stationID = wxObs['meta']['uid'],  stationMeta =  wxObs['meta'], stationData =  {'stationData' : wxObs['data'], 'climateParameters' : climateParams})
    wx._addStation(stationID = wxObs['meta']['uid'],stationMeta =  moreWxObs['meta'], stationData =  {'stationData' : moreWxObs['data'], 'climateParameters' : climateParams})
    print wx.wxParameters
    print wx.stationIDs
    wx.exportData(filePathAndName = r'test.csv')
    print wx

    #WxData is indexable
    print wx[66180].data['maxt']['2012-01-01'].wxOb

    #Iterate through each station, parameter and weather observation
    for station in wx:
        for p in station.data:
            print p
            for ob in p:
                print ob
    print wx.stationNames
