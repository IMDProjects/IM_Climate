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
from DataRequestor import DataRequestor

class Test_StationFinder(unittest.TestCase):

    default_columns = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]
    testColumns = default_columns

    rootFolder = '../TestExamples/StationFinder/'
    def confirmContent_NoOrder(self):
        '''
        Confirms that all information is the same except for the maxRannge field.
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
        self.maxDiff = None
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
        self.maxDiff = None
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


class Test_DataRequestor(unittest.TestCase):

    rootFolder = '../TestExamples/DataRequestor/'
    def confirmContent(self):
        '''
        Confirms that all information the same, ignoring record order
        '''
        dr = DataRequestor()
        wxData =  dr.getDailyWxObservations(climateStations =  self.climateStations,
            climateParameters = self.climateParameters
            ,sdate = self.sdate, edate = self.edate)
        wxData.export('temp.csv')
        infile = open('temp.csv','r')
        testData = infile.read()
        refDataFile = open(Test_DataRequestor.rootFolder + self.refDataFile, 'r')
        refData = refDataFile.read()
        infile.close()
        refDataFile.close()
        os.remove('temp.csv')
        self.result =  list(numpy.setdiff1d(refData, testData))

    def test01(self):
        self.maxDiff = None
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

if __name__ == '__main__':
    unittest.main()