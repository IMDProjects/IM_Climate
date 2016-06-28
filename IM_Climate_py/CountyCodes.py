import urllib2, urllib

class CountyCodes(object):
    '''
    IN DEV - INCOMPLETE
    '''
    def __init__(self):
        super(CountyCodes,self).__init__()
        self.pyVersion = 2
    def get(self, state = None):
        fipCode = []
        if self.pyVersion == 2:
            data = urllib2.urlopen('http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt')
        elif self.pyVersion == 3:
            data = urllib.request.urlopen('http://www2.census.gov/geo/docs/reference/codes/files/national_county.txt')
        for line in data.readlines():
            line = str(line).split(',')
            if state:
                if line[0] == state:
                    fipCode.append(line[3] + ', ' + line[0] + ' : ' + line[1] + line[2])
            else:
                fipCode.append(line[0] + ',' + line[3] + ' : ' + line[1] + line[2])
        return fipCode

if __name__ == '__main__':
    cc = CountyCodes()
    print (cc.get('CO'))