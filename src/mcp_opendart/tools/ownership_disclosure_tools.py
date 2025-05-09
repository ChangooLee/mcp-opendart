import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")

@mcp.tool(
    name="get_major_holder_changes",
    description="5% 이상 보유 주주의 지분 변동을 통한 경영권 위협 및 적대적 인수 가능성 조기 분석",
    tags={"대량보유", "지분변동", "경영권위협", "적대적인수"}
)
def get_major_holder_changes(
    corp_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    대량보유 상황보고 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        start_date (Optional[str]): 검색시작일 (예: 20250101)
        end_date (Optional[str]): 검색종료일 (예: 20251231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019021
    """
    result = with_context(ctx, "get_major_holder_changes", lambda context: context.ds004.get_major_holder_changes(
        corp_code=corp_code,
        start_date=start_date,
        end_date=end_date
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_executive_trading",
    description="임원 및 주요주주의 주식 거래를 통한 내부자 거래 의혹 및 경영진 신호 분석",
    tags={"내부자거래", "임원주주", "지분변동", "경영진신호"}
)
def get_executive_trading(
    corp_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    임원ㆍ주요주주 소유보고 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        start_date (Optional[str]): 검색시작일 (예: 20250101)
        end_date (Optional[str]): 검색종료일 (예: 20251231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019022
    """
    result = with_context(ctx, "get_executive_trading", lambda context: context.ds004.get_executive_trading(
        corp_code=corp_code,
        start_date=start_date,
        end_date=end_date
    ))
    return TextContent(type="text", text=str(result))
