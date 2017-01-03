import unittest
from sets import Set
import datetime
import os
import sys
import numpy
import csv

sys.path.append(r'C:\CODE\IM_Climate\IM_Climate_py')
from StationDateRange import StationDateRange
from StationFinder import StationFinder
from StationDataRequestor import StationDataRequestor
from GridRequestor import GridRequestor

class Test_StationFinder(unittest.TestCase):

    default_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]
    testColumns = default_columns

    rootFolder = '../TestExamples/StationFinder/'
    def confirmContent_NoOrder(self):
        '''
        Confirms that all information is the same except for the maxRange field.
        Order is ignored
        '''
        sf = StationFinder()
        stations = sf.findStation(unitCode = self.unitCode, distance = self.distance,
            climateParameters = self.climateParameters, sdate = self.sdate, edate = self.edate)
        test_data = numpy.array(stations._dumpMetaToList())
        ref_data = []
        with open(Test_StationFinder.rootFolder + self.refFile, 'r')as refFile:
            r = csv.reader(refFile)
            for line in r:
                ref_data.append(line)
        ref_data = numpy.array(ref_data)

        refFile.close()
        self.results =  list(numpy.setdiff1d(ref_data[:,Test_StationFinder.testColumns]
            ,test_data[:,Test_StationFinder.testColumns]))

    def test01(self):
        self.unitCode = 'ROMO'
        self.distance = 30
        self.climateParameters = 'maxt, mint'
        self.sdate = None
        self.edate = None
        self.refFile = 'SF_Test01.csv'
        self.confirmContent_NoOrder()
        self.assertEquals(self.results, [])

    def test01_R(self):
        Test_StationFinder.testColumns = [0,1,2,4,5,6,7,8,9,10,12,14]
        self.unitCode = 'ROMO'
        self.distance = 30
        self.climateParameters = 'maxt, mint'
        self.sdate = None
        self.edate = None
        self.refFile = 'Test01_R.csv'
        self.confirmContent_NoOrder()
        Test_StationFinder.testColumns = Test_StationFinder.default_columns
        self.assertEquals(self.results, [])

    def test02(self):
        self.unitCode = 'AGFO'
        self.distance = 10
        self.climateParameters = None
        self.sdate = None
        self.edate = None
        self.refFile = 'SF_Test02.csv'
        self.confirmContent_NoOrder()
        self.assertEquals(self.results, [])

    def test02_R(self):
        Test_StationFinder.testColumns = [0,1,2,3,4,5,6,7,8,9,10,12,14]
        self.unitCode = 'AGFO'
        self.distance = 10
        self.climateParameters = None
        self.sdate = None
        self.edate = None
        self.refFile = 'Test02_R.csv'
        self.confirmContent_NoOrder()
        Test_StationFinder.testColumns = Test_StationFinder.default_columns
        self.assertEquals(self.results, [])

class Test_StationDataRequestor_getDailyWxObs(unittest.TestCase):

    rootFolder = '../TestExamples/StationDataRequestor/getDailyWxObservations/'
    def confirmContent(self):
        '''
        Confirms that all information is the same, ignoring record order
        '''
        dr = StationDataRequestor()
        wxData =  dr.getDailyWxObservations(climateStations =  self.climateStations,
            climateParameters = self.climateParameters
            ,sdate = self.sdate, edate = self.edate)
        wxData.export('temp.csv')
        infile = open('temp.csv','r')
        testData = infile.read()
        refDataFile = open(Test_StationDataRequestor_getDailyWxObs.rootFolder + self.refDataFile, 'r')
        refData = refDataFile.read()
        infile.close()
        refDataFile.close()
        os.remove('temp.csv')
        self.result =  list(numpy.setdiff1d(refData.split('/n'), testData.split('/n')))

    def test01(self):
        self.climateStations =  25056
        self.climateParameters = ['pcpn', 'avgt', 'obst', 'mint', 'maxt']
        self.sdate = '20150801'
        self.edate = '20150804'
        self.refDataFile = 'Test01_Py.csv'
        self.confirmContent()
        self.assertEqual(self.result,[])

    def test02(self):
        self.climateStations =  30433
        self.climateParameters = 'pcpn'
        self.sdate = '2015-08-01'
        self.edate = '2015-08-04'
        self.refDataFile = 'Test02_Py.csv'
        self.confirmContent()
        self.assertEqual(self.result,[])

    def test03(self):
        sf = StationFinder()
        stationList = sf.findStation(unitCode = 'AGFO', distance = 10)
        self.climateStations = stationList
        self.climateParameters = 'pcpn'
        self.sdate = '2015-08-01'
        self.edate = '2015-08-04'
        self.refDataFile = 'Test03_Py.csv'
        self.confirmContent()
        self.assertEqual(self.result,[])

    def test04(self):
        sf = StationFinder()
        stationList = sf.findStation(unitCode = 'ACAD', distance = 20)
        self.climateStations = stationList
        self.climateParameters = None
        self.sdate = '2015-08-01'
        self.edate = '2015-08-04'
        self.refDataFile = 'Test04_Py.csv'
        self.confirmContent()
        self.assertEqual(self.result,[])

