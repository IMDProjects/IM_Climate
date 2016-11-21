from ACIS import ACIS
import common
from GridStack import GridStack

class GridRequestor(ACIS):
    gridSource = 'PRISM' #ONLY PRISM IS SUPPORTED AT PRESENT
    precision = 1 #precision is only set for gridded data at present

    def __init__(self):
        super(GridRequestor,self).__init__()
        self.defaultParameters = self.supportedParameters()
        self.duration = None
        self.webServiceSource = 'GridData'


    def supportedParameters(self):
        '''
        Supported parameters for grids - this will need to be updated as we
        introduce more grid sources
        '''
        #NOTE: These parameters are specific to PRISM
        return ['pcpn', 'mint', 'maxt', 'avgt']

    def _callForGrids(self):
        '''
        Core method to request grids from ACIS
        '''
        bbox = '-130, 20,-50,60'
        self._formatClimateParameters()
        bbox = common.getBoundingBox(self.unitCode, self.distance)
        elems = self._formatElems()
        gridSourceCode = self.gridSources[self.gridSource]['code']
        missingValue = int(self.gridSources[self.gridSource]['missingValue'])
        cellSize = float(self.gridSources[self.gridSource]['cellSize'])
        projection = self.gridSources[self.gridSource]['projection']
        grids =  self._call_ACIS(elems = elems
            ,bbox = bbox, sDate = self.sdate, eDate = self.edate, grid = gridSourceCode, meta='ll')
        self._checkResponseForErrors(grids)
        latValues = grids['meta']['lat']
        lonValues = grids['meta']['lon']

        #Instantiate grid stack object
        gs = GridStack(gridSource = self.gridSource, latValues = latValues, lonValues = lonValues, cellSize = cellSize,
                projection = projection, aggregation = self.interval, missingValue = missingValue)

        #iterate through all of the grids and add them to the stak
        for grid in grids['data']:
            for index, variable in enumerate(self.climateParameters):
                gs._addGrid(variable = variable, date = grid[0].encode(), grid = grid[index+1])

        #If file Path and name are provided, export all grids
        if self.filePath:
            gs.export(filePath = self.filePath)
        return gs

    def _formatElems(self):
        '''
        Formats the ACIS request into elements
        '''
        elems = []
        for p in self.climateParameters:
            elems.append({'name':p,'interval':self.interval, 'duration' : self.duration, 'prec': self.precision})
        return elems

    def getDailyGrids(self, sdate, edate, unitCode = None, distance = 0,
        climateParameters = None, filePath = None):
        '''
        Method to fetch daily grids from ACIS.  Currently only PRISM grids are
        supported.

        ARGUMENTS
            sdate               Start date (yyyy-mm-dd or yyyymmdd).
            edate               End date (yyyy-mm-dd or yyyymmdd).
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
        self.unitCode = unitCode
        self.sdate = sdate
        self.edate = edate
        self.climateParameters = climateParameters

        self.interval = 'dly'
        self.duration = 'dly'
        self.distance = distance
        self.filePath = filePath
        return self._callForGrids()

    def getMonthlyGrids(self, sdate, edate, unitCode = None, distance = 0,
        climateParameters = None, filePath = None):
        '''
        Method to fetch monthly grids from ACIS.  Currently only PRISM grids are
        supported.

        ARGUMENTS
            sdate               Start date (yyyy-mm,yyyy-mm-dd, yymm, yyyymmdd).
            edate               End date (yyyy-mm, yyyy-mm-dd, yymm, or yyyymmdd).
            unitCode (optional) 4-letter unit code. Currently accepts only one.
            distance (optional) Distance in kilometers for buffering a bounding box of park.
                                If no distance is specified then 0 is used as the default buffer.
            climateParameters (optional)    Accepts one or more of the climate parameter codes,
                                            preferably as a list or tuple
            filePath (optional)             If provided, one or more ascii grids are saved to the
                                    working directory. Grid names follow the pattern of
                                    Source_parameter_aggregation_YYYYMMDD (e.g., PRISM_mint_dly_20150101)

        RETURNS
            Dictionary like object (aka GridStack) containing one or more monthly grids.
            Grids are indexed first by parameter and then by date
        '''
        self.unitCode = unitCode
        self.sdate = sdate
        self.edate = edate
        '''
        #NOTE: PRISM Supports MLY: Maximum Temperature, Minimum Temperature, Precipitation
        mly_maxt	91	Monthly mean maximum temperature (?F)
        mly_mint	92	Monthly mean minimum temperature (?F)
        mly_avgt	99	Monthly mean average temperature (?F)
        mly_pcpn	94	Monthly precipitation sum(inches)
        '''
        self.interval = 'mly'
        self.duration = 'mly'
        self.climateParameters = self._formatStringArguments(climateParameters, self.supportedParameters)
        self.climateParameters = map(lambda p: self.duration + '_' + p, self.climateParameters)
        self.distance = distance
        self.filePath = filePath
        return self._callForGrids()

if __name__ == '__main__':
    gr = GridRequestor()
    filePath = 'C:\\TEMP\\'

    ##MONTHLY GRIDS

    #TEST 01
    sdate = '1895-01'
    edate = '1896-12'
    climateParameters = ['mint', 'maxt']
    unitCode = 'YELL'
    distance = 0

    data =  gr.getMonthlyGrids(sdate = sdate, edate = edate,
        unitCode = unitCode, distance = distance,
        climateParameters = climateParameters, filePath = filePath )
    print data.climateParameters
    print data.dates
    data.export(filePath = filePath)
    print data['mly_mint']['1895-01']
    print data.dates
    print data.climateParameters
    data['mly_mint']['1895-01'].export(filePathAndName = filePath + 'test.asc')

    #Test 02
    unitCode = 'OLYM'
    sdate = '20150115'
    edate = '20150615'
    climateParameters = ['maxt']
    distance = 0
    data =  gr.getMonthlyGrids(sdate = sdate, edate = edate,
        unitCode = unitCode, distance = distance,
        climateParameters = climateParameters, filePath = filePath )


    ##DAILY GRIDS
    #TEST 01
    sdate = '2015-01-01'
    edate = '2015-01-04'
    climateParameters = 'mint, maxt'
    unitCode = 'YELL'
    distance = 0

    data =  gr.getDailyGrids(sdate = sdate, edate = edate,
        unitCode = unitCode, distance = distance,
        climateParameters = climateParameters, filePath = filePath )
    print data.climateParameters
    print data.dates
    data.export(filePath = filePath)
    print data['mint']['2015-01-03']
    print data.dates
    print data.climateParameters
    data['mint']['2015-01-03'].export(filePathAndName = filePath + 'test.asc')

    #Test 02
    unitCode = 'OLYM'
    sdate = '20150615'
    edate = '20150615'
    climateParameters = ['maxt']
    distance = 0
    data =  gr.getDailyGrids(sdate = sdate, edate = edate,
    unitCode = unitCode, distance = distance,
    climateParameters = climateParameters, filePath = filePath )


