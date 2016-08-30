import unittest
from sets import Set
import datetime
import os
import sys
import numpy

sys.path.append(r'C:\CODE\IM_Climate\IM_Climate_py')
from StationDateRange import StationDateRange
from StationFinder import StationFinder
from DataRequestor import DataRequestor


class Test_StationFinder(unittest.TestCase):
    def tmp(self):
        '''
        TEMPLATE
        '''
        sf = StationFinder()
        stations = sf.findStation(unitCode = self.unitCode, distance = self.distance,
            climateParameters = self.climateParameters, sdate = self.sdate, edate = self.edate)
        test_data = numpy.array(stations._dumpMetaToList())

        refFile = open(self.refFile)
        ref_data = []
        for line in refFile.readlines():
            ref_data.append(line.rstrip('\n').split(','))
        ref_data = numpy.array(ref_data)

        refFile.close()
        self.results =  list(numpy.setdiff1d(ref_data[:,[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]]
            ,test_data[:,[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]]))

    def test01(self):
        '''
        Confirms that all information is the same except for the maxRannge field
        '''
        self.unitCode = 'ROMO'
        self.distance = 30
        self.climateParameters = 'maxt, mint'
        self.sdate = None
        self.edate = None
        self.refFile = '../TestExamples/StationFinder/SF_Test01.csv'
        self.tmp()
        self.assertEquals(self.results, [])



    def test02(self):
        self.unitCode = 'AGFO'
        self.distance = 10
        self.climateParameters = None
        self.sdate = None
        self.edate = None
        self.refFile = '../TestExamples/StationFinder/SF_Test02.csv'
        self.tmp()
        self.assertEquals(self.results, [])


class Test_DataRequestor(unittest.TestCase):
    def tmp(self):
        '''
        TEST TEMPLATE
        '''
        dr = DataRequestor()
        wxData =  dr.getDailyWxObservations(climateStations =  self.climateStations,
            climateParameters = self.climateParameters
            ,sdate = self.sdate, edate = self.edate)
        wxData.export('temp.csv')
        infile = open('temp.csv','r')
        testData = infile.read()
        refDataFile = open(self.refDataFile, 'r')
        refData = refDataFile.read()

        infile.close()
        refDataFile.close()
        os.remove('temp.csv')
        self.result =  list(numpy.setdiff1d(refData, testData))

    def test01(self):
        self.climateStations =  25056
        self.climateParameters = ['pcpn', 'avgt', 'obst', 'mint', 'maxt']
        self.sdate = '20150801'
        self.edate = '20150804'
        self.refDataFile = '../TestExamples/DataRequestor/DR_Test01.csv'
        self.tmp()
        self.assertEqual(self.result,[])

    def test02(self):
        self.climateStations =  30433
        self.climateParameters = 'pcpn'
        self.sdate = '2015-08-01'
        self.edate = '2015-08-04'
        self.refDataFile = '../TestExamples/DataRequestor/DR_Test02.csv'
        self.tmp()
        self.assertEqual(self.result,[])

    def test03(self):
        sf = StationFinder()
        stationList = sf.findStation(unitCode = 'AGFO', distance = 10)
        self.climateStations = stationList
        self.climateParameters = 'pcpn'
        self.sdate = '2015-08-01'
        self.edate = '2015-08-04'
        self.refDataFile = '../TestExamples/DataRequestor/DR_Test03.csv'
        self.tmp()
        self.assertEqual(self.result,[])





if __name__ == '__main__':
    unittest.main()