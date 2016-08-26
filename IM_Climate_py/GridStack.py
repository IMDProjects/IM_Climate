
class GridStack(dict):
    '''
    Assume that the following are constant:
        grid resolution
        extent
        missing value
    Organization:
        Source
            Date
                Variable

    '''
    def __init__(self, numberOfColumns, numberOfRows, latValues, lonValues, missingValue):
        self.missingValue = missingValue       #The specified missing value - Must be the same for all grids
        self.numberOfColumns = numberOfColumns        #The x dimension of the grid
        self.numberOfRows = numberOfRows        #The y dimension of the grid
        self.latValues = latValues         #The latitude values
        self.lonValues = lonValues          #The longitude values

    def _addGrid(self, source, variable, date, GridClass):
        pass

if __name__ == '__main__':
    gs = GridStack()
