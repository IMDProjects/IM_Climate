from ACIS import ACIS
from StationDict import StationDict
from WxOb import DailyWxOb, MonthlyWxOb


class StationDataRequestor(ACIS):
    '''
    INFO
    ----
    Object to request weather data using ACIS web services

    '''
    def __init__(self):
        super(StationDataRequestor,self).__init__()
        self.webServiceSource = 'StnData'

    def _fetchStationDataFromACIS(self, **kwargs):
        '''
        INFO
        ----
        Makes data requests using one or more stationIDs. Adds information for
        each station (i.e., station meta and data) to the StationDict object.

        RETURNS
        -------
        StationDict object

        '''
        #additional metadata elements to request along with the data
        metaElements = ('uid', 'll', 'name', 'elev', 'sids', 'state')

        kwargs = self._formatArguments(kwargs, meta = metaElements)

        #Instantiate the station dictionary object
        sd = StationDict(observationClass = self.observationClass, climateParameters = self.updatedClimateParameters,
            queryParameters = None, dateInterval = self.duration
            , aggregation = self.reduceCodes)

        #Iterate over all stationIDs and query ACIS for data. Add the station response
        #to the station dictionary object
        for uid in self.stationIDs:
            response = self._call_ACIS(uid = uid, kwargs = kwargs)
            self._checkResponseForErrors(response)
            sd._addStation(stationID = uid, stationMeta = response['meta']
                    , stationData = response.get('data', 'error'))

        #Export data to a file if the file path and name are provided
        if self.filePathAndName:
            sd.exportData(filePathAndName = self.filePathAndName)
        return sd

    def getDailyWxObservations(self, climateStations, climateParameters = None
            ,sdate = 'por', edate = 'por', includeNormals = False
            ,includeNormalDepartures = False, filePathAndName = None):
        '''
        INFO
        -----
        Returns the daily weather observations for one or more stations.
        Flags and time of observation, if they exist, are also returned.

        ARGUMENTS
        ---------



        climateStations                 The ACIS uids. These can either be a single station (int or string),
                                        a list of stationIDs, or the StationDict object returned
                                        from the StationFinder.FindStation method.

        climateParameters (optional)    The weather parameters to fetch. Valid parameters
                                        can be found by accesssing the supportedParamters property.
                                        Note that ACIS vernacular for climate parameter is element.

        sdate (optional)                Start Date -  YYYY-MM-DD OR YYYYMMDD (default is period of record)

        edate (optional)                End Date - YYYY-MM-DD OR YYYYMMDD (default is period of record)

        includeNormals (optional)       If True, then include the daily normals

        includeNormalDepartures (opt)   If True, then include the daily departues from normal

        filePathAndName (optional)      Location and name of CSV text file to save

        RETURNS
        -------
        Returns object that contains station metadata and the daily weather observations and
        and all associated flags

        '''
        self.duration = 'dly'
        self.interval = 'dly'
        self.add = 'f,s'
        self.observationClass = DailyWxOb
        self.reduceCodes = []

        return self._fetchStationDataFromACIS(sdate = str(sdate),
            edate = str(edate), climateStations = climateStations,
            climateParameters = climateParameters,
            filePathAndName = filePathAndName, reduceCodes = self.reduceCodes,
            includeNormals = includeNormals, includeNormalDepartures = includeNormalDepartures)

    def getMonthlyWxSummaryByYear(self, climateStations, climateParameters = None
            ,reduceCodes = None, sdate = 'por', edate = 'por', maxMissing = 1
            ,includeNormals = False, includeNormalDepartures = False, filePathAndName = None):
        '''
        Returns the monthly summaries/aggregates of weather observations for one or more stations
        by month over 1 or more years

        ARGUMENTS
        ---------

        climateStations                 One or more station identifiers (uids)
                                        passed either as a list or the response
                                        object from the station finder.

        climateParameters (optional)    The weather parameters to fetch. Valid parameters
                                        can be found by accesssing the supportedParamters property.
                                        Note that ACIS vernacular for climate parameter is element.

        reduceCodes (optional)          The method used to summarize the daily observations into monthly
                                        values. Current options inlcude max, min, sum and
                                        mean. If none are provided, then all are returned.

        sdate (optional)                Start Date - YYYY-MM-DD OR YYYYMMDD (default is period of record)

        edate (optional)                End Date - YYYY-MM-DD OR YYYYMMDD (default is period of record)

        maxMissing (optional)           Maximum number of missing days within a month
                                        before a missing value is returned (default is 1, or approximately
                                        3.3% missing days within a month)

        includeNormals (optional)       If True, then include the monthly normals

        includeNormalDepartures (opt)   If True, then include the monthly departues from normal

        filePathAndName (optional)      Location and name of CSV text file to save

        RETURNS
        -------
        Returns object that contains station metadata and the  weather summaries
        by year and month (total of year x month values)

        '''
        self.duration = 'mly'
        self.interval = 'mly'
        self.add = 'mcnt'
        self.observationClass = MonthlyWxOb


        return self._fetchStationDataFromACIS(sdate = sdate
            ,edate = str(edate), reduceCodes = reduceCodes, maxmissing = maxMissing
            ,filePathAndName = filePathAndName, climateStations = climateStations
            ,climateParameters = climateParameters, includeNormals = includeNormals
            ,includeNormalDepartures = includeNormalDepartures)


    def getYearlyWxSummary(self, climateStations, climateParameters = None
            ,reduceCodes = None, sdate = 'por', edate = 'por', maxMissing = None
            ,includeNormals = False, includeNormalDepartures = False, filePathAndName = None):
        '''
        Returns the annual/yearly summaries/aggregates of weather observations for one or more stations


        ARGUMENTS
        ---------

        climateStations                 One or more station identifiers (uids)
                                        passed either as a list or the response
                                        object from the station finder.

        climateParameters (optional)    The weather parameters to fetch. Valid parameters
                                        can be found by accesssing the supportedParamters property.
                                        Note that ACIS vernacular for climate parameter is element.

        reduceCodes (optional)          The method used to summarize the daily observations into monthly
                                        values. Current options inlcude max, min, sum and
                                        mean. If none are provided, then all are returned.

        sdate (optional)                Start Date - YYYY-MM-DD OR YYYYMMDD (default is period of record)

        edate (optional)                End Date - YYYY-MM-DD OR YYYYMMDD (default is period of record)

        maxMissing (optional)           Maximum number of missing days within a month
                                        before a missing value is returned (default is 1, or approximately
                                        3.3% missing days within a month)

        includeNormals (optional)       If True, then include the monthly normals

        includeNormalDepartures (opt)   If True, then include the monthly departues from normal

        filePathAndName (optional)      Location and name of CSV text file to save

        RETURNS
        -------
        Dictionary-like bject that contains station metadata and the annual climate
        aggregates

        '''
        self.duration = 'yly'
        self.interval = 'yly'
        self.add = 'mcnt'
        self.observationClass = MonthlyWxOb


        return self._fetchStationDataFromACIS(sdate = sdate
            ,edate = str(edate), reduceCodes = reduceCodes, maxmissing = maxMissing
            ,filePathAndName = filePathAndName, climateStations = climateStations
            ,climateParameters = climateParameters, includeNormals = includeNormals
            ,includeNormalDepartures = includeNormalDepartures)


    def getDayCountByThreshold(self, climateStations, climateParameters, thresholdType
            ,thresholdValue, duration, sdate = 'por', edate = 'por', filePathAndName = None):
        '''
        Returns the count of days per year above/below threshold


        ARGUMENTS
        ---------

        climateStations                 One or more station identifiers (uids)
                                        passed either as a list or the response
                                        object from the station finder.

        climateParameters               One or more weather parameters (of the same unit - eg., fahrenheit).
                                        Valid parameters can be found by accesssing the supportedParamters property.
                                        Note that ACIS vernacular for climate parameter is element.

        thresholdType                   gt (greater than); ge (greater than equal to); lt (less than)
                                        le (less than equal to); eq (equal to); ne (not equal to)

        thresholdValue                  The method used to summarize the daily observations into monthly
                                        values. Current options inlcude max, min, sum and
                                        mean. If none are provided, then all are returned.

<<<<<<< HEAD
    #########################################################################
##    #DAILY DATA
##    dailyData = dr.getDailyWxObservations(climateStations = stationIDs
##        , climateParameters = 'avgt, mint'
##        , sdate = '20120101', edate = '2012-01-05' )
##    dailyData.exportData(filePathAndName = r'dailyData.csv')
##
##    #GET DATA for a single station
##    dailyData = dr.getDailyWxObservations(climateStations = 77572
##        , sdate = 20160101, edate = '20160105' )
##
##    #Print the station data to the screen
##    print (dailyData)
##
##    #get data for stations returned in station search
##    stationList = sf.findStation(unitCode = 'GRKO', distance = 10)
##    wxData = dr.getDailyWxObservations(climateStations = stationList,
##        climateParameters = 'pcpn'
##        ,sdate = '2015-08-01', edate = '2015-08-04')
##    print (wxData)
##    print (wxData.stationCounts)
=======
        duration                        mly = by month | yly = by year

        sdate (optional)                Start Date - YYYY-MM OR YYYYMM (default is period of record)

        edate (optional)                End Date - YYYY-MM OR YYYYMM (default is period of record)


        filePathAndName (optional)      Location and name of CSV text file to save


        '''
        self.duration = duration
        self.interval = duration
        self.reduceCodes = ['cnt_' +  str(thresholdType) + '_' + str(thresholdValue)]
        self.observationClass = MonthlyWxOb
        self.add = 'mcnt'

        return self._fetchStationDataFromACIS(sdate = sdate
            ,edate = str(edate), reduceCodes = self.reduceCodes
            ,filePathAndName = filePathAndName, climateStations = climateStations
            ,climateParameters = climateParameters)

    def getWxObservations(self, duration, climateStations, climateParameters = None
        ,sdate = 'por', edate = 'por', reduceCodes = None, maxMissing = 1,
        filePathAndName = None):

        if duration == 'dly':
            self.getDailyWxObservations( climateStations = climateStations, climateParameters = climateParameters
                        ,sdate = sdate, edate = edate, filePathAndName = filePathAndName)
        elif duration == 'mly':
            self.getMonthlyWxSummaryByYear(climateStations = climateStations, climateParameters = climateParameters
                         ,reduceCodes = reduceCodes, sdate = sdate, edate = edate, maxMissing = maxMissing
                         ,filePathAndName = filePathAndName)
        elif duration == 'yly':
            self.getYearlyWxSummary(self, climateStations = climateStations, climateParameters = climateParameters
                         ,reduceCodes = reduceCodes, sdate = sdate, edate = edate, maxMissing = maxMissing
                         ,filePathAndName = filePathAndName)
        else:
            raise Exception('Invalid duration code: ' + duration )


