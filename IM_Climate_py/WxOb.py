from common import missingValue # getSupportedParameters
from ACIS import ACIS
from abc import ABCMeta


class WxOb(dict):

    '''
    abstract base class for all other weather observations
    '''
    __metaclass__ = ABCMeta
    acis = ACIS()

    def __init__(self, values = None):
        if values:
            self['date'] = values[0].encode()

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


class DailyWxOb(WxOb):
    ''''
    A dictionary containing a weather observation for a specific station, parameter and date
    WxOb is indexable like a standard dictionary although values can also
    be accessed as properties:
        -WxOb.date
        -WxOb.wxOb, etc).
        -WxOb.ACIS_Flag
        -WxOb.sourceFlag
    '''
    def __init__(self, values = None,  isNormal = False):

        if values:
            self['wxOb']  = values[1]
            if not isNormal:
                self['ACIS_Flag'] = values[2].encode()
                self['sourceFlag'] = values[3].encode()
            super(DailyWxOb, self).__init__(values)
            self.isNormal = isNormal

    @property
    def ACIS_Flag(self):
        if not self.isNormal:
            return self['ACIS_Flag']
        else:
            return 'NA'
    @property
    def sourceFlag(self):
        if not self.isNormal:
            return self['sourceFlag']
        else:
            return 'NA'

    def toList(self, includeDate = True):
        if not self.isNormal:
            l = [self.wxOb, self.ACIS_Flag, self.sourceFlag]
        else:
            l = [self.wxOb]
        if includeDate:
            l.insert(0, self.date)
        return l

    def _createHeader(self, p):
        '''
        Creates the header needed when exporting to a text file
        '''
        if not self.isNormal:
            return [self.acis.supportedParameters[p]['label'], p+'_acis_flag', p+'_source_flag']
        else:
            return [self.acis.supportedParameters[p.split('_')[0]]['label'] + '_' + p.split('_')[1]]

class MonthlyWxOb(WxOb):
    '''
    Class to handle monthly weather observations a a list in the format of
    [u'2012-01', u'22.60', 0] or [Date, observation, count missing]

    If count missing is missing, the monthly weather observation is assumed to
    be a published normal

    '''
    def __init__(self, values = None, isNormal = False):
        super(MonthlyWxOb, self).__init__(values)
        if values:
            self['wxOb']  = values[1].encode()
            if not isNormal:
                self['countMissing'] = values[2]
        self.normal = isNormal

    @property
    def countMissing(self):
        if not self.normal:
            return self['countMissing']
        else:
            return 'NA'

    def toList(self, includeDate = True):
        if self.normal:
            l = [self.wxOb]
        else:
            l = [self.wxOb, str(self.countMissing)]
        if includeDate:
            l.insert(0, self.date)
        return l

    def _createHeader(self, p):
        '''
        Creates the header needed when exporting to a text file
        '''
        pAndU = self.acis.supportedParameters[p[0:p.find('_')]]['label'] + p[p.find('_'):]
        if self.normal:
            return [pAndU]
        else:
            return [pAndU, pAndU +'_countMissing']


if __name__=='__main__':

    #Daily data
    data = ['2012-02-01',u'32.0', u' ', u'U']
    wx = DailyWxOb(data)
    print wx
    print wx._createHeader('mint')

    #Monthly data
    data = [u'2012-01', u'22.60', 0]
    dmonth = MonthlyWxOb(data)
    print dmonth
    print dmonth.toList()
    print dmonth._createHeader('mint_mly')

    #Monthly normal data
    data = [u'2012-01', u'22.60']
    dmonth = MonthlyWxOb(data, isNormal = True)
    print dmonth
    print dmonth.toList()
    print dmonth._createHeader('mint_mly_normal')



