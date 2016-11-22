from common import missingValue

class Observation(dict):

    def __init__(self, values):
        self['date'] = values[0].encode()
        self['wxOb']  = values[1].encode()
        self._replaceBlanks()

    @property
    def date(self):
        return self['date']

    @property
    def wxOb(self):
        return self['wxOb']

    def _replaceBlanks(self):
        #replace blanks with the missing value
        for index, value in self.items():
            if len(value.strip()) == 0:
                self[index] = missingValue

class DailyWxOb(Observation):
    ''''
    A dictionary containing a weather observation for a specific station, parameter and date
    WxOb is indexable like a standard dictionary although values can also
    be accessed as properties:
        -WxOb.date
        -WxOb.wxOb, etc).
        -WxOb.ACIS_Flag
        -WxOb.sourceFlag
    '''
    def __init__(self, values):

        self['ACIS_Flag'] = values[2].encode()
        self['sourceFlag'] = values[3].encode()
        super(DailyWxOb, self).__init__(values)

    @property
    def ACIS_Flag(self):
        return self['ACIS_Flag']
    @property
    def sourceFlag(self):
        return self['sourceFlag']


    def toList(self, includeDate = True):
        l = [self.wxOb, self.ACIS_Flag, self.sourceFlag]
        if includeDate:
            l.insert(0, self.date)
        return l

class MonthlyWxOb(Observation):
    def __init__(self, values):
        super(MonthlyWxOb, self).__init__(values)
        self['countMissing'] = values[2]

    @property
    def countMissing(self):
        return self['countMissing']

    def toList(self, includeDate = True):
        l = [self.wxOb, str(self.countMissing)]
        if includeDate:
            l.insert(0, self.date)
        return l

if __name__=='__main__':

    #Daily data
    data = ['2012-02-01',u'32.0', u' ', u'U']
    wx = DailyWxOb(data)
    print wx

    #Monthly data
    data = [u'2012-01', u'22.60', 0]
    dmonth = MonthlyWxOb(data)
    print dmonth
    print dmonth.toList()
