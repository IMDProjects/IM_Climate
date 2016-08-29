import urllib2
import json
from ACIS import ACIS


missingValue = 'NA'

def getSupportedParameters():
    acis = ACIS()
    return acis.supportedParameters

def getBoundingBox(unitCode, distanceKM = None):
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
    distanceKM = str(distanceKM)
    connection = urllib2.urlopen('http://irmaservices.nps.gov/v2/rest/unit/' + unitCode + '/geography?detail=envelope&dataformat=wkt&format=json')
    geo = json.loads(connection.read())[0]['Geography'][10:-2].split(',')
    west = float(geo[0].split()[0])
    east = float(geo[1].split()[0])
    north = float(geo[2].split()[1])
    south = float(geo[0].split()[1])

    if distanceKM:
        bufr = float(distanceKM)*0.011
        west-=bufr
        east+=bufr
        south-=bufr
        north+=bufr
    return str(west) + ', ' + str(south) + ',' + str(east) + ',' + str(north)

if __name__=='__main__':
    print missingValue
    print getSupportedParameters()
    print getBoundingBox('ACAD',0)
