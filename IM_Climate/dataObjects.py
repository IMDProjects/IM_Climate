import json
import dateutil.parser


class dataObjects(dict):

    '''
    Base class for all dictionary typed data objects
    '''
    def __init__(self,*args,**kwargs):
        super(dataObjects,self).__init__(*args,**kwargs)
        if not self.get('meta', None):  #set up metadata for standard structure used by ACIS
            self['meta'] = [{}]

    def toJSON(self):
        return json.dumps(self)


    def _addStandardMetadataElements(self):
        self['meta']

    @property
    def metadata(self):
        return self['meta'][0]

    def _addMetadata(self, **kwarg):
        for i in kwarg.items():
            self['meta'][0][i[0]] = i[1]

    def _parseDate(self, date):
        if date:
            return dateutil.parser.parse(str(date)).date()



if __name__=='__main__':
    d = dataObjects()
    d._addMetadata(elk = 5)
    print d.metadata