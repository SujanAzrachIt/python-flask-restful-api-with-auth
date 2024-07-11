import enum


class Role(enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    ORG_ADMIN = "org_admin"
    USER = "user"
