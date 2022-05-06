from dataclasses import dataclass


@dataclass(frozen=True)
class AccountData:
    pk: str | None = None
    username: str | None = None
