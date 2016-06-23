import json

try:    #python 2.x
    import urllib2, urllib
    from StationDict import StationDict
    from ACIS import ACIS
    import hucs
    pyVersion = 2
except:     #python 3.x
    import urllib.request
    import urllib.parse
    from .ACIS import ACIS
    from .StationDict import StationDict
    pyVersion = 3

class StationFinder(ACIS):
    '''
    INFO
    -------
    Methods
    *findStation


    '''
    def __init__(self, *args, **kwargs):
        super(StationFinder,self).__init__(*args, **kwargs)
        self.webServiceSource = 'StnMeta'

    def findStation(self, unitCode = None, distance = 30,
        parameter = None, filePathAndName = None):
        '''
        INFO
        ----
        Standard method to find all stations and associated metadata
        based on zero or more criteria.


        ARGUMENTS
        ---------
        unitCode - 4-Letter park code (searches for station within buffer)
        distaince -
        parameter - Parameter code for weather element (e.g., tmin)


        RETURNS
        -------
        A station info object of station metadata
        '''
        metadata = ['uid', 'name', 'state', 'll', 'elev', 'valid_daterange', 'sids']
        if not parameter:
            parameter = ['pcpn', 'snwd', 'avgt', 'obst', 'mint', 'snow', 'maxt']

        if unitCode:
            bbox = self._getBoundingBox(unitCode, distance)

        self.input_dict = {}    #Clears the input dictionary
        results =  self._call_ACIS(elems = parameter
            ,bbox = bbox
            ,meta = metadata
            ,unitCode = unitCode)


        si =  StationDict(results, queryParams = self.input_dict)
        if filePathAndName:
                si.export(filePathAndName)
        return si



    def _getBoundingBox(self, unitCode, distanceKM = None):
        '''
        Calls IRMA Unit Service to get bounding box for NPS unit
        Converts buffer to KM based on 0.011
        Formats String to 'West, South, East, North'
        '''
        connection = urllib2.urlopen('http://irmaservices.nps.gov/v2/rest/unit/' + unitCode + '/geography?detail=envelope&dataformat=wkt&format=json')
        geo = json.loads(connection.read())[0]['Geography'][10:-2].split(',')
        west = float(geo[0].split()[0])
        east = float(geo[1].split()[0])
        north = float(geo[2].split()[1])
        south = float(geo[0].split()[1])

        if distanceKM:
            bufr = float(distanceKM)*0.011
            west+=bufr
            east-=bufr
            south-=bufr
            north+=bufr
        return str(west) + ', ' + str(south) + ',' + str(east) + ',' + str(north)

##    def HUCs(self):
##        '''
##        Returns all of the HUC Codes
##        '''
##        return hucs.hucs
##
##    def countyCodes(self, state = None):
##        fipCode = []
##        if pyVersion == 2:
##            data = urllib2.urlopen('http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt')
##        elif pyVersion == 3:
##            data = urllib.request.urlopen('http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt')
##        for line in data.readlines():
##            line = str(line).split(',')
##            if state:
##                if line[0] == state:
##                    fipCode.append(line[3] + ', ' + line[0] + ' : ' + line[1] + line[2])
##            else:
##                fipCode.append(line[0] + ',' + line[3] + ' : ' + line[1] + line[2])
##        return fipCode

if __name__ == '__main__':
    c = StationFinder()
    print c._getBoundingBox('ACAD', distanceKM = 30)
    stationInfo = c.findStation(unitCode = 'NOCA', filePathAndName  = 'C:\\TEMP\\test.csv')
    print stationInfo.metadata



##    print (c.countyCodes(state =  'CO'))
##    print (c.countyCodes('CO'))
##    print(c.parameters)
##    stationInfo =  c.find(parameter = 'avgt', countyCode = '08117', startDate = '1980-01-01', endDate = '1981-12-31')
    ##print stationInfo.toGeoJSON()
##    stationInfo =  c.findStation( countyCode = '08117')
##    stationInfo = c.findStation(HUC = '14010002, 14010002', parameter = 'avgt')
##    print(len(stationInfo.stationIDs))
##    print(stationInfo.metadata)
##    print c.HUCs()[0:5]

##    print stationIndo.stationIDs
