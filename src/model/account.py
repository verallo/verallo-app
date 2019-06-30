from attr import dataclass


@dataclass(frozen=True)
class AccountResponsePayload:
    update_timestamp: str
    account_id: str
    account_type: str
    display_name: str
    currency: str
    account_number: dict
    provider: dict