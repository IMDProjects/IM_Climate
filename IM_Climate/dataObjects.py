import json

class dataObjects(object):
    def __init__(self):
        super(dataObjects,self).__init__(*args,**kwargs)
    def toJSON(self):
        return json.dumps(self)