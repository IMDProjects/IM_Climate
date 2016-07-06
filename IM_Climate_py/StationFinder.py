import json
import urllib2

from StationDict import StationDict
from ACIS import ACIS

class StationFinder(ACIS):
    '''
    INFO
    -------
    Object to find weather stations.


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
        distance - buffer distance around the provided unitCode (if provided).
                    Default is 30 km.
        parameter - Parameter code for weather element (e.g., tmin)
        filePathAndName - If provided, a csv text file is saved to specific location.

        RETURNS
        -------
        An object of station metadata (See StationDict.py)
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

        si =  StationDict(results, queryParameters = self.input_dict)
        if filePathAndName:
                si.export(filePathAndName)
        return si


    def _getBoundingBox(self, unitCode, distanceKM = None):
        '''
        INFO
        ----
        Calls NPS IRMA Unit Service to get bounding box for respective NPS unit
        Converts buffer to KM based on 0.011
        Formats String to 'West, South, East, North'

        ARGUMENTS
        ---------
        unitCode - 4-letter park code
        distanceKM - distance to buffer park boundary
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


if __name__ == '__main__':
    c = StationFinder()
    print c._getBoundingBox('ACAD', distanceKM = 30)
    stationInfo = c.findStation(unitCode = 'NOCA', filePathAndName  = 'C:\\TEMP\\test.csv')
    print stationInfo.queryParameters


