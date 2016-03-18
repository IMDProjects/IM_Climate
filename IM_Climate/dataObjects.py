import json
from datetime import date


class dataObjects(object):
    def __init__(self,*args,**kwargs):
        super(dataObjects,self).__init__(*args,**kwargs)
    def toJSON(self):
        return json.dumps(self)
    def getCurrentYear(self):
        return date.today().year

if __name__=='__main__':
    d = dataObjects()
    print d.getCurrentYear()