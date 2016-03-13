import urllib2, urllib
import json

from Station import Station
from IM_Climate import IM_Climate

class StationFinder(IM_Climate):
    def __init__(self):
        super(StationList,self).__init__()
        self.webServiceSource = 'StnMeta'
        self.stationList = {}

    def find(self, state = None, wxElement = None, countyCode = None, bbox = None):
        '''Returns a list of stations based on the the specified criteria:
                state - Two-letter state acronym (e.g., CO)
                wxElement - Weather element code (e.g., tmin)
                countyCode - County fips code (e.g., 08117)
                bbox - Bounding box (e.g.,
        '''

        results =  self._call_ACIS(state = state, elems = wxElement
            , county = countyCode, bbox = bbox)
        self.stationList= results['meta']
        return self.stationList


if __name__ == '__main__':
    c = StationFinder()
    stations =  c.find(state = 'CO', wxElement = 'gdd', countyCode = '08117')
    print stations