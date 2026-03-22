from __future__ import annotations

from datetime import datetime

from mcp.server.fastmcp import FastMCP


def register_time_tools(mcp: FastMCP) -> None:
    @mcp.tool()
    def get_current_market_time() -> str:
        """
        Get current system time for grounding date calculations.
        Format: YYYYMMDD, HH:MM:SS
        """
        now = datetime.now()
        return now.strftime("%Y%m%d, %H:%M:%S")
