from datetime import date
import datetime
from common import missingValue

class StationDateRange(dict):
    '''
    Dictionary containing the valid date ranges for each weather parameter
    for a specific station
    '''
    def __init__(self, dateRanges, climateParameters):
        '''
        NOTE: climate parameters can be either a list, tuple,
                 or a comma-delimited string
        '''
        self._maxRange = missingValue
        self._minRange = missingValue
        self._addDates(dateRanges, climateParameters)


    def _addDates(self, dateRanges, climateParameters):
        pass #Method needs to be defined in child class

    @property
    def validDateRange(self):
        try:
            return self._minRange.strftime('%Y-%m-%d') + ':' + self._maxRange.strftime('%Y-%m-%d')
        except:
            return missingValue

    @property
    def climateParameters(self):
        return self.keys()

    def __repr__(self):
        return  self.validDateRange

    @property
    def allRanges(self):
        return self.viewitems()

    @property
    def maxRange(self):
        if self._maxRange == missingValue:
            return missingValue
        else:
            return self._maxRange.isoformat()

    @property
    def minRange(self):
        if self._minRange == missingValue:
            return missingValue
        return self._minRange.isoformat()


if __name__ == '__main__':


    dateRanges = [[u'1999-10-01', u'2016-07-24'],
                                 [u'1999-10-28', u'2016-07-25'],
                                 []]
    parameters = ['mint', 'maxt', 'avgt']
    parameters = 'mint', 'maxt', 'avgt'
    dr = StationDateRange(dateRanges = dateRanges, climateParameters = parameters)
    dr._minRange = date(1990,1,1)
    dr._maxRange = date(2015,12,31)
    print dr.minRange
    print dr.maxRange
    print dr
    print dr.validDateRange
##    print dr['avgt']
##    print (dr.climateParameters)
##    print (dr.allRanges)