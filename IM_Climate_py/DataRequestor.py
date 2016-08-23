from ACIS import ACIS
from ACIS_Station import ACIS_Station
from StationDict import StationDict


class DataRequestor(ACIS):
    '''
    INFO
    ----
    Object to request weather data using ACIS web services

    '''
    def __init__(self, *args, **kwargs):
        super(DataRequestor,self).__init__(*args, **kwargs)
        self.webServiceSource = 'StnData'

        self.reduceCodes = {'max': 'Maximum value for the period'
                , 'min':'Minimum value for the period'
                , 'sum' : 'Sum of the values for the period'
                , 'mean': 'Average of the values for the period'}

    def getDailyWxObservations(self, climateParameters, climateStations, startDate = 'por',
            endDate = 'por', filePathAndName = None):
        '''
        INFO
        -----
        Returns the daily weather observations for one or more stations.
        Flags and time of observation, if they exist, are also returned.

        ARGUMENTS
        ---------

        climateParameters   The weather parameters to fetch. Valid parameters
                            can be found by accesssing the supportedParamters property.
                            Note that ACIS vernacular for climate parameter is element.

        climateStations -   The ACIS uids. These can either be a single station (int or string),
                            a list of stationIDs, or the StationDict object returned
                            from the StationFinder.FindStation method.

        sdate (optional)    Start Date -  YYYY-MM-DD OR YYYYMMDD (default is period of record)
        edate (optional)    End Date - YYYY-MM-DD OR YYYYMMDD (default is period of record)
        filePathAndName (optional) - Location and name of CSV text file to save

        RETURNS
        -------
        Returns object that contains station metadata and the daily weather observations and
        and all associated flags

        '''
        metaElements = ['uid', 'll', 'name', 'elev', 'sids', 'state'] #additional metadata elements to request along with the data
        self.duration = 'dly'
        self.stationIDs = self._extractStationIDs(climateStations)
        self.climateParameters = climateParameters.replace(' ','').split(',')
        self.reduceCode = None

        results =  self._fetchStationDataFromACIS(sdate = str(startDate),
            edate = str(endDate), meta = metaElements)

        if filePathAndName:
            results.exportData(filePathAndName = filePathAndName)
        return results


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
        sd = StationDict(queryParameters = None, dateInterval = self.duration,
            aggregation = self.reduceCode, climateParameters = self.climateParameters)

        for uid in self.stationIDs:
            elems = []
            for p in self.climateParameters:
                elems.append({'name':p,'add':'f,s'})
            response = self._call_ACIS(uid = uid, elems = elems, **kwargs)
            sd._addStation(stationSubClass = ACIS_Station,  stationID = uid, stationMeta = response['meta']
                , stationData = response['data'])

        return sd

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


if __name__=='__main__':
    stationIDs = [66180, 67175]

    dr = DataRequestor()

    #Daily Data
    dailyData = dr.getDailyWxObservations(climateStations = stationIDs, climateParameters = 'avgt, mint'
        , startDate = '20120101', endDate = '2012-01-05' )
    dailyData.exportData(filePathAndName = r'dailyData.csv')

    #GET DATA for a single station
    dailyData = dr.getDailyWxObservations(climateStations = 77572, climateParameters = 'mint, maxt'
        , startDate = 20160101, endDate = '20160105' )

    #Print the station data to the screen
    print dailyData


