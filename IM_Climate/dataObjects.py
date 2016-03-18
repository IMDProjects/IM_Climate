import json
import dateutil.parser
from datetime import date


class dataObjects(dict):

    '''
    Base class for all dictionary typed data objects
    '''
    def __init__(self,*args,**kwargs):
        super(dataObjects,self).__init__(*args,**kwargs)

    def toJSON(self):
        return json.dumps(self)

    def _addStandardMetadataElements(self):
        self._addMetadata(dateCreated = date.today().isoformat())

    @property
    def metadata(self):
        return self['meta']

    @property
    def dateCreated(self):
        '''returns the date the object was created
        '''
        return self['meta']

    def _addMetadata(self, **kwarg):
        for i in kwarg.items():
            self['meta'][i[0]] = i[1]

    def _parseDate(self, date):
        if date:
            return dateutil.parser.parse(str(date)).date()



if __name__=='__main__':
    stuff = {'meta':{},'data':[]}
    d = dataObjects(stuff)
    d._addStandardMetadataElements()
    d._addMetadata(elk = 5)
    print d.metadata
    print d.dateCreated