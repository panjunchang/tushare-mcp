from __future__ import annotations

import tushare as ts
from mcp.server.fastmcp import FastMCP

from .config import load_settings

mcp = FastMCP("Tushare-Financial-Data")


def _create_pro():
    settings = load_settings()
    ts.set_token(settings.tushare_token)
    return ts.pro_api(settings.tushare_token)


def main() -> None:
    pro = _create_pro()

    # 这里后面会注册你拆分后的 tools：
    from .tools.generic import register_generic_tools
    register_generic_tools(mcp=mcp, pro=pro)
    #
    # from .tools.time_tools import register_time_tools
    $ register_time_tools(mcp=mcp)
    #
    from .tools.export_tools import register_export_tools
    register_export_tools(mcp=mcp, pro=pro)
    #
    from .tools.bar_tools import register_bar_tools
    register_bar_tools(mcp=mcp, pro=pro)

    mcp.run()
