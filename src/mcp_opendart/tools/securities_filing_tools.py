import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")

@mcp.tool(
    name="get_equity",
    description="신주 발행 및 지분증권 매출 내역을 통한 지배구조 변동 및 자금운용 리스크 분석",
    tags={"지분증권", "신주발행", "자금조달", "지배구조", "증권신고서"}
)
def get_equity(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    지분증권 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020054
    """
    result = with_context(ctx, "get_equity", lambda context: context.ds006.get_equity(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_debt",
    description="채무증권 발행 조건 및 구조를 통한 부채 리스크 및 차환위험 분석",
    tags={"채무증권", "회사채", "자금조달", "재무리스크", "증권신고서"}
)
def get_debt(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    채무증권 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020055
    """
    result = with_context(ctx, "get_debt", lambda context: context.ds006.get_debt(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_depository_receipt",
    description="예탁증권 발행을 통한 해외자금조달 및 외화 리스크 분석",
    tags={"예탁증권", "외화조달", "환율리스크", "글로벌리스크", "증권신고서"}
)
def get_depository_receipt(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    증권예탁증권 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020056
    """
    result = with_context(ctx, "get_depository_receipt", lambda context: context.ds006.get_depository_receipt(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_merger_report",
    description="합병 구조 및 조건을 통한 경영권 변동, 소수주주 보호, 합병 무효 리스크 분석",
    tags={"합병", "경영권", "주주보호", "지배구조", "증권신고서"}
)
def get_merger_report(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    합병 증권신고서 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020057
    """
    result = with_context(ctx, "get_merger_report", lambda context: context.ds006.get_merger_report(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_exchange_report",
    description="주식교환·이전 조건을 통한 지배구조 재편 및 소수주주 보호 리스크 분석",
    tags={"주식교환", "지배구조", "주주보호", "소수주주", "증권신고서"}
)
def get_stock_exchange_report(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주식의포괄적교환·이전 증권신고서 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020058
    """
    result = with_context(ctx, "get_stock_exchange_report", lambda context: context.ds006.get_stock_exchange_report(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_division_report",
    description="회사분할 조건을 통한 신설법인 리스크 및 주주가치 훼손 가능성 분석",
    tags={"분할", "지배구조", "주주보호", "사업재편", "증권신고서"}
)
def get_division_report(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    분할 증권신고서 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020059
    """
    result = with_context(ctx, "get_division_report", lambda context: context.ds006.get_division_report(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))
