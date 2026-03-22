from __future__ import annotations

import traceback

import pandas as pd
import tushare as ts
from mcp.server.fastmcp import FastMCP


def register_bar_tools(mcp: FastMCP, pro) -> None:
    @mcp.tool()
    def fetch_stock_bar(
        ts_code: str,
        start_date: str,
        end_date: str,
        asset: str = "E",
        adj: str = "qfq",
    ) -> str:
        """
        Fetch adjusted k-line data via ts.pro_bar.

        :param adj: None 未复权 / qfq 前复权 / hfq 后复权
        :return: CSV text with [REAL_DATA_FROM_TUSHARE_API] prefix
        """
        try:
            df = ts.pro_bar(
                pro_api=pro,
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date,
                asset=asset,
                adj=adj,
            )
            if df is None or (isinstance(df, pd.DataFrame) and df.empty):
                return "No bar data returned."

            if len(df) > 100:
                return (
                    "[REAL_DATA_FROM_TUSHARE_API]\n"
                    + df.head(100).to_csv(index=False)
                    + "\n... (truncated to first 100 rows)"
                )

            return "[REAL_DATA_FROM_TUSHARE_API]\n" + df.to_csv(index=False)

        except Exception as e:
            tb = traceback.format_exc()
            return "Bar fetch failed: " + str(e) + "\n" + tb
