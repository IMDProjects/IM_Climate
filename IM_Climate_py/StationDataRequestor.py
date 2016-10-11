from ACIS import ACIS
import StationDict
reload(StationDict)
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
        metaElements = ['uid', 'll', 'name', 'elev', 'sids', 'state'] #additional metadata elements to request along with the data

        elems = []
        for p in self.climateParameters:
            arguments = {'name': p, 'interval': self.interval, 'add': self.add
             ,'duration': self.duration,'maxMissing': self.maxMissing}
            elems.append(arguments)

        #add all variations of parameters abd reduce codes, where applicable - too bad it isn't just ignored
        if self.reduceCodes:
            rcelems = []
            for rd in self.reduceCodes:
                for k in elems:
                    k['reduce'] = {'reduce': rd, 'add':self.add}
                    rcelems.append(k.copy())
            elems = rcelems

        cp = [k['name'] + '_' + k['reduce']['reduce'] for k in elems]
        #Instantiate the station dictionary object
        sd = self.StationDictClass(queryParameters = None, dateInterval = self.duration,
            aggregation = self.reduceCodes, climateParameters = cp)

        for uid in self.stationIDs:
            response = self._call_ACIS(uid = uid, elems = elems,
                 meta = metaElements, **kwargs)
            sd._addStation(stationID = uid, stationMeta = response['meta']
                , stationData = response.get('data', 'error'))

        if self.filePathAndName:
            sd.exportData(filePathAndName = self.filePathAndName)
        return sd


    def getDailyWxObservations(self, climateStations, climateParameters = None, sdate = 'por',
            edate = 'por', filePathAndName = None):
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
        self.climateParameters = self._formatClimateParameters(climateParameters)
        self.reduceCodes = None
        self.maxMissing = 0
        self.filePathAndName = filePathAndName
        self.add = 'f,s'

        return self._fetchStationDataFromACIS(sdate = str(sdate),
            edate = str(edate))

    def getMonthlySummaryByYear(self, climateStations, climateParameters = None, reduceCodes = None
            ,sdate = 'por', edate = 'por', maxMissing = 1, filePathAndName = None):
        '''
        Returns the monthly summaries of weather observations for one or more stations.
        # of observations is returned

        ARGUMENTS
        ---------

        climateStations                 The ACIS uids. These can either be a single station (int or string),
                                        a list of stationIDs, or the StationDict object returned
                                        from the StationFinder.FindStation method.

        climateParameters (optional)    The weather parameters to fetch. Valid parameters
                                        can be found by accesssing the supportedParamters property.
                                        Note that ACIS vernacular for climate parameter is element.

        reduceCodes (optional)          The method used to summarize the daily observations into monthly
                                        values. Current options inlcude max, min, sum
                                        mean, and stdev. If none are provided, then all are returned.

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
        self.duration = 'mly'
        self.interval = 'mly'
        self.reduceCodes = self._formatReduceCodes(reduceCodes)
        self.maxMissing =  maxMissing
        self.filePathAndName = filePathAndName
        self.add = 'mcnt'

        self.stationIDs = self._extractStationIDs(climateStations)
        self.climateParameters = self._formatClimateParameters(climateParameters)

        return self._fetchStationDataFromACIS(sdate = str(sdate),
            edate = str(edate))


    def _extractStationIDs(self, stations):
        '''
        INFO
        ----
        If stations is a StationDict object, extracts list of stationIDs.
        Otherwise, assumes stationIDs to be a list or a single stationID as a string.
        '''
        try:
            return stations.stationIDs
        except:
            if type(stations) == list:
                return stations
            else:
                return [stations]



if __name__=='__main__':

    stationIDs = [66180, 67175]

    dr = StationDataRequestor()

    #monthlyData
    monthlyData = dr.getMonthlySummaryByYear(climateStations = stationIDs,
        reduceCodes = 'mean, max', climateParameters = 'avgt, mint'
        , sdate = '2012-01-01', edate = '2013-01-01' )
    print (monthlyData)
    monthlyData.export(r'C:\TEMP\data.csv')

##    #Daily Data
##    dailyData = dr.getDailyWxObservations(climateStations = stationIDs, climateParameters = 'avgt, mint'
##        , sdate = '20120101', edate = '2012-01-05' )
##    dailyData.exportData(filePathAndName = r'dailyData.csv')
##
##    #GET DATA for a single station
##    dailyData = dr.getDailyWxObservations(climateStations = 77572, sdate = 20160101, edate = '20160105' )
##
##    #Print the station data to the screen
##    print (dailyData)
##
##    #get data for stations returned in station search
##    from StationFinder import StationFinder
##    sf = StationFinder()
##    stationList = sf.findStation(unitCode = 'AGFO', distance = 10)
##    dr = StationDataRequestor()
##    wxData = dr.getDailyWxObservations(climateStations = stationList,
##        climateParameters = 'pcpn'
##        ,sdate = '2015-08-01', edate = '2015-08-04')
##    print (wxData)
##    print (wxData.stationCounts)


