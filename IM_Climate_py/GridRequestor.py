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
        bbox = '-130, 20,-50,60'
        self.climateParameters = self._formatClimateParameters(self.climateParameters)
        if self.unitCode:
            bbox = common.getBoundingBox(self.unitCode, self.distance)
        elems = self._formatElems()
        gridSourceCode = self.gridSources[self.gridSource]['code']
        missingValue = int(self.gridSources[self.gridSource]['missingValue'])
        cellSize = float(self.gridSources[self.gridSource]['cellSize'])
        projection = self.gridSources[self.gridSource]['projection']

        grids =  self._call_ACIS(elems = elems
            ,bbox = bbox, sDate = self.sdate, eDate = self.edate, grid = gridSourceCode, meta='ll')
        latValues = grids['meta']['lat']
        lonValues = grids['meta']['lon']
        gs = GridStack(gridSource = self.gridSource, latValues = latValues, lonValues = lonValues, cellSize = cellSize,
                projection = projection, aggregation = self.interval, missingValue = missingValue)
        for grid in grids['data']:
            for index, variable in enumerate(self.climateParameters):
                gs._addGrid(variable = variable, date = grid[0].encode(), grid = grid[index+1])
        return gs

    def _formatElems(self):
            elems = []
            for p in self.climateParameters:
                elems.append({'name':p,'interval':self.interval, 'duration' : self.duration})
            return elems

    def getDailyGrids(self, sdate, edate, unitCode = None, distance = 0,
        climateParameters = None, filePath = None):
        '''
        Method to fetch daily grids from ACIS.  Currently only PRISM grids are
        supported.
        '''
        self.unitCode = unitCode
        self.sdate = sdate
        self.edate = edate
        self.climateParameters = climateParameters
        self.interval = 'dly'
        self.duration = 'dly'
        self.gridSource = 'PRISM'
        self.distance = distance
        grids = self._callForGrids()
        if filePath:
            grids.export(filePath = filePath)
        return grids

if __name__ == '__main__':
    gr = GridRequestor()
    sDate = '2015-01-01'
    eDate = '2015-01-02'
    climateParameters = 'mint'
    unitCode = 'WICR'
    distance = 0
    filePath = 'C:\\TEMP\\'
    data =  gr.getDailyGrids(sdate = sDate, edate = eDate,
        unitCode = unitCode, distance = distance,
        climateParameters = climateParameters, filePath = filePath )
    print data.variables
    print data.dates
    data.export()


