from dataclasses import dataclass
from typing import Optional


@dataclass
class SignInRequestDTO:
    phone_number: str
    otp: Optional[str] = None
    entry_point: str = '/'
    bypass_otp: bool = False
    email: Optional[str] = None
    password: Optional[str] = None