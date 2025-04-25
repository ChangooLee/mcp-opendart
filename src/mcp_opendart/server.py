
import logging
import sys
import asyncio
from starlette.requests import Request
from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated, Any, Literal, Optional

from fastmcp import FastMCP
from mcp.types import TextContent
from mcp.server.session import ServerSession
from pydantic import Field

from .config import OpenDartConfig, MCPConfig
from .apis.client import OpenDartClient
from .apis import ds001, ds002, ds003, ds004, ds005, ds006
from typing import AsyncIterator

# 로거 설정
mcp_config = MCPConfig.from_env()
level_name = mcp_config.log_level.upper()
level = getattr(logging, level_name, logging.INFO)
logger = logging.getLogger("mcp-opendart")

# 로깅 설정: 출력 형식과 대상 스트림을 지정
logging.basicConfig(
    level=level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)


@dataclass
class OpenDartContext(ServerSession):
    client: Optional[OpenDartClient] = None
    ds001: Any = None
    ds002: Any = None
    ds003: Any = None
    ds004: Any = None
    ds005: Any = None
    ds006: Any = None


    def __post_init__(self):
        # client가 None이면 기본 클라이언트 생성
        if self.client is None:
            from .config import OpenDartConfig, MCPConfig
            config = OpenDartConfig.from_env()
            self.client = OpenDartClient(config=config)
            
        # API 모듈이 None이면 초기화 (지연 임포트 사용)
        if self.ds001 is None:
            from .apis import ds001
            self.ds001 = ds001.DisclosureAPI(self.client)
        if self.ds002 is None:
            from .apis import ds002
            self.ds002 = ds002.PeriodicReportAPI(self.client)
        if self.ds003 is None:
            from .apis import ds003
            self.ds003 = ds003.FinancialInfoAPI(self.client)
        if self.ds004 is None:
            from .apis import ds004
            self.ds004 = ds004.OwnershipDisclosureAPI(self.client)
        if self.ds005 is None:
            from .apis import ds005
            self.ds005 = ds005.MajorReportAPI(self.client)
        if self.ds006 is None:
            from .apis import ds006
            self.ds006 = ds006.SecuritiesFilingAPI(self.client)
        
    async def __aenter__(self):
        logger.info("🔁 OpenDartContext entered (Claude requested tool execution)")
        return self

    async def __aexit__(self, *args):
        logger.info("🔁 OpenDartContext exited")


opendart_client = OpenDartClient(config=OpenDartConfig.from_env())
# 1. OpenDartContext 정의
opendart_context = OpenDartContext(
    client=opendart_client,
    ds001=ds001.DisclosureAPI(opendart_client),
    ds002=ds002.PeriodicReportAPI(opendart_client),
    ds003=ds003.FinancialInfoAPI(opendart_client),
    ds004=ds004.OwnershipDisclosureAPI(opendart_client),
    ds005=ds005.MajorReportAPI(opendart_client),
    ds006=ds006.SecuritiesFilingAPI(opendart_client),
)

# 2. fallback용 ctx 설정은 이후에
ctx = opendart_context        

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

import importlib
for module_name in [
    "disclosure_tools", "financial_info_tools", "major_report_tools",
    "ownership_disclosure_tools", "periodic_report_tools", "securities_filing_tools"
]:
    importlib.import_module(f"mcp_opendart.tools.{module_name}")

def main():
    logger.info("✅ Initializing OpenDART FastMCP server...")
    
    transport = mcp_config.transport
    port = mcp_config.port

    if transport == "sse":
        asyncio.run(run_server(transport="sse", port=port))
    else:
        mcp.run()

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
