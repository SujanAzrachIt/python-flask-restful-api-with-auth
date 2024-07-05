from dataclasses import dataclass
from typing import Optional, List


@dataclass
class SignInResponseDTO:
    message: str
    role: List[str]
    user_id: str
    org_id: str
    redirect_url: str
    token: Optional[str] = None
