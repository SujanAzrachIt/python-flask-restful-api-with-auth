from flask import Blueprint
from flask_restful import Api

from src.resources.auth.auth_singular import GenerateMagicLinkSingular, SignInSingular, RequestOTPSingular
from src.resources.org.org_plural import OrgPlural
from src.resources.org.org_singular import OrgSingular
from src.resources.qr_code.qr_code_singular import QrCodeSingular, GenerateQrCodeSingular
from src.resources.role.role_singular import RoleSingular
from src.resources.user.user_singular import UserSingular

bp_org = Blueprint('orgs', __name__, url_prefix='/api/orgs')
api_org = Api(bp_org)
api_org.add_resource(OrgPlural, '')
api_org.add_resource(OrgSingular, '/<string:id>')

bp_qrcode = Blueprint('qrcodes', __name__, url_prefix='/api/qrcodes')
api_qrcode = Api(bp_qrcode)
api_qrcode.add_resource(QrCodeSingular, '/<string:id>')
api_qrcode.add_resource(GenerateQrCodeSingular, '/generate/<string:id>')

bp_role = Blueprint('roles', __name__, url_prefix='/api/roles')
api_role = Api(bp_role)
api_role.add_resource(RoleSingular, '/<string:id>')

bp_user = Blueprint('users', __name__, url_prefix='/api/users')
api_user = Api(bp_user)
api_user.add_resource(UserSingular, '/<string:id>')

bp_auth = Blueprint('auth', __name__, url_prefix='/api/auth')
api_auth = Api(bp_auth)
api_auth.add_resource(GenerateMagicLinkSingular, '/generate-magic-link')
api_auth.add_resource(SignInSingular, '/sign-in')
api_auth.add_resource(RequestOTPSingular, '/request-otp')