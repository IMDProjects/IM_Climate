from IM_Climate import IM_Climate
from WxData import WxData



class DataRequestor(IM_Climate):
    def __init__(self):
        super(DataRequestor,self).__init__()
        self.webServiceSource = 'MultiStnData'

    def getDailyWxObservations(self, stations, wxElement, startDate, endDate):
        response =  self._call_ACIS(sids = self._extractStationList(stations), sdate = startDate,
            edate = endDate, elems = wxElement, add = 'f', meta = 'sids')
        return WxData(response, startDate = startDate, endDate = endDate, dateInterval = 'daily')

    def getMonthySummary(self, stations, wxElement, reduceCode, startYear = None, endYear = None):
        self.duration = 'mly'
        response = self._call_ACIS(sids = self._extractStationList(stations), sdate = startYear + '-01',
            edate = endYear + '-12', elems = 'mly_' + reduceCode +'_' + wxElement)
        return WxData(response, startDate = startYear, endDate = endYear, dateInterval = 'monthly')

    def _extractStationList(self, stations):
        if type(stations) == 'WxData':
            return stations['meta']['stationList']
        else:
            return stations



if __name__=='__main__':
    s = DataRequestor()
    stations = ['KCAR', 'USC00052281']
    d =  s.getMonthySummary(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1980', endYear = '1981' )
    #d =  s.getDailyWxObservations(stations = stations, wxElement = 'avgt', startDate = '1990-01-01', endDate = '1990-02-05' )
    print d['meta']