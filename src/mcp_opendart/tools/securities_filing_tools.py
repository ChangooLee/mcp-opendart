import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")

@mcp.tool(
    name="get_equity",
    description="증권신고서(지분증권) 내에 요약 정보를 제공합니다. 반환값에는 발행종류, 발행주식수, 발행가액, 모집방법 등의 항목이 포함됩니다.",
    tags={"지분증권", "증권신고서", "지분증권", "증권신고서"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

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
    description="증권신고서(채무증권) 내에 요약 정보를 제공합니다. 반환값에는 채권종류, 발행총액, 이자율, 만기일, 상환방법 등의 항목이 포함됩니다.",
    tags={"채무증권", "증권신고서", "채무증권", "증권신고서"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

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
    description="증권신고서(증권예탁증권) 내에 요약 정보를 제공합니다. 반환값에는 예탁증권 종류, 발행수량, 발행가액, 외화표시 여부 등의 항목이 포함됩니다.",
    tags={"증권예탁증권", "증권신고서", "증권예탁증권", "증권신고서"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

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
    description="증권신고서(합병) 내에 요약 정보를 제공합니다. 반환값에는 합병대상회사, 합병비율, 합병기일, 합병조건 등의 항목이 포함됩니다.",
    tags={"합병", "증권신고서", "합병", "증권신고서"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

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
    description="증권신고서(주식의포괄적교환·이전) 내에 요약 정보를 제공합니다. 반환값에는 교환대상회사, 교환비율, 교환기일, 교환조건 등의 항목이 포함됩니다.",
    tags={"주식의포괄적교환·이전", "증권신고서", "주식의포괄적교환·이전", "증권신고서"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

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
    description="증권신고서(분할) 내에 요약 정보를 제공합니다. 반환값에는 분할방식, 분할회사명, 분할비율, 분할기일 등의 항목이 포함됩니다.",
    tags={"분할", "증권신고서", "분할", "증권신고서"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020059
    """
    result = with_context(ctx, "get_division_report", lambda context: context.ds006.get_division_report(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))
