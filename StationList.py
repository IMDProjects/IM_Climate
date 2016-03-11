import urllib2, urllib
import json

from Station import Station
from IM_Climate import IM_Climate

class StationList(IM_Climate):
    def __init__(self):
        super(StationList,self).__init__()
        self.webServiceSource = 'StnMeta'
        self.stationList = {}

    def getStationList(self, state = None, wxElement = None, county = None, bbox = None):
        results =  self._call_ACIS(state = state, elems = wxElement
            , county = county, bbox = bbox)
        self.stationList= results['meta']
        return self.stationList


if __name__ == '__main__':
    c = StationList()
    stations =  c.getStationList(state = 'CO', wxElement = 'snwd', county = '08117')
    print len(stations)