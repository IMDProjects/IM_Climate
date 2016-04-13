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

    def dailyWxObservations(self, stationIDs, parameter, startDate = 'por',
            endDate = 'por'):
        '''
        INFO
        -----
        Returns the daily weather element observations for a single station.
        Flags and time of observation, if they exist, are also returned.

        ARGUMENTS
        ---------
        stationID - The ACIS uid

        parameter - The weather parameter to summarize. Valid parameters
            can be found using the DataRequestor.paramter property.
            Note that ACIS calls a parameter an element.

        RETURNS
        -------

        '''
        self.duration = 'dly'
        self.stationIDs = stationIDs
        self.parameter = parameter
        self.reduceCode = None

        return self._iterateOverStationIDs(sdate = startDate,
            edate = endDate,  add = 'f,t,n', meta = 'uid',  elems = self.parameter)


    def monthySummaryByYear(self, stationIDs, parameter, reduceCode, startDate = 'por',
         endDate = 'por', maxMissing = 1):

        '''
        INFO
        -----
        Monthly summary by year. Months with more than 1 missing day are not
            calculated.

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

        maxMissing -

        RETURNS
        -------

        '''
        self.duration = 'mly'
        self.reduceCode = reduceCode
        self.parameter = parameter
        elems = self.duration + '_' + reduceCode +'_' + parameter
        self.stationIDs = stationIDs

        return self._iterateOverStationIDs(sdate = startDate, edate = endDate, elems = elems
             ,maxmissing = maxMissing)


    def _iterateOverStationIDs(self, **kwargs):
        '''
        INFO
        ----
        Makes data requests for one or more stationIDs. Appends data to wxData
        object.


        '''
        wd = WxData(dateInterval = self.duration, aggregation = self.reduceCode)

        for uid in self.stationIDs:
            response = self._call_ACIS(uid = uid, **kwargs)
            wd.add(response, parameter = self.parameter)

        return wd

    def yearlySummary(self, stationIDs, parameter, reduceCode, startYear = 'por',
         endYear = 'por'):

        '''
        INFO
        -----
        Calculates the annual weather element summary for a single station.
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

        RETURNS
        -------
        WxData, an extension to the dictionary object

        '''
        self.duration = 'yly'
        self.reduceCode = reduceCode
        self.parameter = parameter
        self.stationIDs = stationIDs

        maxMissing = '12'

        elems =  [{
            'name': parameter,
            'add': 'n',
            'interval': self.duration,
            'duration': self.duration,
            'reduce': {
                'reduce': self.reduceCode,
                'add': 'mcnt'
            },
            'maxmissing': maxMissing,
        }]

        return self._iterateOverStationIDs(
            sdate = startYear, edate = endYear,
            elems = elems)

    def climograph(self):
        '''
        INFO
        ----
        Pulls tmin, tmax, tavg and precipitation to support climograph
        '''

        pass


    def monthlySummary(self, stationIDs, parameter, reduceCode, startDate = 'por',
         endDate = 'por', maxMissing = 1):
        '''
        INFO
        -----
        Monthly summary computed for set of years (i.e, 12 one-month summaries).
        Months with more than ??x%?? missing day are not calculated.

        params = {"sid":"304174","sdate":"por","edate":"por","meta":["name","state"]
        ,"elems":[{"name":"maxt","interval":"dly","duration":"dly","smry":{"reduce":"max","add":"date"}
        ,"smry_only":1,"groupby":"year"}]}
        '''
        duration = 'dly'
        #elems = duration + '_' + reduceCode +'_' + parameter

        elems = [{"name":parameter,"interval":"mly","duration":"mly"
                ,"smry_only":1,"groupby":"year"}]

        return self._iterateOverStationIDs(sdate = startDate, edate = endDate,
            elems = elems ,maxmissing = maxMissing)



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
    #print(dr.parameters)
    stationIDs = [66180, 67175]
    #stationIDs = [66180]

    #Monthly Summary By Year
##    data_monthly = dr.monthySummaryByYear(stationIDs = stationIDs, parameter = 'avgt', reduceCode = 'mean', startDate = '1990-01', endDate = '1991-12' )
##    print data_monthly.stationIDs
##    print data_monthly.metadata
##    print data_monthly.data

    #Daily Data
    dailyData = dr.dailyWxObservations(stationIDs = stationIDs, parameter = 'avgt'
        , startDate = '2012-01-01', endDate = '2012-01-05' )
    print dailyData.data
    dailyData.toCSV(filePathAndName = r'data.csv')


    #Monthly Summary
##    data_monthly = dr.monthlySummary(stationIDs = stationIDs, parameter = 'avgt'
##    , reduceCode = 'mean' )
##    print data_monthly


    #Annual Summary
##    data_annual = dr.yearlySummary(stationIDs = stationIDs, parameter = 'avgt', reduceCode = 'mean')
##    print(data_annual.metadata)
##    print(data.getStationData(stationID))
##    print(data.keys())
##    print(data_annual)