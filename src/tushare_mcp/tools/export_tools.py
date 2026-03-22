from __future__ import annotations

import os
import time
import traceback
from typing import Optional

import pandas as pd
import tushare as ts
from mcp.server.fastmcp import FastMCP


def register_export_tools(mcp: FastMCP, pro) -> None:
    @mcp.tool()
    def export_to_file(api_name: str, params: Optional[dict] = None, file_format: str = "excel") -> str:
        """
        Export tushare query result to ~/Documents/MyTushareData as Excel or CSV.

        Pure-text return (ASCII only). No emoji/special symbols.
        """
        params = params or {}

        try:
            home = os.path.expanduser("~")
            docs_path = os.path.join(home, "Documents", "MyTushareData")
            os.makedirs(docs_path, exist_ok=True)

            date_stamp = time.strftime("%Y%m%d")
            fmt = (file_format or "excel").lower().strip()
            ext = "xlsx" if fmt == "excel" else "csv"

            code_segment = ""
            raw_ts = params.get("ts_code") if isinstance(params, dict) else None
            if raw_ts:
                if isinstance(raw_ts, list):
                    codes = raw_ts
                else:
                    codes = [c.strip() for c in str(raw_ts).split(",") if c.strip()]
                if len(codes) == 1:
                    code_segment = "_" + codes[0].replace(".", "_")

            file_name = f"{api_name}{code_segment}_{date_stamp}.{ext}"
            full_path = os.path.abspath(os.path.join(docs_path, file_name))

            if api_name == "pro_bar":
                df = ts.pro_bar(pro_api=pro, **params)
            else:
                api_func = getattr(pro, api_name)
                df = api_func(**params)

            if df is None or (isinstance(df, pd.DataFrame) and df.empty):
                return "[ERROR] Export aborted: no data returned (check permission/params)."

            if fmt == "excel":
                df.to_excel(full_path, index=False)
            else:
                df.to_csv(full_path, index=False, encoding="utf-8-sig")

            return (
                "[OK] Export success.\n"
                f"file_name: {file_name}\n"
                f"full_path: {full_path}\n"
                f"rows: {len(df)}"
            )

        except Exception as e:
            tb = traceback.format_exc()
            return "[ERROR] Export failed: " + str(e) + "\n" + tb
