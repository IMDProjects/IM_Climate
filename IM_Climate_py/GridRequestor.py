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
                elems.append({'name':p,'interval':self.interval, 'duration' : self.duration, 'prec': 1})
            return elems

    def getDailyGrids(self, sdate, edate, unitCode = None, distance = 0,
        climateParameters = None, filePath = None):
        '''
        Method to fetch daily grids from ACIS.  Currently only PRISM grids are
        supported.

        ARGUMENTS
            sdate - Start date (yyyy-mm-dd or yyyymmdd).
            edate -     End date (yyyy-mm-dd or yyyymmdd).
            unitCode  (optional) ? 4-letter unit code. Currently accepts only one.
            distance (optional) ? Distance in kilometers for buffering a bounding box of park. If no distance is specified then 0 is used as the default buffer.
            climateParameters (optional)  ? accepts one or more of the weather parameter codes in Table 2.
            filePath (optional)?  If provided, one or more ascii grids are saved to the working directory. Grid names follow the pattern of Source_parameter_aggregation_YYYYMMDD (e.g., PRISM_mint_dly_20150101)

        RETURNS
            Dictionary like object (aka GridStack) containing one or more grids.
            Grids are indexed first parameter and then by date
            GridStack
                Parameter
                    Date
                        Grid

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
    eDate = '2015-01-04'
    climateParameters = 'mint'
    unitCode = 'YELL'
    distance = 0
    filePath = 'C:\\TEMP\\'
    data =  gr.getDailyGrids(sdate = sDate, edate = eDate,
        unitCode = unitCode, distance = distance,
        climateParameters = climateParameters, filePath = filePath )
    print data.climateParameters
    print data.dates
    data.export()
    print data['mint']['2015-01-03']
    print data.dates
    print data.climateParameters
    data['mint']['2015-01-03'].export('C:\\TEMP\\test.asc')


