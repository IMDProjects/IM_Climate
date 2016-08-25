from ACIS import ACIS
import common
from GridStack import GridStack

class GridRequestor(ACIS):
    def __init__(self):
        super(GridRequestor,self).__init__()
        self.webServiceSource = 'GridData'

    def getMonthlyGrids(self, gridSource, sDate, eDate,
            parkCodes = None, distance = 0,  climateParameters = None):

        self.gridSource = gridSource
        self.unitCode = unitCode
        self.climateParameters = climateParameters
        self.interval = 'mly'
        self.duration = 'mly'
        response = self._callForGrids()

    def getYearlyGrids(self, gridSource, sDate, eDate,
            parkCodes = None, distance = 0,  climateParameters = None):

        self.gridSource = gridSource
        self.unitCode = unitCode
        self.climateParameters = climateParameters
        self.interval = 'yly'
        self.duration = 'yly'
        response = self._callForGrids()
        print response

    def _callForGrids(self):
        self.climateParameters = self._formatClimateParameters(self.climateParameters)
        if self.unitCode:
            bbox = common.getBoundingBox(self.unitCode, distance)
        elems = self._formatElems()
        grid = self.gridSources[self.gridSource]['code']

        grids =  self._call_ACIS(elems = elems
            ,bbox = bbox, sDate = sDate, eDate = eDate, grid = 21)
        gs = GridStack()
        return grids

    def _formatElems(self):
            elems = []
            for p in self.climateParameters:
                elems.append({'name':p,'interval':self.interval, 'duration' : self.duration})
            return elems

    def getDailyGrids(self, gridSource, sDate, eDate,
            unitCode = None, distance = 0,  climateParameters = None):
        self.gridSource = gridSource
        self.unitCode = unitCode
        self.climateParameters = climateParameters
        self.interval = 'dly'
        self.duration = 'dly'
        response = self._callForGrids()
        print response


if __name__ == '__main__':
    agr = GridRequestor()
    gridSource = 'PRISM'
    sDate = '2015-01-01'
    eDate = '2015-01-03'
    climateParameters = 'mint, maxt'
    parkCode = 'AGFO'
    distance = 0
    print agr.getDailyGrids(gridSource = gridSource, sDate = sDate, eDate = eDate,
        unitCode = parkCode, distance = distance, climateParameters = climateParameters )
##    print agr.getMonthlyGrids(gridSource = gridSource, sDate = sDate, eDate = eDate,
##        parkCodes = parkCode, distance = distance, climateParameters = climateParameters )
##    print agr.getYearlyGrids(gridSource = gridSource, sDate = sDate, eDate = eDate,
##        parkCodes = parkCode, distance = distance, climateParameters = climateParameters )