if __name__=='__main__':

    from StationFinder import StationFinder
    stationIDs = '66180, 67175'

    dr = StationDataRequestor()
    sf = StationFinder()
##    ############################################################################
    # DAY COUNTS BY THRESHOLD
##    yearlyCounts= dr.getDayCountByThreshold(climateStations = 29699,
##         climateParameters = 'maxt',  thresholdType = 'eq'
##        ,thresholdValue = 90,  timeInterval = 'yly'
##        ,sdate = 1980, edate = 1985)
##    print (yearlyCounts)
##
##    yearlyCounts= dr.getDayCountByThreshold(climateStations = 29699,
##         climateParameters = 'mint',  thresholdType = 'le'
##        ,thresholdValue = 10,  timeInterval = 'yly'
##        ,sdate = 1980, edate = 1985)
##    print (yearlyCounts)

##
##    ############################################################################
    #YEARLY DATA
    #INCLUDE NORMALS
##    yearlyData = dr.getYearlyWxSummary(climateStations = 29699,
##        reduceCodes = 'mean', climateParameters = 'maxt'
##        , sdate = '1980', edate = '2004', includeNormals = True
##        ,includeNormalDepartures = True)
##    print (yearlyData)


##    ###########################################################################
    #MONTHLY DATA BY YEAR
