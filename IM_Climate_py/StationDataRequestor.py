from ACIS import ACIS
from StationDict import DailyStationDict, MonthlyStationDict


class StationDataRequestor(ACIS):
    '''
    INFO
    ----
    Object to request weather data using ACIS web services

    '''
    def __init__(self, *args, **kwargs):
        super(StationDataRequestor,self).__init__(*args, **kwargs)
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
        #clean up some of the kwargs
        kwargs['sdate'] = self._formatDate(kwargs.get('sdate', None))
        kwargs['edate'] = self._formatDate(kwargs.get('edate', None))
        kwargs['maxmissing'] = self._formatMaxMissing(kwargs.get('maxmissing', None))

        #pop some of the kwargs that are not used directly in the ACIS call
        self.reduceCodes = self._formatReduceCodes(kwargs.pop('reduceCodes', None))
        self.filePathAndName =  kwargs.pop('filePathAndName', None)
        self.stationIDs = self._extractStationIDs(kwargs.pop('climateStations'))
        self._formatClimateParameters(kwargs.pop('climateParameters'))

        #additional metadata elements to request along with the data
        metaElements = ('uid', 'll', 'name', 'elev', 'sids', 'state')

        #do the complicated formatting of the elems list
        self._formatElems()

        #Instantiate the station dictionary object
        sd = self.StationDictClass(climateParameters = self.updatedClimateParameters,
            queryParameters = None, dateInterval = self.duration
            , aggregation = self.reduceCodes)

        #Iterate over all stationIDs and query ACIS for data. Add the station response
        #to the station dictionary object
        for uid in self.stationIDs:
            response = self._call_ACIS(uid = uid, elems = self.elems,
                 meta = metaElements, **kwargs)
            self._checkResponseForErrors(response)
            sd._addStation(stationID = uid, stationMeta = response['meta']
                    , stationData = response.get('data', 'error'))

        #Export data to a file if the file path and name are provided
        if self.filePathAndName:
            sd.exportData(filePathAndName = self.filePathAndName)
        return sd

    def getDailyWxObservations(self, climateStations, climateParameters = None
            , sdate = 'por', edate = 'por', filePathAndName = None):
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

        filePathAndName (optional)      Location and name of CSV text file to save

        RETURNS
        -------
        Returns object that contains station metadata and the daily weather observations and
        and all associated flags

        '''
        self.duration = 'dly'
        self.interval = 'dly'
        self.add = 'f,s'
        self.StationDictClass = DailyStationDict
        self.reduceCodes = []

        return self._fetchStationDataFromACIS(sdate = str(sdate),
            edate = str(edate), climateStations = climateStations,
            climateParameters = climateParameters,
            filePathAndName = filePathAndName, reduceCodes = self.reduceCodes)

    def getMonthlyWxSummaryByYear(self, climateStations, climateParameters = None
            ,reduceCodes = None, sdate = 'por', edate = 'por', maxMissing = 1
            ,filePathAndName = None):
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

        filePathAndName (optional)      Location and name of CSV text file to save

        RETURNS
        -------
        Returns object that contains station metadata and the  weather summaries
        by year and month (total of year x month values)

        '''
        self.duration = 'mly'
        self.interval = 'mly'
        self.add = 'mcnt'
        self.StationDictClass = MonthlyStationDict


        return self._fetchStationDataFromACIS(sdate = str(sdate),
            edate = str(edate), reduceCodes = reduceCodes, maxmissing = maxMissing
            , filePathAndName = filePathAndName, climateStations = climateStations
            ,climateParameters = climateParameters)


    def getMonthlyWxSummary(self, climateStations, climateParameters = None
            ,reduceCodes = None, sdate = 'por', edate = 'por', maxMissing = 1
            ,filePathAndName = None):
        '''
        Returns the monthly summaries/aggregates of weather observations
        for one or more stations.

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

        filePathAndName (optional)      Location and name of CSV text file to save

        RETURNS
        -------
        Returns object that contains station metadata and the weather
        summaries by month (total of 12 values)


        '''
        self.duration = 'mly'
        self.interval = "1"
        self.add = 'mcnt'
        self.StationDictClass = MonthlyStationDict

        return self._fetchStationDataFromACIS(sdate = str(sdate),
            edate = str(edate), reduceCodes = reduceCodes, maxmissing = maxMissing
            ,filePathAndName = filePathAndName, climateStations = climateStations
            ,climateParameters = climateParameters)



    def _extractStationIDs(self, stations):
        '''
        INFO
        ----
        If stations is a StationDict object, extracts list of stationIDs.
        Otherwise, assumes stationIDs to be a list, comma-delimited string,
        or a single stationID as a string.
        '''
        try:
            return stations.stationIDs
        except:
            return self._formatStringArguments(stations)

if __name__=='__main__':

    from StationFinder import StationFinder
    stationIDs = '66180, 67175'

    dr = StationDataRequestor()


    ###########################################################################
##    #MONTHLY DATA
##    monthlyData = dr.getMonthlyWxSummary(climateStations = stationIDs,
##        reduceCodes = 'max', climateParameters = 'mint'
##        , sdate = '2005-01', edate = '2016-05' )
##    print (monthlyData)
##    #monthlyData.export(r'C:\TEMP\data.csv')


##    ###########################################################################
    #MONTHLY DATA BY YEAR
    monthlyData = dr.getMonthlyWxSummaryByYear(climateStations = stationIDs,
        reduceCodes = 'mean, max', climateParameters = 'avgt, mint'
        , sdate = '2005-01-01', edate = '2016-05-01' )
    print (monthlyData)


    sf = StationFinder()
    YELL_Stations = sf.findStation(unitCode = 'YELL', climateParameters = 'mint, maxt',
        sdate = '2015-01-01', edate = '2015-03-31')

    #get monthly summary for minimum and maximum temperature for the Yellowstone Stations
    # from January 2015 to March 2015. Use default of maximum missing days of 1.
    wxData = dr.getMonthlyWxSummaryByYear(climateStations = YELL_Stations,
        climateParameters = 'mint, maxt', reduceCodes = None
        , sdate = '2015-01', edate = '2015-03')

    print (wxData)


##    #########################################################################
    #DAILY DATA
    dailyData = dr.getDailyWxObservations(climateStations = stationIDs
        , climateParameters = 'avgt, mint'
        , sdate = '20120101', edate = '2012-01-05' )
    print dailyData

    #GET DATA for a single station
    dailyData = dr.getDailyWxObservations(climateStations = 77572
        , sdate = 20160101, edate = '20160105' )

    #Print the station data to the screen
    print (dailyData)

    #get data for stations returned in station search
    sf = StationFinder()
    stationList = sf.findStation(unitCode = 'GRKO', distance = 10)
    wxData = dr.getDailyWxObservations(climateStations = stationList,
        climateParameters = 'pcpn'
        ,sdate = '2015-08-01', edate = '2015-08-04')
    print (wxData)
    print (wxData.stationCounts)


