try:    #python 2.x
    import urllib2, urllib
    from StationInfo import StationInfo
    from ACIS import ACIS
    import hucs
    pyVersion = 2
except:     #python 3.x
    import urllib.request
    import urllib.parse
    from .ACIS import ACIS
    from .StationInfo import StationInfo
    pyVersion = 3

class StationFinder(ACIS):
    def __init__(self, *args, **kwargs):
        super(StationFinder,self).__init__(*args, **kwargs)
        self.webServiceSource = 'StnMeta'
        self._initParkCodes()

    def find(self, parkCode = None, state = None, parameter = None, countyCode = None,
        bbox = None, HUC = None, startDate = None, endDate = None):
        '''
        INFO
        ----
        Standard method to find all stations and associated metadata
        based on zero or more criteria.
        If parameter is not specified, the valid_range will be for all parameters
        collected by the station. Likewise, if parameter(s) are specified,
        valid_range applies to the respective parameters only.

        ARGUMENTS
        ---------
        parkCode - 4-Letter park code (searches for station within buffer)
        state - Two-letter state acronym (e.g., CO)
        parameter - Parameter code for weather element (e.g., tmin)
        countyCode - County fips code (e.g., 08117)
        bbox - A latitude/longitude bounding box defined
            in decimal degrees (West, South, East, North) with negative
            values indicating west longitude and south latitude
            (e.g. -90.7, 40.5, -88.9, 41.5).
        HUC - One or more 8-digit hydrological units as a text string (e.g., '14010002,14010002')
        startDate -
        endDate -


        RETURNS
        -------
        A station info object of station metadata
        '''
        metadata = ['uid', 'name', 'state', 'll', 'elev', 'valid_daterange', 'sids']
        if not parameter:
            parameter = ['pcpn', 'snwd', 'avgt', 'obst', 'mint', 'snow', 'maxt']

        if parkCode:
            bbox = self.parkCodes[parkCode]

        self.input_dict = {}    #Clears the input dictionary
        results =  self._call_ACIS(state = state, elems = parameter
            ,county = str(countyCode), bbox = bbox, basin = str(HUC)
            ,meta = metadata)

        return StationInfo(results, queryParams = self.input_dict)

    def HUCs(self):
        '''
        Returns all of the HUC Codes
        '''
        return hucs.hucs

    def _initParkCodes(self):
        '''
        Pre-defines set of bounding boxes for all park codes
        '''
        self.parkCodes = {}
        self.parkCodes['NOCA'] = [-122, 48, -120, 49.5 ] #West, South, East, North

    def countyCodes(self, state = None):
        fipCode = []
        if pyVersion == 2:
            data = urllib2.urlopen('http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt')
        elif pyVersion == 3:
            data = urllib.request.urlopen('http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt')
        for line in data.readlines():
            line = str(line).split(',')
            if state:
                if line[0] == state:
                    fipCode.append(line[3] + ', ' + line[0] + ' : ' + line[1] + line[2])
            else:
                fipCode.append(line[0] + ',' + line[3] + ' : ' + line[1] + line[2])
        return fipCode

if __name__ == '__main__':
    c = StationFinder()
    print (c.countyCodes(state =  'CO'))
    print (c.countyCodes('CO'))
    print(c.parameters)
    stationInfo =  c.find(parameter = 'avgt', countyCode = '08117', startDate = '1980-01-01', endDate = '1981-12-31')
    print stationInfo.toGeoJSON()
    stationInfo =  c.find( countyCode = '08117')
    stationInfo = c.find(HUC = '14010002, 14010002', parameter = 'avgt')
    print(len(stationInfo.stationIDs))
    print(stationInfo.metadata)
    print c.HUCs()[0:5]
    stationIndo = c.find(parkCode = 'NOCA')
    print stationIndo.stationIDs
