try:    #python 2.x
    from ACIS import ACIS
    from WxData import WxData
except: #python 3.x
    from .ACIS import ACIS
    from .WxData import WxData

class DataRequestor(ACIS):
    def __init__(self, *args, **kwargs):
        super(DataRequestor,self).__init__(*args, **kwargs)
        self.webServiceSource = 'StnData'

    def dailyWxObservations(self, stationID, parameter, startDate = 'por',
        endDate = 'por', **kwargs):
        '''
        Returns the daily weather element observations for a single station.
        Flags and time of observation, if they exist, are also returned.

        Arguments:
            stationID - The ACIS uid

            parameter - The weather parameter to summarize. Valid parameters
                can be found using the DataRequestor.paramter property.
                Note that ACIS calls a parameter an element.
        '''
        duration = 'dly'

        response =  self._call_ACIS(uid = stationID, sdate = startDate,
            edate = endDate, elems = parameter, add = 'f,t', meta = 'sids', **kwargs)

        return WxData(response, duration = duration, startDate = startDate
            , endDate = endDate, queryParams = self.input_dict, **kwargs)

    def monthySummary(self, stationID, parameter, reduceCode, startDate = 'por',
         endDate = 'por',  **kwargs):

        '''
        RETURNS
        -------
        Returns the monthly weather element summary for a single station.
        Months with more than 1 missing day are not calculated.

        ARGUMENTS
        ---------
        stationID - The ACIS uid

        parameter - The weather parameter to summarize. Valid parameters
            can be found using the DataRequestor.paramter property.
            Note that ACIS calls a parameter an element.

        reduceCode - The method for reduction (i.e., aggregation).
            Valid reduction codes can be found using the
            DataRequestor.reductionCodes property.

        startDate - Begin year and month of calculation (YYYY-MM).
            Default is the period of record

        endDate - End year and month of calculation (YYYY-MM).
            Default is the period of record.

        '''
        duration = 'mly'
        maxMissing = 1

        elems = duration + '_' + reduceCode +'_' + parameter

        return self._iterateOverStations(uids = stationID, sdate = startDate,
                edate = endDate, elems = elems, maxmissing = maxMissing
                , **kwargs)

##        response = self._call_ACIS(uid = stationID, sdate = startDate,
##                edate = endDate, elems = elems, maxmissing = maxMissing
##                , **kwargs)
##
##        return WxData(response, duration = duration, startDate = startYearMonth
##                    ,endDate = endYearMonth, queryParams = self.input_dict, **kwargs)


    def _iterateOverStations(self, uids, **kwargs):
        for uid in uids:
            response = self._call_ACIS(uid = uid, **kwargs)
            print response

        return WxData(response, duration = duration, startDate = startDate
                    ,endDate = endDate, queryParams = self.input_dict, **kwargs)


    def yearlySummary(self, stationID, parameter, reduceCode, startYear = 'por',
         endYear = 'por',  **kwargs):

        '''
        RETURNS
        -------
        Returns the annual weather element summary for a single station.
        Years with more than 12 missing days are not calculated.

        ARGUMENTS
        ---------
        station - The ACIS uid

        parameter - The weather parameter to summarize. Valid parameters
            can be found using the DataRequestor.paramter property.
            Note that ACIS calls a parameter an element.

        reduceCode - The method for reduction (i.e., aggregation).
            Valid reduction codes can be found using the
            DataRequestor.reductionCodes property.

        startYear - Begin year of calculation. If beginYear is not provided,
            it will degault to 30 years earlier than current year

        endYear - End year of calculation. If endYear is not provided,
            it will degault to current year.

        '''
        duration = 'yly'
        maxMissing = '12'
        elems =  [{
            'name': parameter,
            'interval': duration,
            'duration': duration,
            'reduce': {
                'reduce': reduceCode,
                'add': 'mcnt'
            },
            'maxmissing': maxMissing,
        }]

        response = self._call_ACIS(uid = stationID,
            sdate = startYear, edate = endYear,
            elems = elems, **kwargs)

        return WxData(response, duration = duration, startDate = startYear
                , endDate = endYear, queryParams = self.input_dict, **kwargs)

    def climograph(self):
        pass

    def _extractStationList(self, stations):
        '''
        If stations is a stationList object, extracts list of stationIDs.
        Otherwise, assumes stationIDs to be a list.
        '''
        try:
            return stations.stationIDs
        except:
            return stations



if __name__=='__main__':
    dr = DataRequestor()
    print(dr.parameters)
    stationID = ['3940', '3941']
    data_monthly = dr.monthySummary(stationID = stationID, parameter = ['mint', 'avgt'], reduceCode = 'mean', startYear = '1980', endYear = '1981' )
    #data_annual = dr.yearlySummary(stationID = stationID, parameter = 'avgt', reduceCode = 'mean')
    #data = dr.dailyWxObservations(stationID = stationID, parameter = 'avgt', startDate = '1990-01-01', endDate = '1990-02-05' )
    #print(data.metadata)
##    print(data.getStationData(stationID))
##    print(data.keys())
##    print(data_annual)