import json
import logging
import os
from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated, Any, Literal

from fastmcp import FastMCP
from mcp.types import TextContent
from mcp.server.session import ServerSession
from pydantic import Field

from .config import OpenDartConfig, MCPConfig
from .apis.client import OpenDartClient
from .apis import ds001, ds002, ds003, ds004, ds005, ds006
from typing import AsyncIterator

# 로거 설정
logger = logging.getLogger("mcp-opendart")
@dataclass
class OpenDartContext(ServerSession):
    client: OpenDartClient
    ds001: ds001.DisclosureAPI
    ds002: ds002.PeriodicReportAPI
    ds003: ds003.FinancialInfoAPI
    ds004: ds004.OwnershipDisclosureAPI
    ds005: ds005.MajorReportAPI
    ds006: ds006.SecuritiesFilingAPI


@asynccontextmanager
async def opendart_lifespan(app: FastMCP) -> AsyncIterator[OpenDartContext]:
    """Lifespan manager for the OpenDART FastMCP server.

    Creates and manages the OpenDartClient instance and API modules.
    """
    logger.info("Initializing OpenDART FastMCP server...")

    # OpenDART 설정 로드
    try:
        opendart_config = OpenDartConfig.from_env()
        mcp_config = MCPConfig.from_env()

        logger.info(f"Server Name: {mcp_config.server_name}")
        logger.info(f"Host: {mcp_config.host}")
        logger.info(f"Port: {mcp_config.port}")
        logger.info(f"Log Level: {mcp_config.log_level}")
        
        # OpenDART API 클라이언트 초기화
        client = OpenDartClient(config=opendart_config)
        
        # API 모듈 초기화
        ctx = OpenDartContext(
            client=client,
            ds001=ds001.DisclosureAPI(client),
            ds002=ds002.PeriodicReportAPI(client),
            ds003=ds003.FinancialInfoAPI(client),
            ds004=ds004.OwnershipDisclosureAPI(client),
            ds005=ds005.MajorReportAPI(client),
            ds006=ds006.SecuritiesFilingAPI(client)
        )
        
        logger.info("OpenDART client and API modules initialized successfully.")
        yield ctx
        
    except Exception as e:
        logger.error(f"Failed to initialize OpenDART client: {e}", exc_info=True)
        raise
    finally:
        logger.info("Shutting down OpenDART FastMCP server...")

# Create the main FastMCP instance
mcp = FastMCP(
    "OpenDART MCP",
    description="OpenDART tools and resources for interacting with DART system",
    lifespan=opendart_lifespan,
)

# Register tool modules (ensure all @mcp.tool decorators run)
import importlib
for module_name in ["disclosure_tools", "financial_info_tools", "major_report_tools",
                    "ownership_disclosure_tools", "periodic_report_tools", "securities_filing_tools"]:
    importlib.import_module(f"mcp_opendart.tools.{module_name}")

async def run_server(
    transport: Literal["stdio", "sse"] = "stdio",
    port: int = 8000,
) -> None:
    """Run the MCP OpenDART server.

    Args:
        transport: The transport to use. One of "stdio" or "sse".
        port: The port to use for SSE transport.
    """
    if transport == "stdio":
        # Use the built-in method for stdio transport
        await mcp.run_stdio_async()
    elif transport == "sse":
        # Use FastMCP's built-in SSE runner
        logger.info(f"Starting server with SSE transport on http://0.0.0.0:{port}")
        await mcp.run_sse_async(host="0.0.0.0", port=port)  # noqa: S104

# Tool implementations will be added here
