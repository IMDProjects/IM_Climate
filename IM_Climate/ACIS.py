try:
    #python 2.x
    import urllib2, urllib
    pyVersion = 2
except:
    #python 3.x
    import urllib.request
    import urllib.parse
    pyVersion = 3
import json
from datetime import date


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
        if pyVersion == 2:      #python 2.x
            params = urllib.urlencode({'params':json.dumps(self.input_dict)})
            request = urllib2.Request(self.url, params, {'Accept':'application/json'})
            response = urllib2.urlopen(request)
            jsonData = response.read()
        elif pyVersion == 3:    #python 3.x
            params = urllib.parse.urlencode({'params':json.dumps(self.input_dict)})
            params = params.encode('utf-8')
            req = urllib.request.urlopen(self.url, data = params)
            jsonData = req.read().decode() #decode() added for python 3.x
        return json.loads(str(jsonData))

    def _formatInputDict(self,**kwargs):
        '''
        Method to pack all arguments into a dictionary using to call the web
            service.

        This method is need primarily for the purpose of filtering our any
            argument that is None.
        '''
        for k in kwargs:
            if kwargs[k] and kwargs[k] <> 'None':
                self.input_dict[k] = kwargs[k]

    def countyCodes(self, state = None):
        fipCode = []
        try:
            #python 2.x
            data = urllib2.urlopen('http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt')
        except:
            #python 3.x
            data = urllib.request.urlopen('http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt')
        for line in data.readlines():
            line = str(line).split(',')
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
    print (c.countyCodes(state =  'CO'))
    print (c._getCurrentYear())
    print (c.countyCodes('CO'))
    print (c.wxElements)

    c.input_dict = {
        'bbox': "-102,48,-98,50",
        'sdate': "2008-01",
        'edate': "2010-12",
        'elems': [{
            'name': "pcpn",
            'interval': "yly",
            'duration': "yly",
            'reduce': {
                'reduce': "sum",
                'add': "mcnt"
            },
            'maxmissing': '7',
            'smry': ["max", "min", "mean"]
        }],
        'meta': "name,state,ll"
    }
    c.webServiceSource = 'MultiStnData '
    c._call_ACIS()