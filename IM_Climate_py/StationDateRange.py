import datetime
from common import missingValue, formatStringArguments
from datetime import date

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
            return self.minRange + ':' + self.maxRange
        except:
            return missingValue

    @property
    def climateParameters(self):
        return self.keys()

    def __str__(self):
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

    def _addDates(self, dateRanges, climateParameters):

        #if there aren't any climate parameters, terminate. Otherwise, set the climate
        #parameters to an iterable list
        if not climateParameters:
            return
        if type(climateParameters) == str:
            climateParameters = formatStringArguments(climateParameters)

        #Assign Begin and End Dates to Each Parameter
        for index, p in enumerate(climateParameters):
            try:
                b =  dateRanges[index][0]
                e = dateRanges[index][1]
                self[p] = {'begin': date(int(b[0:4]), int(b[5:7]), int(b[8:10])),
                    'end': date(int(e[0:4]), int(e[5:7]), int(e[8:10]))}
            except:
                self[p] = {'begin': missingValue, 'end': missingValue}

        #Calculate the range of dates based on all parameters
        self._minRange = date(2100,1,1)
        self._maxRange = date(1492,1,1)
        for p in self.items():
            if p[1]['begin'] <> missingValue:
                if p[1]['begin'] < self._minRange:
                    self._minRange = p[1]['begin']
            if p[1]['end'] <> missingValue:
                if p[1]['end'] > self._maxRange:
                    self._maxRange = p[1]['end']

        #Prevent non-sensical dates from being returned
        if self._minRange == date(2100,1,1):
            self._minRange = missingValue
        if self._maxRange == date(1492,1,1):
            self._maxRange = missingValue


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
    print dr['avgt']
    print (dr.climateParameters)
    print (dr.allRanges)