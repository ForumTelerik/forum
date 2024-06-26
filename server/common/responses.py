from fastapi import Response, HTTPException


class SC:
    Created = 201
    Accepted = 202
    NoContent = 204

    BadRequest = 400
    Unauthorized = 401
    PaymentRequired = 402
    Forbidden = 403
    NotFound = 404


class HTTPBadRequest(HTTPException):
    def __init__(self, detail=''):
        super().__init__(status_code=SC.BadRequest, detail=detail)


class HTTPForbidden(HTTPException):
    def __init__(self, detail=''):
        super().__init__(status_code=SC.Forbidden, detail=detail)


class HTTPUnauthorized(HTTPException):
    def __init__(self, detail=''):
        super().__init__(status_code=SC.Unauthorized, detail=detail)


class HTTPNotFound(HTTPException):
    def __init__(self, detail=''):
        super().__init__(status_code=SC.NotFound, detail=detail)


class BadRequest(Response):
    def __init__(self, content=''):
        super().__init__(status_code=400, content=content)


class NotFound(Response):
    def __init__(self, content=''):
        super().__init__(status_code=404, content=content)


class Unauthorized(Response):
    def __init__(self, content=''):
        super().__init__(status_code=401, content=content)


class Forbidden(Response):

    def __init__(self, content=''):
        super().__init__(status_code=403, content=content)


class NoContent(Response):
    def __init__(self):
        super().__init__(status_code=204)


class Created(Response):
    def __init__(self):
        super().__init__(status_code=201)


class InternalServerError(Response):
    def __init__(self):
        super().__init__(status_code=500)
