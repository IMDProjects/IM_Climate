

class ParameterSeries(dict):
    '''
    Dictionary(-like object) of all weather observations for a particular climate parameter
    A particular wx observation is indexable by date.
    ParameterSeries has been extended to be iterable like a list
    '''

    def __init__(self, observationClass, isNormal = False):
        '''
        isNormal - is the time series actual observations or the published normals
        '''

        self.observationClass = observationClass
        self.isNormal = isNormal

    def _set(self, pData, dates, parameter):

        '''
        Method to set the data for a a particular parameter series
        '''
        self.parameter = parameter
        for index, value in enumerate(pData):
            date = [dates[index]]
            wo = date[:]
            if type(value) == unicode:
                value = [value.encode()]
            wo.extend(value)
            self[date[0]] = self.observationClass(wo, isNormal = self.isNormal)

    def __iter__(self):
        '''
        Allows the dictionary to iterate like a list
        '''
        for k in sorted(self.keys()):
            yield self[k]

    def _createHeader(self):
        d = self.keys()[0]
        return self[d]._createHeader(self.parameter)


if __name__ == '__main__':

    from WxOb import DailyWxOb
    from WxOb import MonthlyWxOb
    data = [[u'21.5', u' ', u'U'],
         [u'29.5', u' ', u'U'],
         [u'32.0', u' ', u'U'],
         [u'27.5', u' ', u'U'],
         [u'35.5', u' ', u'U']]
    dates = (u'2012-01-01', u'2012-01-02', u'2012-01-03', u'2012-01-04', u'2012-01-05')
    parameter = 'maxt'
    ps = ParameterSeries(observationClass = DailyWxOb)
    ps._set(data,dates,parameter)
    print ps

    #MONTHLY
    parameter = 'maxt_mly'
    data = [[u'21.5', '0'],
         [u'29.5', '0'],
         [u'32.0', '0'],
         [u'27.5', '0'],
         [u'35.5', '4']]

    ps = ParameterSeries(observationClass = MonthlyWxOb)
    ps._set(data,dates,parameter)
    print ps
    print ps._createHeader()