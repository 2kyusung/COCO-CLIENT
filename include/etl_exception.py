class RDBConnectErrorException(Exception): pass

class RDBMSInsertException(Exception):
    def __init__(self, err_msg=""):
        super().__init__(err_msg)

class RDBMSInsertDataConvertException(Exception):
    def __init__(self, err_msg=""):
        super().__init__(err_msg)

class ElasticSearchInsertException(Exception): pass