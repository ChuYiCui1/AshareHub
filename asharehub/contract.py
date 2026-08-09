"""Machine-readable AShareHub V2 public contract."""

from __future__ import annotations

import json
from copy import deepcopy
from importlib.resources import files
from typing import Any


def _load_contract() -> dict[str, Any]:
    resource = files("asharehub").joinpath("public_contract.json")
    return json.loads(resource.read_text(encoding="utf-8"))


PUBLIC_CONTRACT = _load_contract()


def get_contract(method: str | None = None) -> dict[str, Any]:
    """Return a defensive copy of the full contract or one SDK method entry."""
    if method is None:
        return deepcopy(PUBLIC_CONTRACT)
    try:
        return deepcopy(PUBLIC_CONTRACT["interfaces"][method])
    except KeyError as error:
        raise KeyError(f"Unknown AShareHub method: {method}") from error


__all__ = ["PUBLIC_CONTRACT", "get_contract"]
