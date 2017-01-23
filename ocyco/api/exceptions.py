class OcycoException(Exception):
    def __init__(self, message, status_code, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or())
        rv['error'] = self.message
        return rv


class ParameterInvalidException(OcycoException):
    status_code = 400

    def __init__(self, message, payload=None):
        OcycoException.__init__(self, message, self.status_code, payload=payload)


class ParameterMissingException(OcycoException):
    status_code = 400

    def __init__(self, message, payload=None):
        OcycoException.__init__(self, message, self.status_code, payload=payload)


class NotFoundException(OcycoException):
    status_code = 404

    def __init__(self, message, payload=None):
        OcycoException.__init__(self, message, self.status_code, payload=payload)


class ConflictExistingObjectException(OcycoException):
    status_code = 409

    def __init__(self, message, payload=None):
        OcycoException.__init__(self, message, self.status_code, payload=payload)


class MultipleMatchesException(OcycoException):
    status_code = 500

    def __init__(self, message, payload=None):
        OcycoException.__init__(self, message, self.status_code, payload=payload)


class PhotonException(OcycoException):
    status_code = 500

    def __init__(self, message, payload=None):
        OcycoException.__init__(self, message, self.status_code, payload=payload)