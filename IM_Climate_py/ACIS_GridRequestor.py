from ACIS import ACIS
import common

class ACIS_GridRequestor(ACIS):
    def __init__(self):
        super(ACIS_GridRequestor,self).__init__()
        self.webServiceSource = 'GridData'

    def getGrids(self, gridSource, sDate, eDate,
            parkCodes = None, distance = 0,  climateParameters = None):

        if not climateParameters:
            climateParameters = ['pcpn', 'snwd', 'avgt', 'obst', 'mint', 'snow', 'maxt']
        else:
            climateParameters = climateParameters.replace(' ','')

        if parkCodes:
            bbox = common.getBoundingBox(parkCodes, distance)

        grids =  self._call_ACIS(elems = climateParameters
            ,bbox = bbox, sDate = sDate, eDate = eDate)
        print grids

if __name__ == '__main__':
    agr = ACIS_GridRequestor()
    gridSource = 21
    sDate = '2015-01-01'
    eDate = '2015-02-01'
    climateParameters = 'mint'
    parkCode = 'ACAD'
    distance = 0
    print agr.getGrids(gridSource = gridSource, sDate = sDate, eDate = eDate,
        parkCodes = parkCode, distance = distance, climateParameters = climateParameters )



