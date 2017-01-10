import urllib2
import json


missingValue = 'NA' #deines missing value for all modules

def getBoundingBox(unitCode = None, distanceKM = 0):
    '''
    INFO
    ----
    Calls NPS IRMA/FWS ECOS Unit Service to get bounding box for respective unit
    Converts buffer to KM based on 0.011
    Formats String to 'West, South, East, North'

    ARGUMENTS
    ---------
    unitCode - NPS/FWS unit code
    distanceKM - distance to buffer park boundary
    '''
    if not unitCode:
        return None
    #Test is alpha nps unit or alpha-numeric FWS Code
    if unitCode.isalpha():
        url = r'http://irmaservices.nps.gov/v2/rest/unit/'
    else:
        url = r'https://ecos.fws.gov/ServCatServices/v2/rest/unit/'
    connection = urllib2.urlopen(url + unitCode + '/geography?detail=envelope&dataformat=wkt&format=json')
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

def formatStringArguments(providedArgs, validArgs = None):
    '''
    Formats arguments to handle None, lists and strings.
    Defaults to the valid arguments if the provided arguments are None
    IF [] is passed, the defaults are not assigned
    '''
    #if no provided arguements, then default to valid arguments
    if not providedArgs and providedArgs != []:
        providedArgs = validArgs

    #if provided arguments are iterable, then do nothing
    elif hasattr(providedArgs, '__iter__'):
        pass

    #otherwise, assume that provided arguments are a string(-like) and can be
    # split using a comma as the delimiter
    else:
        providedArgs = str(providedArgs)
        providedArgs = providedArgs.replace(' ','')
        providedArgs = providedArgs.split(',')
    return providedArgs


if __name__=='__main__':
    print (missingValue)
    print (getBoundingBox('ACAD',0))
    print (getBoundingBox('FF04RMHC00'))
