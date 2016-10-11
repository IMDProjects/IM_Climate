import json

try:    #python 2.x
    import urllib2, urllib
    pyVersion = 2
except: #python 3.x
    try:
        import urllib.request
        import urllib.parse
        pyVersion = 3
    except:
        raise Exception('Libary Import Failure')


class ACIS(object):

    '''
    Base class for all objects interacting with ACIS web services
    '''
    def __init__(self, *args, **kwargs):
        super(ACIS,self).__init__(*args, **kwargs)
        self.baseURL = 'http://data.rcc-acis.org/'
        self._input_dict = {}
        self.webServiceSource = None   #The web service source (e.g., 'StnData')
        self._getACISLookups()
        self.precision = 1

    def _getACISLookups(self):
        '''
        Reads the common lookup tables shared by python and R libraries
        '''
        try:
            lfile = open('./ACISLookups.json', 'r')
        except:
            lfile = open('../ACISLookups.json', 'r')
        info = lfile.read()
        self._acis_lookups = json.loads(info)

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
        self._input_dict = {}    #Clears the input dictionary
        for k in kwargs:
            if kwargs[k] and kwargs[k] != 'None':
                self._input_dict[k] = kwargs[k]

    @property
    def supportedParameters(self):
        return {elem['code'].encode(): {'description': elem['description'].encode(),
                                        'unit': elem['unit'].encode(),
                                        'unitabbr': elem['unitabbr'].encode(),
                                        'label': elem['code'].encode() + '_' + elem['unitabbr'].encode(),
                                        } for elem in self._acis_lookups['element'] }
    @property
    def stationSources(self):
        return {elem['code'].encode(): {'description': elem['description'].encode(),
                                        'subtypes': elem['subtypes'],
                                        } for elem in self._acis_lookups['stationIdType'] }

    @property
    def gridSources(self):
        return self._acis_lookups['gridSources']

    def _formatClimateParameters(self, climateParameters):
        '''
        Formats the climate parameters.
        If None, then default to all supported climate parameters
        '''
        return self._formatStringArguments(climateParameters
            , ['pcpn', 'snwd', 'avgt', 'obst', 'mint', 'snow', 'maxt'])

    def _formatReduceCodes(self, reduceCodes):
        '''
        Formats reduce codes consistently.
        If None, then default to all supported reduce codes
        '''
        return self._formatStringArguments(reduceCodes
            , ['max', 'min', 'sum','mean'])
            #,'stddev' - omitting right now because ACIS does not return any data

    def _formatStringArguments(self, providedArgs, validArgs = None):
        '''
        Formats arguments to handle None, lists and strings.
        Defaults to the valid arguments if the provided arguments are None
        '''
        #if no provided arguements, then default to valid arguments
        if not providedArgs:
            providedArgs = validArgs
        #if provided arguments are a list, then do nothing
        elif type(providedArgs) == list:
            pass

        #otherwise, assume that provided arguments are a string(-like) and can be
        # split using a comma as the delimiter
        else:
            providedArgs = str(providedArgs)
            providedArgs = providedArgs.replace(' ','')
            providedArgs = providedArgs.split(',')
        return providedArgs


if __name__ == '__main__':
    c = ACIS()


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
    print (c._acis_lookups.keys())
    print (c.supportedParameters)
    print (c.stationSources)
    print (c.gridSources.keys())
