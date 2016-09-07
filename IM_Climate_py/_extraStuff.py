
    def getMonthlyGrids(self, gridSource, sDate, eDate,
            parkCodes = None, distance = 0,  climateParameters = None):

        self.gridSource = gridSource
        self.unitCode = unitCode
        self.climateParameters = climateParameters
        self.interval = 'mly'
        self.duration = 'mly'
        response = self._callForGrids()

    def getYearlyGrids(self, gridSource, sDate, eDate,
            parkCodes = None, distance = 0,  climateParameters = None):

        self.gridSource = gridSource
        self.unitCode = unitCode
        self.climateParameters = climateParameters
        self.interval = 'yly'
        self.duration = 'yly'
        response = self._callForGrids()
        print response




        self.reduceCodes = {'max': 'Maximum value for the period'
                , 'min':'Minimum value for the period'
                , 'sum' : 'Sum of the values for the period'
                , 'mean': 'Average of the values for the period'}


##    def monthySummaryByYear(self, stationIDs, parameter, reduceCode, startDate = 'por',
##         endDate = 'por', maxMissing = 1):
##
##        '''
##        INFO
##        -----
##        Monthly summary by year. Months with more than 1 missing day are not
##            calculated.
##
##        ARGUMENTS
##        ---------
##        stationID - The ACIS uid
##
##        parameter - The weather parameter to summarize. Valid parameters
##            can be found using the DataRequestor.paramter property.
##            Note that ACIS calls a parameter an element.
##
##        reduceCode - The method for reduction (i.e., aggregation).
##            Valid reduction codes can be found using the
##            DataRequestor.reductionCodes property.
##
##        startDate - Begin year and month of calculation (YYYY-MM).
##            Default is the period of record
##
##        endDate - End year and month of calculation (YYYY-MM).
##            Default is the period of record.
##
##        maxMissing -
##
##        RETURNS
##        -------
##
##        '''
##        self.duration = 'mly'
##        self.reduceCode = reduceCode
##        self.parameter = parameter
##        elems = self.duration + '_' + reduceCode +'_' + parameter
##        self.stationIDs = self._extractStationIDs(stationIDs)
##
##        return self._iterateOverStationIDs(sdate = startDate, edate = endDate, elems = elems
##             ,maxmissing = maxMissing)



##    def yearlySummary(self, stationIDs, parameter, reduceCode, startYear = 'por',
##         endYear = 'por'):
##
##        '''
##        INFO
##        -----
##        Calculates the annual weather element summary for a single station.
##        Years with more than 12 missing days are not calculated.
##
##        ARGUMENTS
##        ---------
##        station - The ACIS uid
##
##        parameter - The weather parameter to summarize. Valid parameters
##            can be found using the DataRequestor.paramter property.
##            Note that ACIS calls a parameter an element.
##
##        reduceCode - The method for reduction (i.e., aggregation).
##            Valid reduction codes can be found using the
##            DataRequestor.reductionCodes property.
##
##        startYear - Begin year of calculation. If beginYear is not provided,
##            it will degault to 30 years earlier than current year
##
##        endYear - End year of calculation. If endYear is not provided,
##            it will degault to current year.
##
##        RETURNS
##        -------
##        WxData, an extension to the dictionary object
##
##        '''
##        self.duration = 'yly'
##        self.reduceCode = reduceCode
##        self.parameter = parameter
##        self.stationIDs = self._extractStationIDs(stationIDs)
##
##        maxMissing = '12'
##
##        elems =  [{
##            'name': parameter,
##            'add': 'n',
##            'interval': self.duration,
##            'duration': self.duration,
##            'reduce': {
##                'reduce': self.reduceCode,
##                'add': 'mcnt'
##            },
##            'maxmissing': maxMissing,
##        }]
##
##        return self._iterateOverStationIDs(
##            sdate = startYear, edate = endYear,
##            elems = elems)
##
##    def climograph(self):
##        '''
##        INFO
##        ----
##        Pulls tmin, tmax, tavg and precipitation to support climograph
##        '''
##
##        pass
##
##
##    def monthlySummary(self, stationIDs, parameter, reduceCode, startDate = 'por',
##         endDate = 'por', maxMissing = 1):
##        '''
##        INFO
##        -----
##        Monthly summary computed for set of years (i.e, 12 one-month summaries).
##        Months with more than ??x%?? missing day are not calculated.
##
##        params = {"sid":"304174","sdate":"por","edate":"por","meta":["name","state"]
##        ,"elems":[{"name":"maxt","interval":"dly","duration":"dly","smry":{"reduce":"max","add":"date"}
##        ,"smry_only":1,"groupby":"year"}]}
##        '''
##        duration = 'dly'
##        #elems = duration + '_' + reduceCode +'_' + parameter
##
##        elems = [{"name":parameter,"interval":"mly","duration":"mly"
##                ,"smry_only":1,"groupby":"year"}]
##
##        return self._iterateOverStationIDs(sdate = startDate, edate = endDate,
##            elems = elems ,maxmissing = maxMissing)