##    monthlyData = dr.getMonthlyWxSummaryByYear(climateStations = stationIDs,
##        reduceCodes = 'mean, max', climateParameters = 'avgt, mint'
##        , sdate = '2007-01-01', edate = '2007-05-01', maxMissing = 0 )
##    print (monthlyData)

    #INCLUDE NORMALS
##    monthlyData = dr.getMonthlyWxSummaryByYear(climateStations = 29699,
##        reduceCodes = 'mean', climateParameters = 'maxt'
##        , sdate = '2003-01', edate = '2003-01', includeNormals = True
##        ,includeNormalDepartures = True)
##    print (monthlyData)
##
##
##    sf = StationFinder()
##    YELL_Stations = sf.findStation(unitCode = 'YELL', climateParameters = 'mint, maxt',
##        sdate = '2015-01-01', edate = '2015-03-31')
##
##    #get monthly summary for minimum and maximum temperature for the Yellowstone Stations
##    # from January 2015 to March 2015. Use default of maximum missing days of 1.
##    wxData = dr.getMonthlyWxSummaryByYear(climateStations = YELL_Stations,
##        climateParameters = 'mint, maxt', reduceCodes = None
##        , sdate = '2015-01', edate = '2015-03')
##
##    print (wxData)
##
##    sf = StationFinder()
##    wxData = dr.getMonthlyWxSummaryByYear(climateStations = stationIDs,
##        climateParameters = 'mint, maxt', reduceCodes = None
##        , sdate = None, edate = '2015-03')
##    print (wxData)


    #########################################################################
    #DAILY DATA
