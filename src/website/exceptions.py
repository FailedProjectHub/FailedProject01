class BaseException(Exception):

    def __init__(self, why):
        self.reason = why

    def __str__(self, reason):
        return self.reason


class Unanuthorized(BaseException):
    status_code = 403
