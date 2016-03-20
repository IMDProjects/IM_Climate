try:
    from ACIS import ACIS
    from WxData import WxData
except:
    from .ACIS import ACIS
    from .WxData import WxData

class DataRequestor(ACIS):
    def __init__(self, *args, **kwargs):
        super(DataRequestor,self).__init__(*args, **kwargs)
        self.webServiceSource = 'MultiStnData'

    def dailyWxObservations(self, stations, wxElement, startDate = None, endDate = None, **kwargs):
        '''
        Returns the daily weather element observations for one or more stations.
        Flags and time of observation, if they exist, are also returned.
        '''
        self.duration = 'dly'
        response =  self._call_ACIS(sids = self._extractStationList(stations), sdate = startDate,
            edate = endDate, elems = wxElement, add = 'f,t', meta = 'sids', **kwargs)
        return WxData(response, duration = self.duration, startDate = startDate
            , endDate = endDate, queryParams = self.input_dict, **kwargs)

    def monthySummary(self, stations, wxElement, reduceCode, startYear = None,
         endYear = None,   **kwargs):

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
        self.maxMissing = 1

        self.startYear = str(startYear)
        self.endYear = str(endYear)
        self._formatYears()

        response = self._call_ACIS(sids = self._extractStationList(stations),
            sdate = startYear + '-01', edate = endYear + '-12',
            elems = self.duration + '_' + reduceCode +'_' + wxElement,
            maxmissing = self.maxMissing, **kwargs)
        return WxData(response, duration = self.duration, startDate = startYear
                , endDate = endYear, queryParams = self.input_dict, **kwargs)


    def yearlySummary(self, stations, wxElement, reduceCode, startYear = None,
         endYear = None,  **kwargs):

        '''
            Returns the annual weather element summary for one or more stations.
            Years with more than 12 missing days are not calculated.

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
        self.duration = 'yly'
        self.maxMissing = '12'
        self.startYear = str(startYear)
        self.endYear = str(endYear)
        self._formatYears()
        elems =  [{
            'name': wxElement,
            'interval': self.duration,
            'duration': self.duration,
            'reduce': {
                'reduce': reduceCode,
                'add': "mcnt"
            },
            'maxmissing': self.maxMissing,
            #'smry': ["max", "min", "mean"]
        }]

        response = self._call_ACIS(sids = self._extractStationList(stations),
            sdate = startYear, edate = endYear,
            elems = elems, **kwargs)

        return WxData(response, duration = self.duration, startDate = startYear
                , endDate = endYear, queryParams = self.input_dict, **kwargs)

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
            self.endYear = self._getCurrentYear()
        elif not self.startYear and self.endYear:
            self.startYear = self.endYear - 30
        elif not self.startYear and not self.endYear:
            self.endYear = self._getCurrentYear()
            self.startYear = self.endYear  - 30


if __name__=='__main__':
    dr = DataRequestor()
    print(dr.wxElements)
    stations = ['KCAR', 'USC00052281']
    data = dr.monthySummary(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1980', endYear = '1981' )
    data_annual = dr.yearlySummary(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1980', endYear = '1983' )
    data = dr.dailyWxObservations(stations = stations, wxElement = 'avgt', startDate = '1990-01-01', endDate = '1990-02-05' )
    print(data.metadata)
    print(data.getStationData(data.stationIDList[0]))
    print(data.keys())
    print(data_annual)