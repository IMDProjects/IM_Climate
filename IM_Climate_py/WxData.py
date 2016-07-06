try:    #python 2.x
    from dataObjects import dataObjects
    from Station import Station
except: #python 3.x
    from .dataObjects import dataObjects

class WxData(dict, dataObjects):
    def __init__(self, queryParameters, dateInterval, aggregation, wxParameters, data = None, *args, **kwargs):
        '''
        Data object that holds and organizes all weather data returned by ACIS
        using the StnData request.

        '''
        self.queryParameters = queryParameters
        self.dateInterval = dateInterval
        self.aggregation = aggregation
        self.wxParameters = wxParameters
        if data:
            self.add(data)

    def add(self, newData):
        '''
        Adds additional weather data to the wxData object unless there is an
        'error' tag. In that case, no data is appended for the
        '''
        #Duck Type - check is data dictionary exists
        #If not, then add the data dictionary in exception
        try:
            self[newData['meta']['uid']].keys()
        except:
            self[newData['meta']['uid']]={}

        #If no data, then set to None. Otherwise, add the station data and station metadata
        if newData.get('error'):
            self[newData['meta']['uid']]['data'] = None
        else:
            #self[newData['meta']['uid']]['data'] = tuple(newData['data'])
            self[newData['meta']['uid']] = Station(stationMetadata = newData['meta'],
                    stationData = tuple(newData['data']))
        self.stationIDs = self.keys() #Update metadata to reflect all stationIDs


    def _dumpToList(self):
        '''
        INFO
        ----
        Dumps all info to a list

        NOTE:
        ----
        Method currently assumes that each station has the same set of parameters
        for the same date range.
        '''
        header = ['UID','Longitude', 'Latitude', 'Sids1', 'Sids2','Sids3', 'Name', 'Elevation', 'Date']
        params = self.wxParameters
        for p in params:
            header.append(p)
        self._dataAsList = [header]
        for station in self.stationIDs:
            for ob in self[station].data:
                lat = self[station].latitude
                lon = self[station].longitude
                name = self[station].name
                elev = self[station].elev
                sid1 = self[station].sid1
                sid2 = self[station].sid2
                sid3 = self[station].sid3
                a = [str(station), lon, lat,sid1,sid2,sid3,name,elev]
                for o in ob:
                    a.append(o)
                self._dataAsList.append(a)

if __name__ == '__main__':
    queryParameters = {'elk':'moose'}
    dateInterval = 'mly'
    aggregation = 'avg'

    #Station #1
    wxObs = {u'data': [[u'2012-01-01', u'21.5', u'5'],
           [u'2012-01-02', u'29.5', u'12'],
           [u'2012-01-03', u'32.0', u'19'],
           [u'2012-01-04', u'27.5', u'12'],
           [u'2012-01-05', u'35.5', u'18']],
    u'meta': {u'elev': 9600.1,
           u'll': [-105.9864, 39.56],
           u'name': u'SODA CREEK COLORADO',
           u'sids': [u'USR0000CSOD 6'],
           u'uid': 66180}}

    #Station #2,
    moreWxObs = {u'data': [[u'2012-01-01', u'21.5', u'5'],
           [u'2012-01-02', u'29.5', u'12'],
           [u'2012-01-03', u'32.0', u'19'],
           [u'2012-01-04', u'27.5', u'12'],
           [u'2012-01-05', u'35.5', u'18']],
 u'meta': {u'elev': 9600.1,
           u'll': [-105.9864, 39.56],
           u'name': u'SODA CREEK COLORADO',
           u'sids': [u'USR0000CSOD 6'],
           u'uid': 66181}}

    s = WxData(queryParameters, dateInterval = 'mly', aggregation = 'avg', wxParameters = ['mint','maxt'])
    s.add(wxObs)
    s.add(moreWxObs)
    print s.wxParameters
    print s.stationIDs
    s.export(filePathAndName = r'test.csv')
