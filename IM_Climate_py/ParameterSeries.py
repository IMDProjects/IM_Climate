from WxOb import DailyWxOb
from WxOb import MonthlyWxOb

class DailyParameterSeries(dict):
    '''
    Dictionary(-like object) of all weather observations for a particular climate parameter
    A particular wx observation is indexable by date.
    ParameterSeries has been extended to be iterable like a list
    '''

    def __init__(self):
        self.observationClass = DailyWxOb

    def _set(self, pData, dates, parameter):
        self.parameter = parameter
        for index, value in enumerate(pData):
            date = [dates[index]]
            wo = date
            wo.extend(value)
            self[date[0]] = self.observationClass(wo)

    def __iter__(self):
        '''
        Allows the dictionary to iterate like a list
        '''
        for k in sorted(self.keys()):
            yield self[k]

class MonthlyParameterSeries(DailyParameterSeries):
    def __init__(self):
        self.observationClass = MonthlyWxOb

if __name__ == '__main__':


    data = [[u'21.5', u' ', u'U'],
         [u'29.5', u' ', u'U'],
         [u'32.0', u' ', u'U'],
         [u'27.5', u' ', u'U'],
         [u'35.5', u' ', u'U']]
    dates = (u'2012-01-01', u'2012-01-02', u'2012-01-03', u'2012-01-04', u'2012-01-05')
    parameter = 'maxt'
    ps = DailyParameterSeries()
    ps._set(data,dates,parameter)
    print ps