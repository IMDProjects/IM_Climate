import json

try:    #python 2.x
    import urllib2, urllib
    pyVersion = 2
except: #python 3.x
    import urllib.request
    import urllib.parse
    pyVersion = 3

supportedParameters = {'maxt':	{'info':'Maximum temperature (?F)', 'label':'maxt_F'}
                        ,'mint':{'info':'Minimum temperature (?F)', 'label':'mint_F'}
                        ,'avgt':{'info':'Average temperature (?F)', 'label':'avgt_F'}
                        ,'obst':{'info':'Obs time temperature (?F)', 'label':'obst_F'}
                        ,'pcpn':{'info': 'Precipitation (inches)', 'label':'pcpn_In'}
                        ,'snow' :{'info': 'Snowfall (inches)', 'label':'snow_In'}
                        ,'snwd': {'info':'Snow depth (inches)', 'label':'snwd_In'}
                        ,'cddXX': {'info':'Cooling Degree Days; where XX is base temperature', 'label':'cddXX'}
                        ,'hddXX': {'info':'Heating Degree Days; where XX is base temperature', 'label':'hddXX'}
                        ,'gddXX': {'info':'Growing Degree Days; where XX is base temperature', 'label':'gddXX'}
                        }

missingValue = 'NA'

class ACIS(object):

    '''
    Base class for all objects interacting with ACIS web services
    '''
    def __init__(self, *args, **kwargs):
        super(ACIS,self).__init__(*args, **kwargs)
        self.baseURL = 'http://data.rcc-acis.org/'
        self._input_dict = {}
        self.webServiceSource = None   #The web service source (e.g., 'StnData')

    def _call_ACIS(self, **kwargs):
        '''
        Core method for calling the ACIS services.

        Returns python dictionary by de-serializing json response
        '''
        self._formatInputDict(**kwargs)
        self.url = self.baseURL + self.webServiceSource
        if pyVersion == 2:      #python 2.x
            params = urllib.urlencode({'params':json.dumps(self._input_dict)})
            request = urllib2.Request(self.url, params, {'Accept':'application/json'})
            response = urllib2.urlopen(request)
            jsonData = response.read()
        elif pyVersion == 3:    #python 3.x
            params = urllib.parse.urlencode({'params':json.dumps(self._input_dict)})
            params = params.encode('utf-8')
            req = urllib.request.urlopen(self.url, data = params)
            jsonData = req.read().decode()
        return json.loads(jsonData)

    def _formatInputDict(self,**kwargs):
        '''
        Method to pack all arguments into input_dict which used to call the ACIS web
            service. Filters out all argument of None.
        '''
        for k in kwargs:
            if kwargs[k] and kwargs[k] <> 'None':
                self._input_dict[k] = kwargs[k]

if __name__ == '__main__':
    c = ACIS()

    print (supportedParameters)

    c.input_dict = {
        'uid': 3940,
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
    c.webServiceSource = 'StnData'
