import json
import copy
from common import getBoundingBox, formatStringArguments

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
    defaultParameters = ('pcpn', 'mint', 'maxt', 'avgt', 'obst', 'snow', 'snwd')
    baseURL = 'http://data.rcc-acis.org/'
    _input_dict = {}
    webServiceSource = None   #The web service source (e.g., 'StnData')

    def __init__(self):
        self._getACISLookups()

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

    def _call_ACIS(self, kwargs, **moreKwargs):
        '''
        Core method for calling the ACIS services.

        Returns python dictionary by de-serializing json response
        '''
        #self._formatInputDict(**kwargs)
        kwargs.update(moreKwargs)
        self._input_dict = self._stripNoneValues(kwargs)
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

    def _stripNoneValues(self, d = {}, **kwargs):
        '''
        Strips out all argument of None from a dictionary and/or a set
        of keyword arguments
        '''
        data = {}
        kwargs.update(d)
        for k in kwargs:
            if kwargs[k] is not None and kwargs[k] != 'None':
                data[k] = kwargs[k]
        return data

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

    def _formatClimateParameters(self, climateParameters = None):
        '''
        Formats the climate parameters.
        If None, then default to all supported climate parameters
        '''
        if not hasattr(self, 'climateParameters'):
            self.climateParameters = climateParameters
        self.climateParameters =  formatStringArguments(climateParameters
            , self.defaultParameters)

    def _formatReduceCodes(self, reduceCodes):
        '''
        Formats reduce codes consistently.
        If None, then default to all supported reduce codes
        If [], reduce codes are set to None
        '''
        return formatStringArguments(reduceCodes, ('min', 'max', 'sum', 'mean'))


    def _formatDate(self, date):
        '''
        If date is None, then sets value to por
        If date is NA, then returns None
        '''
        if date == 'NA':
            date = None
            return date
        if date is None:
            date = 'por'
        return str(date)

    def _checkResponseForErrors(self, response):
        '''
        Raises an exception if the ACIS response is an Error
        '''
        if response.get('error', None) and response.get('error', None) != 'no data available':
            raise Exception('ACIS Service Error: ' + str(response['error']))

    def _formatElems(self):
        '''
        Formats consistently the ELEMs objects used in the ACIS web service calls
        '''

        #build the elems objects, which ACIS requires for more complex queries
        self.elems = []
        for p in self.climateParameters:
            arguments = {'name': p, 'interval': self.interval, 'add': self.add
             ,'duration': self.duration,'maxmissing': self.maxMissing, 'prec': self.precision}
            self.elems.append(arguments)

        #Update the elems object to add all variations of parameters and reduce
        # codes, where applicable
        # Too bad ACIS just doesn't just ignore reduce codes where not applicable
        if self.reduceCodes:
            rcelems = []
            for k in self.elems:
                for rd in self.reduceCodes:
                    k['reduce'] = {'reduce': rd, 'add':self.add}
                    rcelems.append(k.copy())
            self.elems = rcelems[:]

        #Add all variations of climate parameters and reduce codes to a list
        #This list is used to help instantaite the station dictionary object
        self.updatedClimateParameters = None #re-initialize these each time
        if self.reduceCodes:
            self.updatedClimateParameters = [k['name'] + '_' + k['reduce']['reduce'] for k in self.elems]
        else:
            self.updatedClimateParameters = self.climateParameters[:]

        #update climate parameters to include normals
        np = []
        if self.includeNormals or self.includeNormalDepartures:
            for cp in self.updatedClimateParameters:
                np.append(cp)
                if self.includeNormals:
                    z = cp[:]
                    np.append(z + '_normal')
                if self.includeNormalDepartures:
                    z = cp[:]
                    np.append(z + '_normalDeparture')
            self.updatedClimateParameters = np[:]

        #Add additional request of normals to elems dictionary
        if self.includeNormals or self.includeNormalDepartures:
            rcelems = []
            for k in self.elems:
                rcelems.append(k)
                if self.includeNormals:
                    n = copy.deepcopy(k)
                    n['normal']=1
                    n.pop('add', None)  #remove the add argument, if present
                    rcelems.append(n)
                if self.includeNormalDepartures:
                    n = copy.deepcopy(k)
                    n['normal'] = "departure"
                    n.pop('add', None)  #remove the add argument, if present
                    rcelems.append(n)
            self.elems = rcelems[:]

        #strip out all None values
        for e,value in enumerate(self.elems):
            self.elems[e] = self._stripNoneValues(value)

    def _formatArguments(self, k_dict = {}, **kwargs):
        '''
        Provides a standard way of formatting the ACIS web service arguments
        '''

        kwargs.update(k_dict)
        self.climateParameters = None
        #clean up some of the kwargs used in the ACIS call
        kwargs['sdate'] = self._formatDate(kwargs.get('sdate', None))
        kwargs['edate'] = self._formatDate(kwargs.get('edate', None))

        #pop the kwargs that are not used directly in the ACIS call
        self.reduceCodes = self._formatReduceCodes(kwargs.pop('reduceCodes', None))
        self.filePathAndName =  kwargs.pop('filePathAndName', None)
        self.stationIDs = self._extractStationIDs(kwargs.pop(('climateStations'), None))
        self._formatClimateParameters(kwargs.pop('climateParameters'))
        self.includeNormals = kwargs.pop('includeNormals', None)
        self.includeNormalDepartures = kwargs.pop('includeNormalDepartures', None)
        self.maxMissing = (kwargs.pop('maxmissing', None))
        self.filePath= (kwargs.pop('filePath', None))
        self.precision = (kwargs.pop('precision', None))
        unitCode = (kwargs.pop('unitCode', None))
        distance = (kwargs.pop('distance', None))

        kwargs['bbox'] = getBoundingBox(unitCode, distance)

        #do the complicated formatting of the elems list
        self._formatElems()
        kwargs['elems'] = self.elems
        return kwargs


    def _extractStationIDs(self, stations):
        '''
        INFO
        ----
        If stations is a StationDict object, extracts list of stationIDs.
        Otherwise, assumes stationIDs to be a list, comma-delimited string,
        or a single stationID as a string.
        '''
        if stations is not None:
            try:
                return stations.stationIDs
            except:
                return formatStringArguments(stations)

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
