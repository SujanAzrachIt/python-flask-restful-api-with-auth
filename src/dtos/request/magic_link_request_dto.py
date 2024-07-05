from dataclasses import dataclass


@dataclass
class MagicLinkRequestDTO:
    phone_number: str
    magic_link_entry_point: str = '/'