from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import tushare as ts

@dataclass
class TushareClient:
    token: str

    def __post_init__(self) -> None:
        ts.set_token(self.token)
        self.pro = ts.pro_api(self.token)

    def call(self, api_name: str, **kwargs: Any):
        fn = getattr(self.pro, api_name, None)
        if fn is None:
            raise ValueError(f"Unknown tushare api: {api_name}")
        return fn(**kwargs)
