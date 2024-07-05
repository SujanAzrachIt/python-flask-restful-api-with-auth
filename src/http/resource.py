from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.exceptions import BadRequest

from .exception.exception import *


class HttpResource(Resource):
    def dispatch_request(self, *args, **kwargs):
        try:
            return super().dispatch_request(*args, **kwargs)
        except (IntegrityError, OperationalError) as e:
            abort(400, message=str(e.orig))
        except (ValueError, BadRequest, BadDataException) as e:
            abort(400, message=str(e))
        except UnauthorizedException as e:
            abort(401, message=str(e))
        except ForbiddenException as e:
            abort(403, message=str(e))
        except NotFoundException as e:
            abort(404, message=str(e))
        except PreConditionException as e:
            abort(428, message=str(e))
        except InternalServerErrorException as e:
            abort(500, message=str(e))
        except NotImplementedException as e:
            abort(501, message=str(e))
        except GatewayTimeoutException as e:
            abort(503, message=str(e))
        except Exception as e:
            abort(500, message=str(e))
