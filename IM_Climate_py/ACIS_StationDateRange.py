from ACIS import missingValue
from StationDateRange import StationDateRange

class ACIS_StationDateRange(StationDateRange):
    '''
    Dictionary containing the valid date ranges for each weather parameter
    for a specific station
    '''
    def __init__(self, dateRanges, climateParameters):
        '''
        NOTE: climate parameters can be either a list, tuple,
                 or a comma-delimited string
        '''
        super(ACIS_StationDateRange, self).__init__(dateRanges, climateParameters)

    def _addDates(self, dateRanges, climateParameters):
        if not climateParameters:
            return
        if type(climateParameters) == str:
            climateParameters = climateParameters.split(',')


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
        self._maxRange =  date(1492,1,1)

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
    print dr.minRange
    print dr.maxRange
    print dr['avgt']
    print dr
    print dr.validDateRange
    print (dr.climateParameters)
    print (dr.allRanges)