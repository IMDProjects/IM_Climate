from datetime import date


class RequestMetadata(object):
    def __init__(self, queryParameters, **kwargs):
        self.queryParameters = queryParameters
        for k in kwargs.items():
            self.__dict__[k[0]]=k[1]

        self.dateRequested = date.today().isoformat()

if __name__ == '__main__':
    queryParameters = {'elk':'moose'}
    rm = RequestMetadata(queryParameters, info='moreInfo')
    print rm.info