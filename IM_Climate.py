#-------------------------------------------------------------------------------
# Name:       IM_Climate
# Purpose: Simple API to interface with ACIS Sytsem
#
# Author:      Iventory and Montoring Division,  National Park Service
#               Lisa Nelson, Brent Frakes

#-------------------------------------------------------------------------------
import urllib2, urllib
import json

class IM_Climate(object):

    '''
    Base class with common methods
    '''
    def __init__(self):
        self.baseURL = 'http://data.rcc-acis.org/'
        self.input_dict = {}
        self.webServiceSource = None   #The web service source (e.g., 'StnData')


        self.wxElements = {'maxt':	'Maximum temperature (?F)'
                            ,'mint':'Minimum temperature (?F)'
                            ,'avgt':'Average temperature (?F)'
                            ,'obst':'Obs time temperature (?F)'
                            ,'pcpn': 'Precipitation (inches)'
                            ,'snow' : 'Snowfall (inches)'
                            ,'snwd': 'Snow depth (inches)'}

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
        '''
        for k in kwargs:
            if kwargs[k]:
                self.input_dict[k] = kwargs[k]




if __name__ == '__main__':
    c = IM_Climate()
