import unittest
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
        List stations IDs for stations around NOCA within a 30km buffer.
        '''
        info = [78568,
                         17675,
                         29457,
                         39793,
                         17579,
                         25054,
                         17591,
                         30909,
                         17598,
                         17611,
                         17605,
                         25030,
                         25031,
                         25032,
                         25033,
                         25034,
                         55883,
                         25036,
                         25037,
                         25038,
                         77391,
                         25041,
                         25042,
                         25043,
                         25044,
                         25046,
                         25047,
                         64986,
                         25051,
                         25052,
                         71390,
                         25056,
                         25057,
                         25058,
                         25059,
                         25060,
                         25061,
                         79206,
                         60903,
                         60904,
                         25065,
                         60906,
                         39784,
                         69843,
                         39798,
                         60905,
                         39804]

        sf = StationFinder()
        wxStations = sf.findStation(parkCodes = 'MABI', distance = 30)
        self.assertListEqual(info, wxStations.stationIDs)


if __name__ == '__main__':
    unittest.main()