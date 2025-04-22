import json
import logging
import os
from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from typing import Annotated, Any

from fastmcp import FastMCP, Context
from mcp.types import TextContent
from pydantic import Field

from .config import OpenDartConfig, MCPConfig
from .apis.client import OpenDartClient
from .apis import ds001, ds002, ds003, ds004, ds005, ds006

# 로거 설정
logger = logging.getLogger("mcp-opendart")

@asynccontextmanager
async def opendart_lifespan(app: FastMCP) -> AsyncGenerator[dict[str, Any], None]:
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
        ctx = {
            "client": client,
            "ds001": ds001.DisclosureAPI(client),
            "ds002": ds002.PeriodicReportAPI(client),
            "ds003": ds003.FinancialInfoAPI(client),
            "ds004": ds004.OwnershipDisclosureAPI(client),
            "ds005": ds005.MajorReportAPI(client),
            "ds006": ds006.SecuritiesFilingAPI(client),
        }
        
        logger.info("OpenDART client and API modules initialized successfully.")
        yield ctx
        
    except Exception as e:
        logger.error(f"Failed to initialize OpenDART client: {e}", exc_info=True)
        yield {}
    finally:
        logger.info("Shutting down OpenDART FastMCP server...")

# Create the OpenDART FastMCP instance
mcp = FastMCP(
    "OpenDART",
    description="Tools for interacting with OpenDART API",
    lifespan=opendart_lifespan,
)

# Tool implementations will be added here
