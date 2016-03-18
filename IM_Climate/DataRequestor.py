from ACIS import ACIS
from WxData import WxData

class DataRequestor(ACIS):
    def __init__(self, *args, **kwargs):
        super(DataRequestor,self).__init__(*args, **kwargs)
        self.webServiceSource = 'MultiStnData'

    def getDailyWxObservations(self, stations, wxElement, startDate = None, endDate = None, **kwargs):
        '''
        Returns the daily weather element observations for one or more stations.
        Flags and time of observation, if they exist, are also returned.
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
        self.startYear = startYear
        self.endYear = endYear
        self._formatYears()

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

    def _formatYears(self):
        '''
        Method to deal with dates that default to None.
        Generally, it set dates to a 30-year range, depending on if start or end
        dates are specified.
        '''
        if not self.endYear and self.startYear:
            self.endYear = self.getCurrentYear()
        elif not self.startYear and self.endYear:
            self.startYear = self.endYear - 30
        elif not self.startYear and not self.endYear:
            self.endYear = self.getCurrentYear()
            self.startYear = self.endYear  - 30


if __name__=='__main__':
    dr = DataRequestor()
    dr.wxElements
    stations = ['KCAR', 'USC00052281']
    data =  s.getMonthySummary(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1980', endYear = '1981' )
    #data =  s.getDailyWxObservations(stations = stations, wxElement = 'avgt', startDate = '1990-01-01', endDate = '1990-02-05' )
    print data.metadata
    #print data.getStationData(d.stationIDList[0])
