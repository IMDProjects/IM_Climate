from ACIS import ACIS
from Station import Station
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

    def getDailyWxObservations(self, climateStations, climateParameters = None, sdate = 'por',
            edate = 'por', filePathAndName = None):
        '''
        INFO
        -----
        Returns the daily weather observations for one or more stations.
        Flags and time of observation, if they exist, are also returned.

        ARGUMENTS
        ---------



        climateStations -               The ACIS uids. These can either be a single station (int or string),
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
        metaElements = ['uid', 'll', 'name', 'elev', 'sids', 'state'] #additional metadata elements to request along with the data
        self.duration = 'dly'
        self.stationIDs = self._extractStationIDs(climateStations)
        self.climateParameters = self._formatClimateParameters(climateParameters)
        self.reduceCode = None

        results =  self._fetchStationDataFromACIS(sdate = str(sdate),
            edate = str(edate), meta = metaElements)

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
            sd._addStation(stationSubClass = Station,  stationID = uid, stationMeta = response['meta']
                , stationData = response.get('data', 'error'))

        return sd


if __name__=='__main__':

    stationIDs = [66180, 67175]

    dr = DataRequestor()

    #Daily Data
    dailyData = dr.getDailyWxObservations(climateStations = stationIDs, climateParameters = 'avgt, mint'
        , sdate = '20120101', edate = '2012-01-05' )
    dailyData.exportData(filePathAndName = r'dailyData.csv')

    #GET DATA for a single station
    dailyData = dr.getDailyWxObservations(climateStations = 77572, sdate = 20160101, edate = '20160105' )

    #Print the station data to the screen
    print dailyData

    #get data for stations returned in station search
    from StationFinder import StationFinder
    sf = StationFinder()
    stationList = sf.findStation(unitCode = 'AGFO', distance = 10)
    dr = DataRequestor()
    wxData = dr.getDailyWxObservations(climateStations = stationList,
        climateParameters = 'pcpn'
        ,sdate = '2015-08-01', edate = '2015-08-04')
    print wxData
    print wxData.stationCounts


