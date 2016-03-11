from IM_Climate import IM_Climate

class Station(IM_Climate):
    def __init__(self, stationID):
        super(Station,self).__init__()
        self.stationID = stationID
        self.webServiceSource = 'StnData'
        self.reduceCodes = {'max': 'Maximum value for the period'
                , 'min':'Minimum value for the period'
                , 'sum' : 'Sum of the values for the period'
                , 'mean': 'Average of the values for the period'}

    def getDailyData(self, startDate = None, endDate = None, wxElements = None):
        pass

    def getMonthySummary(self, wxElement, reduceCode, startYear, endYear):
        self.duration = 'mly'
        data = self._call_ACIS(sid = self.stationID, sdate= str(startYear) + '-01', edate= str(endYear) + '-12', elems = 'mly_' + reduceCode +'_' + wxElement)
        print data


if __name__=='__main__':
    s = Station('KCAR')
    s.getMonthySummary(wxElement = 'avgt', reduceCode = 'mean', startYear = 1980, endYear = 2015 )
