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
        stations = sf.findStation(unitCode = 'ROMO', distance = 30, climateParameters = 'maxt, mint')
        test_data = numpy.array(stations._dumpMetaToList())

        refFile = open('../TestExamples/StationFinder/SF_Test01.csv')
        #refFile = open('../TestExamples/StationFinder/SF_Test01.csv')
        ref_data = []
        for line in refFile.readlines():
            ref_data.append(line.rstrip('\n').split(','))
        ref_data = numpy.array(ref_data)
        self.assertEquals(list(numpy.setdiff1d(ref_data[:,[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]]
            ,test_data[:,[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]])),[])
        refFile.close()

    def test02(self):
        sf = StationFinder()
        stations = sf.findStation(unitCode = 'AGFO', distance = 10)
        test_data = numpy.array(stations._dumpMetaToList())

        refFile = open('../TestExamples/StationFinder/SF_Test02.csv')
        ref_data = []
        for line in refFile.readlines():
            ref_data.append(line.rstrip('\n').split(','))
        ref_data = numpy.array(ref_data)
        self.assertTrue(numpy.array_equal(ref_data[:,[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]],
            test_data[:,[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]] ))
        refFile.close()



    def test_StationIDs(self):
        '''
        List stations IDs for stations around NOCA within a 20km buffer. List only
        stations collecting data on January 1, 1940.
        '''
        stations = Set([25057, 17605, 25047, 25051, 25052, 25054])

        sf = StationFinder()
        wxStations = sf.findStation(unitCode = 'MABI', distance = 20, sdate = '1940-01-01', edate = '1940-01-01')
        self.assertSetEqual(stations, Set(wxStations.stationIDs))

        #Check station metadata properties
        station = wxStations[25057]
        self.assertEqual(station.name,'BETHEL')
        self.assertEqual(station.latitude,43.83333)
        self.assertEqual(station.longitude,-72.63333)
        self.assertEqual(station.sid1, '430660 2')
        self.assertEqual(station.sid1_type, 'COOP')
        self.assertEqual(station.state, 'VT')
        self.assertEqual(station.elev, 541.0)
        self.assertEqual(station.uid, 25057)

    def test_DocumentationExample(self):
        sf = StationFinder()
        wxStations = sf.findStation(unitCode = 'MABI', distance = 30,
            sdate = '1940-01-01', edate = '1940-01-01',
            climateParameters = 'mint, maxt')
        self.assertEquals(len(wxStations.stationIDs), 6)


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
        dr = DataRequestor()
        wxData =  dr.getDailyWxObservations(climateStations =  25056,
            climateParameters = ['pcpn', 'avgt', 'obst', 'mint', 'maxt']
            ,sdate = '20150801', edate = '20150804')
        wxData.export('temp.csv')
        infile = open('temp.csv','r')
        testData = infile.read()
        refDataFile = open('../TestExamples/DataRequestor/DR_Test01.csv')
        refData = refDataFile.read()
        self.assertEqual(testData,refData)

        infile.close()
        refDataFile.close()
        os.remove('temp.csv')

    def test02(self):
        dr = DataRequestor()
        wxData =  dr.getDailyWxObservations(climateStations =  30433,
            climateParameters = 'pcpn'
            ,sdate = '2015-08-01', edate = '2015-08-04')
        wxData.export('temp.csv')
        infile = open('temp.csv','r')
        testData = infile.read()
        refDataFile = open('../TestExamples/DataRequestor/DR_Test02.csv')
        refData = refDataFile.read()
        self.assertEqual(testData,refData)

        infile.close()
        refDataFile.close()
        os.remove('temp.csv')

    def test03(self):
        sf = StationFinder()
        stationList = sf.findStation(unitCode = 'AGFO', distance = 10)
        dr = DataRequestor()
        wxData = dr.getDailyWxObservations(climateStations = stationList,
            climateParameters = 'pcpn'
            ,sdate = '2015-08-01', edate = '2015-08-04')
        wxData.export('temp.csv')
        infile = open('temp.csv','r')
        testData = infile.read()
        refDataFile = open('../TestExamples/DataRequestor/DR_Test03.csv')
        refData = refDataFile.read()
        self.assertEqual(list(numpy.setdiff1d(testData, refData)),[])
        #self.assertEqual(testData,refData)

        infile.close()
        refDataFile.close()
        os.remove('temp.csv')



if __name__ == '__main__':
    unittest.main()