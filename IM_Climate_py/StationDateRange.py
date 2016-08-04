from datetime import date
import datetime
from ACIS import missingValue

class StationDateRange(dict):
    '''
    Dictionary containing the valid date ranges for each weather parameter
    for a specific station
    '''
    def __init__(self, dateRanges, climateParameters):
        if not climateParameters:
            return

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
        self.begin = date(2100,1,1)
        self.end =  date(1492,1,1)

        for p in self.items():
            if p[1]['begin'] <> missingValue:
                if p[1]['begin'] < self.begin:
                    self.begin = p[1]['begin']
            if p[1]['end'] <> missingValue:
                if p[1]['end'] > self.end:
                    self.end = p[1]['end']

        #Prevent non-sensical dates from being returned
        if self.begin == date(2100,1,1):
            self.begin = missingValue
        if self.end == date(1492,1,1):
            self.end = missingValue

    @property
    def validDateRange(self):
        try:
            return self.begin.strftime('%Y-%m-%d') + ':' + self.end.strftime('%Y-%m-%d')
        except:
            return missingValue

    def __repr__(self):
        return  self.validDateRange


if __name__ == '__main__':


    dateRanges = [[u'1999-10-01', u'2016-07-24'],
                                 [u'1999-10-28', u'2016-07-25'],
                                 []]
    parameters = ['mint', 'maxt', 'avgt']
    dr = StationDateRange(dateRanges = dateRanges, climateParameters = parameters)
    print dr.begin
    print dr.end
    print dr['avgt']
    print dr
    print dr.validDateRange