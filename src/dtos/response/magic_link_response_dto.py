from dataclasses import dataclass


@dataclass
class MagicLinkResponseDTO:
    message: str
    magic_link: str