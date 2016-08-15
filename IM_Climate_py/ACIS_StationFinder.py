import json
import urllib2

import StationDict
reload(StationDict)
from StationDict import StationDict
from ACIS import ACIS
from ACIS_Station import ACIS_Station

class ACIS_StationFinder(ACIS):
    '''
    INFO
    -------
    Object to find weather stations using ACIS Web Services.


    '''
    def __init__(self, *args, **kwargs):
        super(StationFinder,self).__init__(*args, **kwargs)
        self.webServiceSource = 'StnMeta'

    def findStation(self, parkCodes = None, distance = 0,
        climateParameters = None, sDate = None, eDate = None
        ,filePathAndName = None):
        '''
        INFO
        ----
        Standard method to find all stations and associated metadata
        based on zero or more criteria.


        ARGUMENTS
        ---------
        parkCodes           4-Letter park code (searches for station within buffer)

        distance            buffer distance around the provided unitCode (if provided).
                            Default is 0 km.

        climateParameters    Parameter code for climate/weather element (e.g., mint, avgt, pcpn)

        sDate               (Optional) - Start date as yyyy-mm-dd or yyyymmdd.
                             If not provided, the default is the period of record.

        eData               (Optional) - End date as yyyy-mm-dd or yyyymmdd.
                             If not provided, the default is the period of record

        filePathAndName    If provided, a csv text file is saved to specific location.

        RETURNS
        -------
        An object of station metadata (See StationDict.py)
        '''
        metadata = ['uid', 'name', 'state', 'll', 'elev', 'valid_daterange', 'sids']
        if not climateParameters:
            climateParameters = ['pcpn', 'snwd', 'avgt', 'obst', 'mint', 'snow', 'maxt']
        else:
            climateParameters = climateParameters.replace(' ','')

        if parkCodes:
            bbox = self._getBoundingBox(parkCodes, distance)

        self._input_dict = {}    #Clears the input dictionary
        results =  self._call_ACIS(elems = climateParameters
            ,bbox = bbox, sDate = sDate, eDate = eDate
            ,meta = metadata)

        #adds parkCodes to input_dict following the call to ACIS
        if parkCodes:
            self._input_dict['parkCodes'] = parkCodes

        si =  StationDict(queryParameters = self._input_dict, climateParameters = climateParameters)
        for station in results['meta']:
            si._addStation(ACIS_Station, stationID = station['uid'], stationMeta = station)
        if filePathAndName:
                si.exportMeta(filePathAndName)
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
    sf = ACIS_StationFinder()

    #wxStations = sf.findStation(parkCodes = 'NOCA', filePathAndName  = 'C:\\TEMP\\test.csv', sDate = '1940-01-01', eDate = '1940-01-01')
    #print wxStations.queryParameters
    #print wxStations
    #print sf.supportedParameters
    #print wxStations[26202].validDateRange
    #print wxStations[26202].validDateRange.keys()

    wxStations = sf.findStation(parkCodes = 'ROMO', climateParameters = 'mint, maxt,pcpn')
    #print wxStations
    print wxStations[48106].validDateRange
    print wxStations[48106].validDateRange['pcpn']




