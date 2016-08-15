missingValue = 'NA'
from ACIS import ACIS

class Common(object):
    @property
    def supportedParameters(self):
        acis = ACIS()
        return acis.supportedParameters

if __name__=='__main__':
    print missingValue
    c = Common()
    print c.supportedParameters
