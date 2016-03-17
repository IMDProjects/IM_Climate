from ACIS import ACIS
from WxData import WxData



class DataRequestor(ACIS):
    def __init__(self,*args,**kwargs):
        super(DataRequestor,self).__init__(*args,**kwargs)
        self.webServiceSource = 'MultiStnData'

    def getDailyWxObservations(self, stations, wxElement, startDate, endDate, **kwargs):
        response =  self._call_ACIS(sids = self._extractStationList(stations), sdate = startDate,
            edate = endDate, elems = wxElement, add = 'f', meta = 'sids')
        return WxData(response, startDate = startDate, endDate = endDate, dateInterval = 'daily', **kwargs)

    def getMonthySummary(self, stations, wxElement, reduceCode, startYear = None, endYear = None, **kwargs):
        self.duration = 'mly'
        response = self._call_ACIS(sids = self._extractStationList(stations), sdate = str(startYear) + '-01',
            edate = str(endYear) + '-12', elems = 'mly_' + reduceCode +'_' + wxElement)
        return WxData(response, startDate = startYear, endDate = endYear, dateInterval = 'monthly', **kwargs)

    def _extractStationList(self, stations):
        '''
        If the station is a WxData objects, extracts list of stations using method.
        Otherwise, assumes stations is a list
        '''

        try:
            return stations.stationIDs
        except:
            return stations



if __name__=='__main__':
    s = DataRequestor()
    stations = ['KCAR', 'USC00052281']
    d =  s.getMonthySummary(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1980', endYear = '1981' )
    #d =  s.getDailyWxObservations(stations = stations, wxElement = 'avgt', startDate = '1990-01-01', endDate = '1990-02-05' )
    print d.metadata