from flask_restful.reqparse import request

from src.models.org.model_org import OrgModel
from src.resources.org.org_base import OrgBase, org_marshaller


class OrgPlural(OrgBase):
    @classmethod
    def get(cls):
        orgs = OrgModel.find_all()
        return org_marshaller(orgs, request.args)
