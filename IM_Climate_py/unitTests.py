import unittest
from sets import Set
from StationDateRange import StationDateRange
from StationFinder import StationFinder
import datetime


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
        List stations IDs for stations around NOCA within a 20km buffer. List only
        stations collecting data on January 1, 1940.
        '''
        stations = Set([25057, 25054, 25047])

        sf = StationFinder()
        wxStations = sf.findStation(parkCodes = 'MABI', distance = 20, sDate = '1940-01-01', eDate = '1940-01-01')
        self.assertSetEqual(stations, Set(wxStations.stationIDs))

    def test02(self):
        '''
        Confirm that the start/end dates returned for a station are always the same
        '''
        sf = StationFinder()
        wxStations = sf.findStation(parkCodes = 'ROMO', climateParameters = 'mint, maxt, pcpn, snwd')
        self.assertEqual(wxStations[4072].validDateRange['mint']['begin'], datetime.date(1939, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['pcpn']['begin'], datetime.date(1907, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['snwd']['begin'], datetime.date(1908, 10, 19))

        wxStations = sf.findStation(parkCodes = 'ROMO', climateParameters = 'pcpn, snwd ,mint, maxt')
        self.assertEqual(wxStations[4072].validDateRange['mint']['begin'], datetime.date(1939, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['pcpn']['begin'], datetime.date(1907, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['snwd']['begin'], datetime.date(1908, 10, 19))

        wxStations = sf.findStation(parkCodes = 'ROMO', climateParameters = 'snwd ,mint, maxt, pcpn')
        self.assertEqual(wxStations[4072].validDateRange['mint']['begin'], datetime.date(1939, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['pcpn']['begin'], datetime.date(1907, 10, 1))
        self.assertEqual(wxStations[4072].validDateRange['snwd']['begin'], datetime.date(1908, 10, 19))



if __name__ == '__main__':
    unittest.main()