class Test_StationDataRequestor_getMonthlyWxSummaryByYear(unittest.TestCase):

    rootFolder = '../TestExamples/StationDataRequestor/getMonthlyWxSummaryByYear/'
    def confirmContent(self):
        '''
        Confirms that all information is the same, ignoring record order
        '''
        dr = StationDataRequestor()
        wxData =  dr.getMonthlyWxSummaryByYear(climateStations =  self.climateStations,
            climateParameters = self.climateParameters, reduceCodes = self.reduceCodes
            ,sdate = self.sdate, edate = self.edate, maxMissing = self.maxMissing,
            includeNormals = self.includeNormals, includeNormalDepartures = self.includeNormalDepartures)
        wxData.export('temp.csv')
        infile = open('temp.csv','r')
        testData = infile.read()
        refDataFile = open(Test_StationDataRequestor_getMonthlyWxSummaryByYear.rootFolder + self.refDataFile, 'r')
        refData = refDataFile.read()
        infile.close()
        refDataFile.close()
        os.remove('temp.csv')
        self.result =  list(numpy.setdiff1d(refData.split('/n'), testData.split('/n')))

    def test01(self):
        self.climateStations =  '61193, 26215'
        self.climateParameters = None
        self.reduceCodes = None
        self.sdate = '201401'
        self.edate = '201501'
        self.maxMissing = 1
        self.includeNormals = False
        self.includeNormalDepartures = False
        self.refDataFile = 'Test01_Py.csv'
        self.confirmContent()
        self.assertEqual(self.result,[])

##    def test01_R(self):
##        self.climateStations =  '61193, 26215'
##        self.climateParameters = None
##        self.reduceCodes = None
##        self.sdate = '201401'
##        self.edate = '201501'
##        self.maxMissing = None
##        self.includeNormals = False
##        self.includeNormalDepartures = False
##        self.refDataFile = 'Test01_R.csv'
##        self.confirmContent()
##        self.assertEqual(self.result,[])

    def test02(self):
        self.climateStations =  26215
        self.climateParameters = 'pcpn'
        self.reduceCodes = 'min'
        self.sdate = None
        self.edate = '2016-09'
        self.maxMissing = 2
        self.includeNormals = False
        self.includeNormalDepartures = False
        self.refDataFile = 'Test02_Py.csv'
        self.confirmContent()
        self.assertEqual(self.result,[])

    #THIS IS FAILING BECAUSE OF THE ELEVATION PRECISION
##    def test02_R(self):
##        self.climateStations =  26215
##        self.climateParameters = 'pcpn'
##        self.reduceCodes = 'min'
##        self.sdate = None
##        self.edate = '2016-09'
##        self.maxMissing = 2
##        self.refDataFile = 'Test02_R.csv'
##        self.confirmContent()
##        self.assertEqual(self.result,[])


    def test03(self):
        self.climateStations =  29699
        self.climateParameters = 'maxt'
        self.reduceCodes = 'mean'
        self.sdate = '2003-01'
        self.edate = '2003-02'
        self.maxMissing = 1
        self.includeNormals = True
        self.includeNormalDepartures = True
        self.refDataFile = 'Test03_Py.csv'
        self.confirmContent()
        self.assertEqual(self.result,[])

class Test_GridRequestor(unittest.TestCase):
    rootFolder = '../TestExamples/GridRequestor/'
    gr = GridRequestor()
    def confirmAsciiGrid(self):

        data =  self.method(sdate = self.sdate, edate = self.edate,
            unitCode = self.unitCode, distance = self.distance,
            climateParameters = self.climateParameters)
        testDataFile = data.export()[0]
        testFile = open(testDataFile,'r')
        testData = testFile.read()
        testFile.close()
        os.remove(testDataFile)
        os.remove(testDataFile[:-3] + 'prj')
        refDataFile = open(Test_GridRequestor.rootFolder + self.refDataFile,'r')
        refData = refDataFile.read()
        refDataFile.close()
        self.result =  list(numpy.setdiff1d(refData.split('/n'),testData.split('/n')))

    def test_getDailyGrids_01(self):
        #DAILY GRID - PRISM
        self.method = self.gr.getDailyGrids
        self.sdate = '2015-01-01'
        self.edate = '2015-01-01'
        self.climateParameters = 'mint'
        self.unitCode = 'APPA'
        self.distance = 0
        self.refDataFile = 'getDailyGrids/Test01/PY_PRISM_mint_dly_2015-01-01.asc'
        self.confirmAsciiGrid()
        self.assertEquals(self.result,[])


