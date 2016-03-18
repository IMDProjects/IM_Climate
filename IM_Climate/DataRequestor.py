from ACIS import ACIS
from WxData import WxData



class DataRequestor(ACIS):
    def __init__(self,*args,**kwargs):
        super(DataRequestor,self).__init__(*args,**kwargs)
        self.webServiceSource = 'MultiStnData'

    def getDailyWxObservations(self, stations, wxElement, startDate, endDate, **kwargs):
        '''
        Returns the daily weather element observations for one or more stations.
        Flags and time of observation (if it exists), are also returned.
        '''

        response =  self._call_ACIS(sids = self._extractStationList(stations), sdate = startDate,
            edate = endDate, elems = wxElement, add = 'f,t', meta = 'sids', **kwargs)
        return WxData(response, startDate = startDate, endDate = endDate, dateInterval = 'daily', **kwargs)

    def getMonthySummary(self, stations, wxElement, reduceCode, startYear = None,
         endYear = None, maxmissing = 1,  **kwargs):

        '''
            Returns the monthly weather element summary for one or more stations.
            Months with more than 1 missing day are not calculated.

            Arguments:
                stations - Stations can be passed as the stationList object returned
                    from a stationFinder search or stations can be in list format

                wxElement - The weather element to summarize. Valid weather elements
                    can be found using the DataRequestor.wxElement property.

                reduceCode - The method for reduction (i.e., aggregation).
                    Valid reduction codes can be found using the
                    DataRequestor.reductionCodes property.

                startYear - Begin year of calculation. If beginYear is not provided,
                    it will degault to 30 years earlier than current year

                endYear - End year of calculation. If endYear is not provided,
                    it will degault to current year.

        '''
        self.duration = 'mly'
        if not endYear:
            endYear = self.getCurrentYear()
        if not startYear:
            startYear = self.CurrentYear() - 30


        response = self._call_ACIS(sids = self._extractStationList(stations),
            sdate = str(startYear) + '-01', edate = str(endYear) + '-12',
            elems = 'mly_' + reduceCode +'_' + wxElement, **kwargs)
        return WxData(response, startDate = startYear, endDate = endYear,
            dateInterval = 'monthly', **kwargs)

    def _extractStationList(self, stations):
        '''
        If the station is a stationList object, extracts list of stations.
        Otherwise, assumes stations to be a list.
        '''

        try:
            return stations.stationIDs
        except:
            return stations




if __name__=='__main__':
    s = DataRequestor()
    s.wxElements
    stations = ['KCAR', 'USC00052281']
    #d =  s.getMonthySummary(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1980', endYear = '1981' )
    d =  s.getDailyWxObservations(stations = stations, wxElement = 'avgt', startDate = '1990-01-01', endDate = '1990-02-05' )
    print d.metadata
    print d.getStationData(d.stationIDList[0])