from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tushare-mcp")

def main() -> None:
    mcp.run()
