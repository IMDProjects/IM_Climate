from DataRequestor import DataRequestor

class Station(DataRequestor):
    def __init__(self):
        super(Station,self).__init__()
        self.webServiceSource = 'StnData'

    def getMonthySummary(self, station, wxElement, reduceCode, startYear, endYear, maxmissing = 2):
        self.duration = 'mly'
        data = self._call_ACIS(sid = station, sdate= str(startYear) + '-01', edate= str(endYear) + '-12', elems = 'mly_' + reduceCode +'_' + wxElement)
        return data

    #def getDailyWxObservations(self, station, wxElement, startDate, endDate, **kwargs):
    def getDailyWxObservations(self, station, **kwargs):
        super(Station, self).getDailyWxObservations(stations = None, sid = station, **kwargs)

##        data =  self._call_ACIS(sid = station, sdate = startDate, edate = endDate, elems = wxElement, add = 'f')
##        return data


if __name__=='__main__':
    s = Station()
    #data =  s.getMonthySummary(station = 'KCAR', wxElement = 'avgt', reduceCode = 'mean', startYear = 1980, endYear = 2015 )
    print s.getDailyWxObservations(station = 'KCAR', wxElement = 'avgt',  startDate = '1980-01-01', endDate = '1980-02-01' )
    print data.metadata
