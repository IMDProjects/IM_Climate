import Grid
reload(Grid)
from Grid import Grid
import numpy as np
import sets

class GridStack(dict):
    '''
    Assume that the following are constant:
        grid source
        grid resolution
        extent
        missing value
    Organization:
        Date
            Variable

    '''
    def __init__(self, gridSource, latValues, lonValues, cellSize, projection,
                   aggregation, missingValue):
        self.gridSource = gridSource
        self.missingValue = missingValue       #The specified missing value - Must be the same for all grids
        self.latValues = np.array(latValues)         #The latitude values
        self.lonValues = np.array(lonValues)          #The longitude values
        self.XLLCenter = self.lonValues.min()
        self.YLLCenter = self.latValues.min()
        self.cellSize = cellSize
        self.projection = projection
        self.aggregation = aggregation

    @property
    def climateParameters(self):
        return self.keys()

    @property
    def dates(self):
        allDates = sets.Set([])
        for d in self.keys():
            allDates.update(self[d].keys())
        d =  list(allDates)
        d.sort()
        return d

    def _addGrid(self, variable, date, grid):
        '''
        Method to control the adding of grids to the stack
        '''
        try:
            self[variable]
        except:
            self[variable] = {}
        self[variable][date] = Grid(grid, XLLCenter = self.XLLCenter
            , YLLCenter = self.YLLCenter, cellSize = self.cellSize, projection = self.projection
            , missingValue = self.missingValue)

    def export(self, filePath = '', climateParameters = None, dates = None):
        '''
        Export that iterates through the set of grids within the stack and saves
        all individually as ascii grids (with projection file).

        RETURNS
        List of all exported files
        '''
        exportedFiles = []
        if not climateParameters:
            climateParameters = self.climateParameters
        if not dates:
            dates = self.dates
        for c in climateParameters:
            for d in dates:
                filePathAndName = (filePath + self.gridSource + '_' +  c + '_' +
                    self.aggregation + '_' + d + '.asc')
                self[c][d].export(filePathAndName = filePathAndName )
                exportedFiles.append(filePathAndName)
        return exportedFiles



if __name__ == '__main__':
    gridSource = 'PRISM'
    cellSize = 4
    missingValue= -999
    projection = 'NAD83'
    aggregation = 'dly'
    latValues = [[37.041666, 37.041666, 37.041666],
         [37.083333, 37.083333, 37.083333],
         [37.125, 37.125, 37.125]]
    lonValues = [[-93.458333, -93.416667, -93.375],
         [-93.458333, -93.416667, -93.375],
         [-93.458333, -93.416667, -93.375]]
    gs = GridStack(gridSource =gridSource, latValues = latValues,
        lonValues = lonValues, cellSize = cellSize, projection = projection,
        aggregation = aggregation, missingValue = missingValue)

    variable = 'mint'
    date = '2015-01-01'
    grid = [[15, 16, 16], [15, 15, 15], [15, 15, 15]]
    gs._addGrid(variable = variable, date = date, grid = grid)
    print gs.climateParameters
    print gs.dates
    print gs.export()