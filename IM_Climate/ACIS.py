import urllib2, urllib
import json
from datetime import date

##import urllib.request
##import urllib.parse
##
##input_dict = {"county":"22033"}
##params = urllib.parse.urlencode({'params':json.dumps(input_dict)})
##params = params.encode('utf-8')
##req = urllib.request.urlopen('http://data.rcc-acis.org/StnMeta', data = params)
##z = req.read()
##print (z)


class ACIS(object):

    '''
    Base class for all objects interacting with ACIS web services
    '''
    def __init__(self, *args, **kwargs):
        super(ACIS,self).__init__(*args, **kwargs)
        self.baseURL = 'http://data.rcc-acis.org/'
        self.input_dict = {}
        self.webServiceSource = None   #The web service source (e.g., 'StnData')


        self.wxElements = {'maxt':	'Maximum temperature (?F)'
                            ,'mint':'Minimum temperature (?F)'
                            ,'avgt':'Average temperature (?F)'
                            ,'obst':'Obs time temperature (?F)'
                            ,'pcpn': 'Precipitation (inches)'
                            ,'snow' : 'Snowfall (inches)'
                            ,'snwd': 'Snow depth (inches)'
                            ,'cddXX': 'Cooling Degree Days; where XX is base temperature'
                            ,'hddXX': 'Heating Degree Days; where XX is base temperature'
                            ,'gddXX': 'Growing Degree Days; where XX is base temperature'
                            }

        self.reduceCodes = {'max': 'Maximum value for the period'
                , 'min':'Minimum value for the period'
                , 'sum' : 'Sum of the values for the period'
                , 'mean': 'Average of the values for the period'}

    def _call_ACIS(self, **kwargs):
        '''
        Common method for calling the ACIS services.

        Returns python dictionary bu de-serializing json response
        '''
        self._formatInputDict(**kwargs)
        self.url = self.baseURL + self.webServiceSource
        params = urllib.urlencode({'params':json.dumps(self.input_dict)})
        request = urllib2.Request(self.url, params, {'Accept':'application/json'})
        response = urllib2.urlopen(request)
        jsonData = response.read()
        return json.loads(jsonData)

    def _formatInputDict(self,**kwargs):
        '''
        Method to pack all arguments into a dictionary using to call the web
            service.

        This method is need primarily for the purpose of filtering our any
            argument that is None.
        '''
        for k in kwargs:
            if kwargs[k]:
                self.input_dict[k] = kwargs[k]

    def countyCodes(self, state = None):
        fipCode = []
        data = urllib2.urlopen('http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt')
        for line in data.readlines():
            line = line.split(',')
            if state:
                if line[0] == state:
                    fipCode.append(line[3] + ', ' + line[0] + ' : ' + line[1] + line[2])
            else:
                fipCode.append(line[0] + ',' + line[3] + ' : ' + line[1] + line[2])
        return fipCode


    def _getCurrentYear(self):
        return date.today().year


if __name__ == '__main__':
    c = ACIS()
    print c.countyCodes(state =  'CO')
    print c._getCurrentYear()
    print c.countyCodes('CO')
    print c.wxElements