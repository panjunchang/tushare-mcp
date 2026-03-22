from __future__ import annotations

from typing import Optional, Dict

import pandas as pd
from mcp.server.fastmcp import FastMCP

# 先放最小子集，确认流程跑通后你再把完整 SUPPORTED_TOOLS 全部粘进来
SUPPORTED_TOOLS: Dict[str, str] = {
    "stock_basic": "获取基础信息数据，包括股票代码、名称、上市日期、退市日期等(ID:25)",
    "trade_cal": "获取各大交易所交易日历数据(ID:26)",
    "daily": "获取股票行情数据(ID:27)",
    "pro_bar": "获取复权行情(ID:109,146)",
    "fina_indicator": "获取上市公司财务指标数据(ID:79)",
}


def register_generic_tools(mcp: FastMCP, pro) -> None:
    @mcp.tool()
    def fetch_tushare_data(api_name: str, params: Optional[dict] = None) -> str:
        """
        通用 Tushare 数据获取工具。

        :param api_name: 接口名称 (例如 'trade_cal', 'daily', 'stock_basic')
        :param params: 字典格式的参数 (例如 {"exchange": "SSE", "start_date": "20230101"})
        :return: CSV 文本（带 [REAL_DATA_FROM_TUSHARE_API] 前缀）
        """
        if params is None:
            params = {}

        try:
            api_func = getattr(pro, api_name)
            df = api_func(**params)

            if df is None or (isinstance(df, pd.DataFrame) and df.empty):
                return "No data returned. Please check parameters or permissions."

            return "[REAL_DATA_FROM_TUSHARE_API]\n" + df.to_csv(index=False)

        except AttributeError:
            return f"API '{api_name}' is not available on current pro client."
        except Exception as e:
            return f"Fetch failed: {str(e)}"

    @mcp.tool()
    def list_available_interfaces() -> str:
        """查询目前 MCP 支持的所有 Tushare 接口列表"""
        lines = [f"- {name}: {desc}" for name, desc in SUPPORTED_TOOLS.items()]
        return "Supported interfaces:\n" + "\n".join(lines)
