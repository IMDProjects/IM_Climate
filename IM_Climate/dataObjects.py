import json
import dateutil.parser


class dataObjects(dict):

    '''
    Base class for all dictionary typed data objects
    '''
    def __init__(self,*args,**kwargs):
        super(dataObjects,self).__init__(*args,**kwargs)
        if not self.get('meta', None):
            self['meta'] = {}

    def toJSON(self):
        return json.dumps(self)



    def _addStandardMetadataElements(self):
        self['meta']

    @property
    def metadata(self):
        return [k for k in self['meta'].items()]

    def addMetadata(self, **kwarg):
        for i in kwarg.items():
            self['meta'][i[0]] = i[1]

    def _parseDate(self, date):
        if date:
            return dateutil.parser.parse(str(date)).date()



if __name__=='__main__':
    d = dataObjects()
    d.addMetadata(elk = 5)
    print d.metadata