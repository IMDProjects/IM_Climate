from ACIS import ACIS
from common import formatStringArguments
from GridStack import GridStack

class GridRequestor(ACIS):
    gridSource = 'PRISM' #ONLY PRISM IS SUPPORTED AT PRESENT
    precision = 1 #precision is only set for gridded data at present
    add = None
    reduceCodes = []

    def __init__(self):
        super(GridRequestor,self).__init__()
        self.defaultParameters = self.supportedParameters
        self.duration = None
        self.webServiceSource = 'GridData'

    @property
    def supportedParameters(self):
        '''
        Supported parameters for grids - this will need to be updated as we
        introduce more grid sources
        '''
        #NOTE: These parameters are specific to PRISM
        return ['pcpn', 'mint', 'maxt', 'avgt']

    def _callForGrids(self, **kwargs):
        '''
        Core method to request grids from ACIS
        '''
        #add the metadata and  precision level to the set of arguments
        kwargs = self._formatArguments(kwargs, meta = 'll', precision = self.precision)

        #Based on the grid source, get additional metadata values specific to grids
        gridSourceCode = self.gridSources[self.gridSource]['code']
        missingValue = int(self.gridSources[self.gridSource]['missingValue'])
        cellSize = float(self.gridSources[self.gridSource]['cellSize'])
        projection = self.gridSources[self.gridSource]['projection']

        #call ACIS for grids and extract out the latitude and longitude values
        #from the response
        grids = self._call_ACIS(kwargs, grid = gridSourceCode)
        self._checkResponseForErrors(grids)
        latValues = grids['meta']['lat']
        lonValues = grids['meta']['lon']

        #Instantiate grid stack object
        gs = GridStack(gridSource = self.gridSource, latValues = latValues, lonValues = lonValues, cellSize = cellSize,
                projection = projection, aggregation = self.interval, missingValue = missingValue)

        #iterate through all of the grids and add them to the stack
        for grid in grids['data']:
            for index, variable in enumerate(self.climateParameters):
                gs._addGrid(variable = variable, date = grid[0].encode(), grid = grid[index+1])

        #If file Path and name are provided, export all grids
        if self.filePath:
            gs.export(filePath = self.filePath)
        return gs

    def getGrids(self, sdate, edate, duration, unitCode = None, distance = 0,
        climateParameters = None, filePath = None):
        '''
        Method to fetch daily grids from ACIS.  Currently only PRISM grids are
        supported.

        ARGUMENTS
            sdate               Start date (yyyy-mm-dd or yyyymmdd).
            edate               End date (yyyy-mm-dd or yyyymmdd).
            duration            dly | mly | yly (i.e, daily, monthly, or yearly)
            unitCode (optional) 4-letter unit code. Currently accepts only one.
            distance (optional) Distance in kilometers for buffering a bounding box of park.
                                If no distance is specified then 0 is used as the default buffer.
            climateParameters (optional)    Accepts one or more of the climate parameter codes,
                                            preferably as a list or tuple
            filePath (optional)             If provided, one or more ascii grids are saved to the
                                    working directory. Grid names follow the pattern of
                                    Source_parameter_aggregation_YYYYMMDD (e.g., PRISM_mint_dly_20150101)

        RETURNS
            Dictionary like object (aka GridStack) containing one or more daily grids.
            Grids are indexed first by parameter and then by date
        '''
        self.interval = duration
        self.duration = duration


        if self.duration != 'dly':
            climateParameters = formatStringArguments(climateParameters, self.supportedParameters)
            climateParameters = map(lambda p: self.duration + '_' + p, climateParameters)

        return self._callForGrids(unitCode = unitCode, sdate = sdate, edate = edate
            , distance = distance, filePath = filePath, climateParameters = climateParameters,
            reduceCodes = self.reduceCodes, prec = self.precision )


if __name__ == '__main__':
    gr = GridRequestor()
    filePath = 'C:\\TEMP\\'

    ##YEARLY GRIDS

    #TEST 01
    sdate = '1915'
    edate = '1929'
    climateParameters = ['mint', 'maxt']
    unitCode = 'LIBO'
    distance = 10

    data =  gr.getGrids(sdate = sdate, edate = edate, duration = 'yly'
        ,unitCode = unitCode, distance = distance,
        climateParameters = climateParameters, filePath = filePath )
    print data.climateParameters
    print data.dates

    ##MONTHLY GRIDS

    #TEST 01
    sdate = '1895-01'
    edate = '1896-12'
    climateParameters = ['mint', 'maxt']
    unitCode = 'YELL'
    distance = 0

    data =  gr.getGrids(sdate = sdate, edate = edate, duration = 'mly'
        ,unitCode = unitCode, distance = distance,
        climateParameters = climateParameters, filePath = filePath )
    print data.climateParameters
    print data.dates
    data.export(filePath = filePath)
    print data['mly_mint']['1895-01']
    print data.dates
    print data.climateParameters
    data['mly_mint']['1895-01'].export(filePathAndName = filePath + 'test.asc')
##
    #Test 02
    unitCode = 'OLYM'
    sdate = '20150115'
    edate = '20150615'
    climateParameters = ['maxt']
    distance = 0
    data =  gr.getGrids(sdate = sdate, edate = edate, duration = 'mly'
        ,unitCode = unitCode, distance = distance,
        climateParameters = climateParameters, filePath = filePath )


    ##DAILY GRIDS
##    #TEST 01
##    sdate = '2015-01-01'
##    edate = '2015-01-04'
##    climateParameters = 'mint, maxt'
##    unitCode = 'APPA'
##    distance = 0
##
##    data =  gr.getGrids(sdate = sdate, edate = edate, duration = 'dly',
##        unitCode = unitCode, distance = distance,
##        climateParameters = climateParameters, filePath = filePath )
##    print data.climateParameters
##    print data.dates
##    data.export(filePath = filePath)
##    print data['mint']['2015-01-03']
##    print data.dates
##    print data.climateParameters
##    data['mint']['2015-01-03'].export(filePathAndName = filePath + 'test.asc')
##
##    #Test 02
##    unitCode = 'OLYM'
##    sdate = '20150615'
##    edate = '20150615'
##    climateParameters = ['maxt']
##    distance = 0
##    data =  gr.getGrids(sdate = sdate, edate = edate, duration = 'dly',
##        unitCode = unitCode, distance = distance,
##    climateParameters = climateParameters, filePath = filePath )



