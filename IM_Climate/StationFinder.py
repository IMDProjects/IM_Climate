try:
    #python 2.x
    from StationInfo import StationInfo
    from ACIS import ACIS
except:
    #python 3.x
    from .ACIS import ACIS
    from .StationInfo import StationInfo

class StationFinder(ACIS):
    def __init__(self, *args, **kwargs):
        super(StationFinder,self).__init__(*args, **kwargs)
        self.webServiceSource = 'StnMeta'

    def find(self, state = None, wxElement = None, countyCode = None,
        bbox = None, HUC = None, **kwargs):
        '''Returns a list object of stations based on the the specified criteria:
                state - Two-letter state acronym (e.g., CO)
                wxElement - Weather element code (e.g., tmin)
                countyCode - County fips code (e.g., 08117)
                bbox - A latitude/longitude bounding box defined
                    in decimal degrees (West, South, East, North) with negative
                    values indicating west longitude and south latitude
                    (e.g. -90.7, 40.5, -88.9, 41.5).
        '''

        results =  self._call_ACIS(state = state, elems = wxElement
            ,county = str(countyCode), bbox = bbox, basin = str(HUC), **kwargs)

        return StationInfo(results, queryParams = self.input_dict)


if __name__ == '__main__':
    c = StationFinder()
    print(c.wxElements)
    stationInfo =  c.find(wxElement = 'avgt', countyCode = '08117')
    #stationInfo =  c.find( countyCode = '08117')
    #stationInfo = c.find(HUC = 14010001)
    print(stationInfo.stationIDs)
    #print(stationInfo.metadata)