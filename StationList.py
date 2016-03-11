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
import IM_Climate

class StationList(IM_Climate):
    def __init__(self):
        self.source = 'StnMeta'

    def getStationList(self, state = None, wxElement = None, county = None, bbox = None):
        return self._call_ACIS(state = state, elems = wxElement
            , county = county, bbox = bbox)


if __name__ == '__main__':
    c = StationList()
    data =  c.getStationList(state = 'CO', wxElement = 'snwd', county = '08117')
    print len(data['meta'])