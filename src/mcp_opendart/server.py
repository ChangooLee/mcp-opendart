from mcp.server.fastmcp import FastMCP, Context
from opendart_mcp.apis.client import OpenDartClient
from opendart_mcp.apis import ds001, ds002, ds003, ds004, ds005, ds006  # API modules

# 1) MCP 서버 초기화
mcp = FastMCP("OpenDART")

# 2) lifespan 컨텍스트 정의 (OpenDartClient 및 API 클래스 초기화)
from dataclasses import dataclass
from contextlib import asynccontextmanager

@dataclass
class AppContext:
    client: OpenDartClient
    ds001: ds001.DisclosureAPI
    ds002: ds002.PeriodicReportAPI
    ds003: ds003.FinancialInfoAPI
    ds004: ds004.OwnershipDisclosureAPI
    ds005: ds005.MajorReportAPI
    ds006: ds006.SecuritiesFilingAPI

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    # API Key는 환경변수 등에서 로드
    api_key = os.getenv("DART_API_KEY")
    client = OpenDartClient(api_key)
    # OpenDART API 클래스 인스턴스 생성
    ctx = AppContext(
        client=client,
        ds001 = ds001.DisclosureAPI(client),
        ds002 = ds002.PeriodicReportAPI(client),
        ds003 = ds003.FinancialInfoAPI(client),
        ds004 = ds004.OwnershipDisclosureAPI(client),
        ds005 = ds005.MajorReportAPI(client),
        ds006 = ds006.SecuritiesFilingAPI(client),
    )
    yield ctx

mcp = FastMCP("OpenDART", lifespan=app_lifespan)