##    def test_getDailyGrids_01_R(self):
##        self.method = self.gr.getMonthlyGrids
##        self.sdate = '2015-01-01'
##        self.edate = '2015-01-01'
##        self.climateParameters = 'mint'
##        self.unitCode = 'APPA'
##        self.distance = 0
##        self.refDataFile = 'getDailyGrids/Test01/R_PRISM_mint_dly_2015-01-01.asc'
##        self.confirmAsciiGrid()
##        self.assertEquals(self.result,[])

    def test_getMonthlyGrids_01(self):
        #MONTHLY GRID - PRISM
        self.method = self.gr.getMonthlyGrids
        self.sdate = '1900-01'
        self.edate = '1900-01'
        self.climateParameters = 'mint'
        self.unitCode = 'GRKO'
        self.distance = 0
        self.refDataFile = 'getMonthlyGrids/Test01/PY_PRISM_mly_mint_mly_1900-01.asc'
        self.confirmAsciiGrid()
        self.assertEquals(self.result,[])

    def test_getMonthlyGrids_01_R(self):
        #MONTHLY GRID - PRISM
        self.method = self.gr.getMonthlyGrids
        self.sdate = '1900-01'
        self.edate = '1900-01'
        self.climateParameters = 'mint'
        self.unitCode = 'GRKO'
        self.distance = 0
        self.refDataFile = 'getMonthlyGrids/Test01/R_PRISM_mly_mint_mly_1900-01.asc'
        self.confirmAsciiGrid()
        self.assertEquals(self.result,[])


    def test_getYearlyGrids_01(self):
        #PRISM
        self.method = self.gr.getYearlyGrids
        self.sdate = '1970'
        self.edate = '1970'
        self.climateParameters = 'pcpn'
        self.unitCode = 'ARPO'
        self.distance = 5
        self.refDataFile = 'getYearlyGrids/Test01/PY_PRISM_yly_pcpn_yly_1970.asc'
        self.confirmAsciiGrid()
        self.assertEquals(self.result,[])


class Test_StationDataRequestor_getYearlyWxSummary(unittest.TestCase):

    rootFolder = '../TestExamples/StationDataRequestor/getYearlyWxSummary/'
    def confirmContent(self):
        '''
        Confirms that all information is the same, ignoring record order
        '''
        dr = StationDataRequestor()
        wxData =  dr.getYearlyWxSummary(climateStations =  self.climateStations,
            climateParameters = self.climateParameters, reduceCodes = self.reduceCodes
            ,sdate = self.sdate, edate = self.edate, maxMissing = self.maxMissing,
            includeNormals = self.includeNormals, includeNormalDepartures = self.includeNormalDepartures)
        wxData.export('temp.csv')
        infile = open('temp.csv','r')
        testData = infile.read()
        refDataFile = open(Test_StationDataRequestor_getYearlyWxSummary.rootFolder + self.refDataFile, 'r')
        refData = refDataFile.read()
        infile.close()
        refDataFile.close()
        os.remove('temp.csv')
        self.result =  list(numpy.setdiff1d(refData.split('/n'), testData.split('/n')))

    def test01(self):
        self.climateStations =  29699
        self.climateParameters = 'mint'
        self.reduceCodes = 'mean'
        self.sdate = 2001
        self.edate = 2005
        self.maxMissing = 0
        self.includeNormals = True
        self.includeNormalDepartures = True
        self.refDataFile = 'Test01_Py.csv'
        self.confirmContent()
        self.assertEqual(self.result,[])

class Test_StationDataRequestor_getDayCountByThreshold(unittest.TestCase):

    rootFolder = '../TestExamples/StationDataRequestor/getDayCountByThreshold/'
    def confirmContent(self):
        '''
        Confirms that all information is the same, ignoring record order
        '''
        dr = StationDataRequestor()
        wxData =  dr.getDayCountByThreshold(climateStations =  self.climateStations,
            climateParameters = self.climateParameters
            ,sdate = self.sdate, edate = self.edate, thresholdValue = self.thresholdValue,
            timeInterval = self.timeInterval, thresholdType = self.thresholdType)

        wxData.export('temp.csv')
        infile = open('temp.csv','r')
        testData = infile.read()
        refDataFile = open(Test_StationDataRequestor_getDayCountByThreshold.rootFolder + self.refDataFile, 'r')
        refData = refDataFile.read()
        infile.close()
        refDataFile.close()
        os.remove('temp.csv')
        self.result =  list(numpy.setdiff1d(refData.split('/n'), testData.split('/n')))

    def test01(self):
        self.climateStations =  29699
        self.climateParameters = 'mint'
        self.sdate = '200101'
        self.edate = '200105'
        self.thresholdValue = 90
        self.thresholdType = 'gt'
        self.timeInterval = 'mly'
        self.refDataFile = 'Test01_Py.csv'
        self.confirmContent()
        self.assertEqual(self.result,[])

    def test02(self):
        self.climateStations =  29699
        self.climateParameters = 'mint'
        self.sdate = 2001
        self.edate = 2010
        self.thresholdValue = 10
        self.thresholdType = 'le'
        self.timeInterval = 'yly'
        self.refDataFile = 'Test02_Py.csv'
        self.confirmContent()
        self.assertEqual(self.result,[])

if __name__ == '__main__':
    unittest.main()