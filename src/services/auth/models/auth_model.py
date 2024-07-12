from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SignInRequestDTO:
    phone_number: str
    otp: Optional[str] = None
    entry_point: str = '/'
    bypass_otp: bool = False
    email: Optional[str] = None
    password: Optional[str] = None


@dataclass
class MagicLinkResponseDTO:
    message: str
    admin_sign_in_required: bool = False
    magic_link: str = ''


@dataclass
class SignInResponseDTO:
    message: str
    role: List[str]
    user_id: str
    org_id: str
    redirect_url: str
    token: Optional[str] = None
