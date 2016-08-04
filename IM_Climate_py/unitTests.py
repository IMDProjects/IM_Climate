import unittest
from sets import Set
from StationDateRange import StationDateRange
from StationFinder import StationFinder


class Test_StationDateRanges(unittest.TestCase):

    def test_dateRanges(self):
        dateRanges = [[u'1999-10-01', u'2016-07-24'],
                                 [u'1999-10-28', u'2016-07-25'],
                                 []]
        parameters = ['mint', 'maxt', 'avgt']
        dr = StationDateRange(dateRanges = dateRanges, climateParameters = parameters)

        self.assertEquals(dr.begin.isoformat(), '1999-10-01')
        self.assertEquals (dr.end.isoformat(),'2016-07-25')
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


if __name__ == '__main__':
    unittest.main()