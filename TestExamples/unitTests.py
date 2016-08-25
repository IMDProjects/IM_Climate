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


class Test_StationDateRanges(unittest.TestCase):

    def test_dateRanges(self):
        dateRanges = [[u'1999-10-01', u'2016-07-24'],
                                 [u'1999-10-28', u'2016-07-25'],
                                 []]
        parameters = ['mint', 'maxt', 'avgt']
        dr = StationDateRange(dateRanges = dateRanges, climateParameters = parameters)

        self.assertEquals(dr.minRange, '1999-10-01')
        self.assertEquals (dr.maxRange,'2016-07-25')
        self.assertEquals(dr['avgt'], {'begin': 'NA', 'end': 'NA'})

class Test_StationFinder(unittest.TestCase):

    def test01(self):
        '''
        Confirms that all information is the same except for the maxRannge field
        '''
        sf = StationFinder()
        stations = sf.findStation(unitCode = 'ROMO', distance = 30, climateParameters = 'maxt, mint'
            ,filePathAndName = 'SF01.csv')
        test_data = numpy.array(stations._dumpMetaToList())

        refFile = open('../TestExamples/StationFinder/Test01.csv')
        ref_data = []
        for line in refFile.readlines():
            ref_data.append(line.rstrip('\n').split(','))
        ref_data = numpy.array(ref_data)
        self.assertTrue(numpy.array_equal(ref_data[:,1:13],test_data[:,1:13] ))
        self.assertTrue(numpy.array_equal(ref_data[:,14],test_data[:,14] ))

        refFile.close()


    def test_StationIDs(self):
        '''
        List stations IDs for stations around NOCA within a 20km buffer. List only
        stations collecting data on January 1, 1940.
        '''
        stations = Set([25057, 25054, 25047])

        sf = StationFinder()
        wxStations = sf.findStation(unitCode = 'MABI', distance = 20, sDate = '1940-01-01', eDate = '1940-01-01')
        self.assertSetEqual(stations, Set(wxStations.stationIDs))

    def test_dates(self):
        '''
        Confirm that the start/end dates returned for a station are always the same
        '''
        sf = StationFinder()
        wxStations = sf.findStation(unitCode = 'ROMO', climateParameters = 'mint, maxt, pcpn, snwd')
        self.assertEqual(wxStations[4072].validDateRange['mint']['begin'], datetime.date(1939, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['pcpn']['begin'], datetime.date(1907, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['snwd']['begin'], datetime.date(1908, 10, 19))

        wxStations = sf.findStation(unitCode = 'ROMO', climateParameters = 'pcpn, snwd ,mint, maxt')
        self.assertEqual(wxStations[4072].validDateRange['mint']['begin'], datetime.date(1939, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['pcpn']['begin'], datetime.date(1907, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['snwd']['begin'], datetime.date(1908, 10, 19))

        wxStations = sf.findStation(unitCode = 'ROMO', climateParameters = 'snwd ,mint, maxt, pcpn')
        self.assertEqual(wxStations[4072].validDateRange['mint']['begin'], datetime.date(1939, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['pcpn']['begin'], datetime.date(1907, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['snwd']['begin'], datetime.date(1908, 10, 19))

class Test_DataRequestor(unittest.TestCase):
    def test01(self):
        '''
        list('pcpn', 'avgt', 'obst', 'mint', 'maxt'), 25056, "20150801", "20150804")
        '''
        dr = DataRequestor()
        wxData =  dr.getDailyWxObservations(climateStations =  25056,
            climateParameters = ['pcpn', 'avgt', 'obst', 'mint', 'maxt']
            ,startDate = '20150801', endDate = '20150804')
        wxData.export('dr_test01.csv')
        infile = open('dr_test01.csv','r')
        testData = infile.read()
        refDataFile = open('../TestExamples/DataRequestor/Test01.csv')
        refData = refDataFile.read()
        self.assertEqual(testData,refData)

        infile.close()
        refDataFile.close()
        os.remove('dr_test01.csv')


if __name__ == '__main__':
    unittest.main()