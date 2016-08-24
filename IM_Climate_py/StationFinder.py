import json
import urllib2

import StationDict
reload(StationDict)
from StationDict import StationDict
from ACIS import ACIS
from Station import Station
import common

class StationFinder(ACIS):
    '''
    INFO
    -------
    Object to find weather stations using ACIS Web Services.


    '''
    def __init__(self, *args, **kwargs):
        super(StationFinder, self).__init__(*args, **kwargs)
        self.webServiceSource = 'StnMeta'

    def findStation(self, unitCode = None, distance = 0,
        climateParameters = None, sDate = None, eDate = None
        ,filePathAndName = None):
        '''
        INFO
        ----
        Standard method to find all stations and associated metadata
        based on zero or more criteria.


        ARGUMENTS
        ---------
        unitCode           4-Letter park code (searches for station within buffer)

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

        if unitCode:
            bbox = common.getBoundingBox(unitCode, distance)

        results =  self._call_ACIS(elems = climateParameters
            ,bbox = bbox, sDate = sDate, eDate = eDate
            ,meta = metadata)

        #adds unitCode to input_dict following the call to ACIS
        if unitCode:
            self._input_dict['unitCode'] = unitCode

        si =  StationDict(queryParameters = self._input_dict, climateParameters = climateParameters)
        for station in results['meta']:
            station['unitCode'] = unitCode
            si._addStation(Station, stationID = station['uid'], stationMeta = station)
        if filePathAndName:
                si.exportMeta(filePathAndName)
        return si





if __name__ == '__main__':
    sf = StationFinder()

    wxStations = sf.findStation(unitCode = 'NOCA', filePathAndName  = 'C:\\TEMP\\test.csv', sDate = '1940-01-01', eDate = '1940-01-01')
    print wxStations.queryParameters
    print wxStations
    print sf.supportedParameters
    print wxStations[26202].validDateRange
    print wxStations[26202].validDateRange.keys()

    wxStations = sf.findStation(unitCode = 'ROMO', climateParameters = 'mint, maxt,pcpn')
    print wxStations
    print wxStations[48106].validDateRange
    print wxStations[48106].validDateRange['pcpn']




