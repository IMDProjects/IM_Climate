from IM_Climate import IM_Climate

class Station(IM_Climate):
    def __init__(self):
        super(Station,self).__init__()
        self.webServiceSource = 'StnData'

    def getMonthySummary(self, station, wxElement, reduceCode, startYear, endYear):
        self.duration = 'mly'
        data = self._call_ACIS(sid = station, sdate= str(startYear) + '-01', edate= str(endYear) + '-12', elems = 'mly_' + reduceCode +'_' + wxElement)
        return data

    def getDailyWxObservations(self, station, wxElement, startDate, endDate):
        data =  self._call_ACIS(sid = station, sdate = startDate, edate = endDate, elems = wxElement, add = 'f')
        return data


if __name__=='__main__':
    s = Station()
    #print s.getMonthySummary(station = 'KCAR', wxElement = 'avgt', reduceCode = 'mean', startYear = 1980, endYear = 2015 )
    print s.getDailyWxObservations(station = 'KCAR', wxElement = 'avgt',  startDate = '1980-01-01', endDate = '1980-02-01' )
