#-------------------------------------------------------------------------------
# Name:       IM_Climate
# Purpose: Simple API to interface with ACIS Sytsem
#
# Author:      Iventory and Montoring Division,  National Park Service
#               Lisa Nelson, Brent Frakes

#-------------------------------------------------------------------------------
import urllib2, urllib
import json

from Station import Station

class NPS_Climate(object):
    def __init__(self):
        self.baseURL = 'http://data.rcc-acis.org/'
        self.input_dict = {}

    def getStationList(self, state = None, wxElement = None, county = None, bbox = None):
        self.source = 'StnMeta'
        return self._call_ACIS(state = state, elems = wxElement
            , county = county, bbox = bbox)

    def _call_ACIS(self, **kwargs):
        '''
        Common method for calling the ACIS services.

        Returns python dictionary bu de-serializing json response
        '''
        self._formatInputDict(**kwargs)
        self.url = self.baseURL + self.source
        params = urllib.urlencode({'params':json.dumps(self.input_dict)})
        request = urllib2.Request(self.url, params, {'Accept':'application/json'})
        response = urllib2.urlopen(request)
        jsonData = response.read()
        return json.loads(jsonData)

    def _formatInputDict(self,**kwargs):
        for k in kwargs:
            if kwargs[k]:
                self.input_dict[k] = kwargs[k]




if __name__ == '__main__':
    c = NPS_Climate()
    data =  c.getStationList(state = 'CO', wxElement = 'snwd', county = '08117')
    print len(data['meta'])