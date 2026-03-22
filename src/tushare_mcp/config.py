from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
    tushare_token: str

def load_settings() -> Settings:
    load_dotenv()
    token = os.getenv("TUSHARE_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Missing TUSHARE_TOKEN. Set env var or put it in .env.")
    return Settings(tushare_token=token)
