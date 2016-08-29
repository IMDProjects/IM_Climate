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
    def tmp(self, unitCode, distance, climateParameters,sdate, edate, refFile):
        '''
        TEMPLATE
        '''
        sf = StationFinder()
        stations = sf.findStation(unitCode = unitCode, distance = distance,
            climateParameters = climateParameters, sdate = sdate, edate = edate)
        test_data = numpy.array(stations._dumpMetaToList())

        refFile = open(refFile)
        ref_data = []
        for line in refFile.readlines():
            ref_data.append(line.rstrip('\n').split(','))
        ref_data = numpy.array(ref_data)

        refFile.close()
        return list(numpy.setdiff1d(ref_data[:,[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]]
            ,test_data[:,[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]]))

    def test01(self):
        '''
        Confirms that all information is the same except for the maxRannge field
        '''
        results = self.tmp(unitCode = 'ROMO', distance = 30, climateParameters = 'maxt, mint',
                sdate = None, edate = None, refFile = '../TestExamples/StationFinder/SF_Test01.csv' )
        self.assertEquals(results, [])



    def test02(self):
        results = self.tmp(unitCode = 'AGFO', distance = 10, climateParameters = None,
                sdate = None, edate = None, refFile = '../TestExamples/StationFinder/SF_Test02.csv' )
        self.assertEquals(results, [])


class Test_DataRequestor(unittest.TestCase):
    def tmp(self, climateStations, climateParameters, sdate, edate, refDataFile):
        '''
        TEST TEMPLATE
        '''
        dr = DataRequestor()
        wxData =  dr.getDailyWxObservations(climateStations =  climateStations,
            climateParameters = climateParameters
            ,sdate = sdate, edate = edate)
        wxData.export('temp.csv')
        infile = open('temp.csv','r')
        testData = infile.read()
        refDataFile = open(refDataFile, 'r')
        refData = refDataFile.read()

        infile.close()
        refDataFile.close()
        os.remove('temp.csv')
        return list(numpy.setdiff1d(refData, testData))

    def test01(self):
        result = self.tmp(climateStations =  25056,
            climateParameters = ['pcpn', 'avgt', 'obst', 'mint', 'maxt']
            ,sdate = '20150801', edate = '20150804',
            refDataFile = '../TestExamples/DataRequestor/DR_Test01.csv')

        self.assertEqual(result,[])

    def test02(self):
        result = self.tmp(climateStations =  30433,
            climateParameters = 'pcpn'
            ,sdate = '2015-08-01', edate = '2015-08-04',
            refDataFile = '../TestExamples/DataRequestor/DR_Test02.csv')

        self.assertEqual(result,[])

    def test03(self):
        sf = StationFinder()
        stationList = sf.findStation(unitCode = 'AGFO', distance = 10)
        result = self.tmp(climateStations = stationList,
            climateParameters = 'pcpn'
            ,sdate = '2015-08-01', edate = '2015-08-04',
            refDataFile = '../TestExamples/DataRequestor/DR_Test03.csv')

        self.assertEqual(result,[])





if __name__ == '__main__':
    unittest.main()