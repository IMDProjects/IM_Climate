from ACIS import ACIS
import common

class ACIS_GridRequestor(ACIS):
    def __init__(self):
        super(ACIS_GridRequestor,self).__init__()
        self.webServiceSource = 'GridData'

    def getDailyGrids(self, gridSource, sDate, eDate,
            parkCodes = None, distance = 0,  climateParameters = None):

        if not climateParameters:
            climateParameters = ['pcpn', 'snwd', 'avgt', 'obst', 'mint', 'snow', 'maxt']
        else:
            climateParameters = climateParameters.replace(' ','')

        if parkCodes:
            bbox = common.getBoundingBox(parkCodes, distance)

        grids =  self._call_ACIS(elems = [{'name':'maxt','interval':'dly','duration':'dly'}]
            ,bbox = bbox, sDate = '2012-1-01', eDate = '2012-01-05', grid = 21)
        print grids

    def getMonthlyGrids(self, gridSource, sDate, eDate,
            parkCodes = None, distance = 0,  climateParameters = None):

        if not climateParameters:
            climateParameters = ['pcpn', 'snwd', 'avgt', 'obst', 'mint', 'snow', 'maxt']
        else:
            climateParameters = climateParameters.replace(' ','')

        if parkCodes:
            bbox = common.getBoundingBox(parkCodes, distance)

        grids =  self._call_ACIS(elems = [{'name':'maxt','interval':'mly','duration':'mly'}]
            ,bbox = bbox, sDate = '2012-1-01', eDate = '2012-02-01', grid = 21)
        print grids

    def getYearlyGrids(self, gridSource, sDate, eDate,
            parkCodes = None, distance = 0,  climateParameters = None):

        if not climateParameters:
            climateParameters = ['pcpn', 'snwd', 'avgt', 'obst', 'mint', 'snow', 'maxt']
        else:
            climateParameters = climateParameters.replace(' ','')

        if parkCodes:
            bbox = common.getBoundingBox(parkCodes, distance)

        grids =  self._call_ACIS(elems = [{'name':'maxt','interval':'yly','duration':'yly'}]
            ,bbox = bbox, sDate = '2012', eDate = '2012', grid = 21)
        print grids

if __name__ == '__main__':
    agr = ACIS_GridRequestor()
    gridSource = 21
    sDate = '2015-01-01'
    eDate = '2015-02-01'
    climateParameters = 'mint'
    parkCode = 'AGFO'
    distance = 0
    print agr.getDailyGrids(gridSource = gridSource, sDate = sDate, eDate = eDate,
        parkCodes = parkCode, distance = distance, climateParameters = climateParameters )
    print agr.getMonthlyGrids(gridSource = gridSource, sDate = sDate, eDate = eDate,
        parkCodes = parkCode, distance = distance, climateParameters = climateParameters )
    print agr.getYearlyGrids(gridSource = gridSource, sDate = sDate, eDate = eDate,
        parkCodes = parkCode, distance = distance, climateParameters = climateParameters )


