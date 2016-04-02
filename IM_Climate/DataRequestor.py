try:
    #python 2.x
    from ACIS import ACIS
    from WxData import WxData
except:
    #python 3.x
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
                    it will default to 30 years earlier than current year

                endYear - End year of calculation. If endYear is not provided,
                    it will default to current year.

        '''
        self.duration = 'mly'
        self.maxMissing = 1

        self.startYear = str(startYear) + '-01'
        self.endYear = str(endYear) + '-12'
        self._formatYears()

        response = self._call_ACIS(sids = self._extractStationList(stations),
            sdate = self.startYear, edate = self.endYear,
            elems = self.duration + '_' + reduceCode +'_' + wxElement,
            maxmissing = self.maxMissing, **kwargs)
        return WxData(response, duration = self.duration, startDate = self.startYear
                , endDate = self.endYear, queryParams = self.input_dict, **kwargs)

    def monthySummary_ALT(self, stations, wxElement, reduceCode, startYear = None,
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
                    it will default to 30 years earlier than current year

                endYear - End year of calculation. If endYear is not provided,
                    it will default to current year.

        '''
        self.webServiceSource = 'StnData'
        self.duration = 'mly'
        self.maxMissing = 1

        self.startYear = str(startYear) + '-01'
        self.endYear = str(endYear) + '-12'
        self._formatYears()
        stationList = self._extractStationList(stations)

        wd = WxData({}, duration = self.duration, startDate = self.startYear
                    ,endDate = self.endYear, queryParams = self.input_dict, **kwargs)

        for s in stationList:
            response = self._call_ACIS(sid = s,
                sdate = self.startYear, edate = self.endYear,
                elems = self.duration + '_' + reduceCode +'_' + wxElement,
                maxmissing = self.maxMissing, **kwargs)
            if response.get('error') <> 'no data available':
                wd.append(response)
        return wd


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
    #stations = ['KCAR', 'USC00052281']
    stations = ['93005 1', '94035 1', '23066 1', '03013 1', '93013 1', '03016 1', '03017 1', '050848 2', '051294 2', '051528 2', '051564 2', '051741 2', '052184 2', '03005 1', '052446 2', '053038 2', '053146 2', '053662 2', '053951 2', '054076 2', '054834 2', '055322 2', '055722 2', '057337 2', '057936 2', '058204 2', '058429 2', '059243 2', '24047 1', '23069 1', '052803 2', '051268 2', '050898 2', '054346 2', '052048 2', '050307 2', '058468 2', '051816 2', '054250 2', '058431 2', '058436 2', '054542 2', '050873 2', '055990 2', '057428 2', '057928 2', '051570 2', '053016 2', '055531 2', '056710 2', '057867 2', '058574 2', '23070 1', '056258 2', '058793 2', '057866 2', '056559 2', '03008 1', '054934 2', '055327 2', '051886 2', '052000 2', '057862 2', '053010 2', '050776 2', '058092 2', '056271 2', '053463 2', '054538 2', '054870 2', '23061 1', '050126 2', '050125 2', '055711 2', '059181 2', '059183 2', '052326 2', '054865 2', '058154 2', '058510 2', '055706 2']
    data = dr.monthySummary_ALT(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1980', endYear = '1981' )
    #data = dr.monthySummary(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1980', endYear = '1981' )
    print data['data']
    #print len(data.stationIDList)
##    data_annual = dr.yearlySummary(stations = stations, wxElement = 'avgt', reduceCode = 'mean', startYear = '1980', endYear = '1983' )
##    data = dr.dailyWxObservations(stations = stations, wxElement = 'avgt', startDate = '1990-01-01', endDate = '1990-02-05' )
##    print(data.metadata)
##    print(data.getStationData(data.stationIDList[0]))
##    print(data.keys())
##    print(data_annual)