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
        #additional metadata elements to request along with the data
        metaElements = ['uid', 'll', 'name', 'elev', 'sids', 'state']

        #build the elems objects, which ACIS requires for more complex queries
        elems = []
        for p in self.climateParameters:
            arguments = {'name': p, 'interval': self.interval, 'add': self.add
             ,'duration': self.duration,'maxmissing': self.maxMissing}
            elems.append(arguments)

        #Update the elems object to add all variations of parameters and reduce
        # codes, where applicable
        # Too bad ACIS just doesn't just ignore reduce codes where not applicable
        if self.reduceCodes:
            rcelems = []
            for k in elems:
                for rd in self.reduceCodes:
                    k['reduce'] = {'reduce': rd, 'add':self.add}
                    rcelems.append(k.copy())
            elems = rcelems

        #Add all variations of climate parameters and reduce codes to a list
        #This list is used to help instantaite the station dictionary object
        if self.reduceCodes:
            cp = [k['name'] + '_' + k['reduce']['reduce'] for k in elems]
        else:
            cp = self.climateParameters[:]

        #Instantiate the station dictionary object
        sd = self.StationDictClass(climateParameters = cp, queryParameters = None
            , dateInterval = self.duration, aggregation = self.reduceCodes)

        #Iterate over all stationIDs and query ACIS for data. Add the station response
        #to the station dictionary object
        for uid in self.stationIDs:
            response = self._call_ACIS(uid = uid, elems = elems,
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
        self.StationDictClass = DailyStationDict
        self.duration = 'dly'
        self.interval = 'dly'
        self.stationIDs = self._extractStationIDs(climateStations)
        self._formatClimateParameters(climateParameters)
        sdate = self._formatDate(sdate)
        edate = self._formatDate(edate)
        self.reduceCodes = None
        self.maxMissing = 0
        self.filePathAndName = filePathAndName
        self.add = 'f,s'

        return self._fetchStationDataFromACIS(sdate = str(sdate),
            edate = str(edate))

    def getMonthlyWxSummaryByYear(self, climateStations, climateParameters = None
            ,reduceCodes = None, sdate = 'por', edate = 'por', maxMissing = 1
            ,filePathAndName = None):
        '''
        Returns the monthly summaries/aggregates of weather observations for one or more stations.
        # of observations is returned

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
        Returns object that contains station metadata and the monthly weather summaries

        '''
        self.StationDictClass = MonthlyStationDict
        sdate = self._formatDate(sdate)
        edate = self._formatDate(edate)
        self.duration = 'mly'
        self.interval = 'mly'
        self.reduceCodes = self._formatReduceCodes(reduceCodes)
        if not maxMissing:
            self.maxMissing = 1
        else:
            self.maxMissing =  maxMissing
        self.filePathAndName = filePathAndName
        self.add = 'mcnt'

        self.stationIDs = self._extractStationIDs(climateStations)
        self._formatClimateParameters(climateParameters)

        return self._fetchStationDataFromACIS(sdate = str(sdate),
            edate = str(edate))


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
    #MONTHLY DATA
    monthlyData = dr.getMonthlyWxSummaryByYear(climateStations = stationIDs,
        reduceCodes = 'mean, max', climateParameters = 'avgt, mint'
        , sdate = 'por', edate = 'por' )
    print (monthlyData)
    monthlyData.export(r'C:\TEMP\data.csv')


    sf = StationFinder()
    YELL_Stations = sf.findStation(unitCode = 'YELL', climateParameters = 'mint, maxt',
        sdate = '2015-01-01', edate = '2015-03-31')

    #get monthly summary for minimum and maximum temperature for the Yellowstone Stations
    # from January 2015 to March 2015. Use default of maximum missing days of 1.
    wxData = dr.getMonthlyWxSummaryByYear(climateStations = YELL_Stations,
<<<<<<< HEAD
        climateParameters = 'mint, maxt', reduceCodes = None
=======
        climateParameters = 'mint, maxt', reduceCodes = 'min'
>>>>>>> 7cf1e2e3cfb29506783f20cd7085eeae19b2ba4f
        , sdate = '2015-01', edate = '2015-03')

    print (wxData)


    ###########################################################################
    #DAILY DATA
    dailyData = dr.getDailyWxObservations(climateStations = stationIDs
        , climateParameters = 'avgt, mint'
        , sdate = '20120101', edate = '2012-01-05' )
    dailyData.exportData(filePathAndName = r'dailyData.csv')

    #GET DATA for a single station
    dailyData = dr.getDailyWxObservations(climateStations = 77572
        , sdate = 20160101, edate = '20160105' )

    #Print the station data to the screen
    print (dailyData)

    #get data for stations returned in station search
    stationList = sf.findStation(unitCode = 'GRKO', distance = 10)
    wxData = dr.getDailyWxObservations(climateStations = stationList,
        climateParameters = 'pcpn'
        ,sdate = '2015-08-01', edate = '2015-08-04')
    print (wxData)
    print (wxData.stationCounts)