##    dailyData = dr.getDailyWxObservations(climateStations = stationIDs
##        , climateParameters = 'avgt, mint'
##        , sdate = '20120101', edate = '2012-01-05' )
##    print dailyData
##
##    #INCLUDE DAILY NORMALS
##    dailyData = dr.getDailyWxObservations(climateStations = 29699
##        , climateParameters = 'mint'
##        , sdate = '20120101', edate = '2012-03-30', includeNormals = True,
##        includeNormalDepartures = True )
##    print dailyData
##
##
##    #GET DATA for a single station
##    dailyData = dr.getDailyWxObservations(climateStations = 77572
##        , sdate = 20160101, edate = '20160105' )
##
##    #Print the station data to the screen
##    print (dailyData)
##
##    #get data for stations returned in station search
##    sf = StationFinder()
##    stationList = sf.findStation(unitCode = 'GRKO', distance = 10)
##    wxData = dr.getDailyWxObservations(climateStations = stationList,
##        climateParameters = 'pcpn'
##        ,sdate = '2015-08-01', edate = '2015-08-04')
##    print (wxData)
##    print (wxData.stationCounts)
##
##    #Export Daily data to data.csv
##    dailyData = dr.getDailyWxObservations(climateStations = '29699'
##        , climateParameters = 'maxt'
##        , sdate = '2003-01-01', edate = '2004-12-31' )
##    print dailyData
##    dailyData.export(r'C:\TEMP\data.csv')


    #another test
    stationList = sf.findStation(unitCode = 'CAHA', distance = 10, climateParameters = ['pcpn', 'mint', 'maxt'])
    dailyData = dr.getDailyWxObservations(climateStations = stationList
        , climateParameters = ['pcpn', 'mint', 'maxt'], sdate = 'por', edate = 'por')
    dailyData.export(r'C:\TEMP\test.txt')
