class XploreBaseException(BaseException):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        if self.msg is not None:
            return self.msg
        else:
            return "An exception in xplore occurred."


class ValidationException(XploreBaseException):
    pass
