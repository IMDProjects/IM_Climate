from ACIS import ACIS
import common
import GridStack
reload (GridStack)
from GridStack import GridStack

class GridRequestor(ACIS):
    def __init__(self):
        super(GridRequestor,self).__init__()
        self.webServiceSource = 'GridData'

    def _callForGrids(self):
        self.climateParameters = self._formatClimateParameters(self.climateParameters)
        if self.unitCode:
            bbox = common.getBoundingBox(self.unitCode, distance)
        elems = self._formatElems()
        gridSourceCode = self.gridSources[self.gridSource]['code']
        missingValue = int(self.gridSources[self.gridSource]['missingValue'])
        cellSize = float(self.gridSources[self.gridSource]['cellSize'])
        projection = self.gridSources[self.gridSource]['projection']

        grids =  self._call_ACIS(elems = elems
            ,bbox = bbox, sDate = sDate, eDate = eDate, grid = gridSourceCode, meta='ll')
        latValues = grids['meta']['lat']
        lonValues = grids['meta']['lon']
        gs = GridStack(gridSource = gridSource, latValues = latValues, lonValues = lonValues, cellSize = cellSize,
                projection = projection, missingValue = missingValue)
        for grid in grids['data']:
            for index, variable in enumerate(self.climateParameters):
                gs._addGrid(variable = variable, date = grid[0].encode(), grid = grid[index+1])
        return gs

    def _formatElems(self):
            elems = []
            for p in self.climateParameters:
                elems.append({'name':p,'interval':self.interval, 'duration' : self.duration})
            return elems

    def getDailyGrids(self, sdate, edate, unitCode = None, distance = 0, climateParameters = None):
        '''
        Method to fetch daily grids from ACIS.  Currently only PRISM grids are
        supported.
        '''
        self.gridSource = gridSource
        self.unitCode = unitCode
        self.climateParameters = climateParameters
        self.interval = 'dly'
        self.duration = 'dly'
        self.gridSource = 'PRISM'
        return self._callForGrids()

if __name__ == '__main__':
    agr = GridRequestor()
    gridSource = 'PRISM'
    sDate = '2015-01-01'
    eDate = '2015-01-01'
    climateParameters = 'mint'
    parkCode = 'GRKO'
    distance = 0
    data =  agr.getDailyGrids(sdate = sDate, edate = eDate,
        unitCode = parkCode, distance = distance, climateParameters = climateParameters )
    print data.variables
    print data.dates
    data.export('C:\\TEMP\\')


