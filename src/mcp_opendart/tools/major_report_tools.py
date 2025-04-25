import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")
@mcp.tool(
    name="get_asset_transfer",
    description="주요사항보고서(자산양수도(기타), 풋백옵션) 내에 주요 정보를 제공합니다. 반환값에는 계약일자, 자산명, 양수/양도 금액, 계약상대방, 풋백옵션 조건 등이 포함됩니다.",
    tags={"주요사항보고서", "자산양수도", "풋백옵션", "주요정보"}
)
def get_asset_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자산양수도(기타), 풋백옵션 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020018
    """
    result = with_context(ctx, "get_asset_transfer", lambda context: context.ds005.get_asset_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_bankruptcy",
    description="주요사항보고서(부도발생) 내에 주요 정보를 제공합니다. 반환값에는 발생일자, 사유, 채권자 정보, 부도금액 등이 포함됩니다.",
    tags={"주요사항보고서", "부도발생", "주요정보", "부도"}
)
def get_bankruptcy(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    부도발생 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020019
    """
    result = with_context(ctx, "get_bankruptcy", lambda context: context.ds005.get_bankruptcy(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_business_suspension",
    description="주요사항보고서(영업정지) 내에 주요 정보를 제공합니다. 반환값에는 정지사유, 정지기간, 정지영업부문, 영향 및 향후대책 등이 포함됩니다.",
    tags={"주요사항보고서", "영업정지", "주요정보", "정지"}
)
def get_business_suspension(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    영업정지 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020020
    """
    result = with_context(ctx, "get_business_suspension", lambda context: context.ds005.get_business_suspension(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_rehabilitation",
    description="주요사항보고서(회생절차 개시신청) 내에 주요 정보를 제공합니다. 반환값에는 신청일자, 신청사유, 법원명, 진행현황 등이 포함됩니다.",
    tags={"주요사항보고서", "회생절차", "주요정보", "회생"}
)
def get_rehabilitation(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회생절차 개시신청 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020021
    """
    result = with_context(ctx, "get_rehabilitation", lambda context: context.ds005.get_rehabilitation(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_dissolution",
    description="주요사항보고서(해산사유 발생) 내에 주요 정보를 제공합니다. 반환값에는 발생일자, 해산사유, 법적근거, 향후 절차 등이 포함됩니다.",
    tags={"주요사항보고서", "해산사유", "주요정보", "해산"}
)
def get_dissolution(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    해산사유 발생 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020022
    """
    result = with_context(ctx, "get_dissolution", lambda context: context.ds005.get_dissolution(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_paid_in_capital_increase",
    description="주요사항보고서(유상증자 결정) 내에 주요 정보를 제공합니다. 반환값에는 발행주식수, 발행가액, 모집방법, 자금사용계획 등이 포함됩니다.",
    tags={"주요사항보고서", "유상증자", "주요정보", "증자"}
)
def get_paid_in_capital_increase(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유상증자 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020023
    """
    result = with_context(ctx, "get_paid_in_capital_increase", lambda context: context.ds005.get_paid_in_capital_increase(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_free_capital_increase",
    description="주요사항보고서(무상증자 결정) 내에 주요 정보를 제공합니다. 반환값에는 신주배정비율, 기준일, 배정기준일, 신주상장예정일 등이 포함됩니다.",
    tags={"주요사항보고서", "무상증자", "주요정보", "증자"}
)
def get_free_capital_increase(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    무상증자 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020024
    """
    result = with_context(ctx, "get_free_capital_increase", lambda context: context.ds005.get_free_capital_increase(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_paid_free_capital_increase",
    description="주요사항보고서(유무상증자 결정) 내에 주요 정보를 제공합니다. 반환값에는 유상/무상 발행주식수, 발행가액, 배정비율, 상장예정일 등이 포함됩니다.",
    tags={"주요사항보고서", "유무상증자", "주요정보", "증자"}
)
def get_paid_free_capital_increase(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유무상증자 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020025
    """
    result = with_context(ctx, "get_paid_free_capital_increase", lambda context: context.ds005.get_paid_free_capital_increase(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_capital_reduction",
    description="주요사항보고서(감자 결정) 내에 주요 정보를 제공합니다. 반환값에는 감자방법, 감자비율, 기준일, 감자사유 등이 포함됩니다.",
    tags={"주요사항보고서", "감자", "주요정보", "감자"}
)
def get_capital_reduction(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    감자 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020026
    """
    result = with_context(ctx, "get_capital_reduction", lambda context: context.ds005.get_capital_reduction(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_creditor_management",
    description="주요사항보고서(채권은행 등의 관리절차 개시) 내에 주요 정보를 제공합니다. 반환값에는 개시일자, 채권은행명, 관리내용, 진행계획 등이 포함됩니다.",
    tags={"주요사항보고서", "채권은행", "주요정보", "채권"}
)
def get_creditor_management(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    채권은행 등의 관리절차 개시 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020027
    """
    result = with_context(ctx, "get_creditor_management", lambda context: context.ds005.get_creditor_management(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_lawsuit",
    description="주요사항보고서(소송 등의 제기) 내에 주요 정보를 제공합니다. 반환값에는 소송제기일, 소송당사자, 청구내용, 소송금액, 소송진행상황 등이 포함됩니다.",
    tags={"주요사항보고서", "소송", "주요정보", "소송"}
)
def get_lawsuit(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    소송 등의 제기 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020028
    """
    result = with_context(ctx, "get_lawsuit", lambda context: context.ds005.get_lawsuit(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_foreign_listing_decision",
    description="주요사항보고서(해외 증권시장 주권등 상장 결정) 내에 주요 정보를 제공합니다. 반환값에는 상장예정시장, 상장예정일, 상장주식수, 외화표시 여부 등이 포함됩니다.",
    tags={"주요사항보고서", "해외 증권시장", "주권등", "상장", "결정"}
)
def get_foreign_listing_decision(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    해외 증권시장 주권등 상장 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020029
    """
    result = with_context(ctx, "get_foreign_listing_decision", lambda context: context.ds005.get_foreign_listing_decision(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_foreign_delisting_decision",
    description="주요사항보고서(해외 증권시장 주권등 상장폐지 결정) 내에 주요 정보를 제공합니다. 반환값에는 상장폐지시장, 상장폐지사유, 상장폐지예정일, 영향 등 주요 항목이 포함됩니다.",
    tags={"주요사항보고서", "해외 증권시장", "주권등", "상장", "결정"}
)
def get_foreign_delisting_decision(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    해외 증권시장 주권등 상장폐지 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020030
    """
    result = with_context(ctx, "get_foreign_delisting_decision", lambda context: context.ds005.get_foreign_delisting_decision(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_foreign_listing",
    description="주요사항보고서(해외 증권시장 주권등 상장) 내에 주요 정보를 제공합니다. 반환값에는 상장시장명, 상장일자, 상장주식수, 발행시장 구분 등이 포함됩니다.",
    tags={"주요사항보고서", "해외 증권시장", "주권등", "상장"}
)
def get_foreign_listing(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    해외 증권시장 주권등 상장 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020031
    """
    result = with_context(ctx, "get_foreign_listing", lambda context: context.ds005.get_foreign_listing(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_foreign_delisting",
    description="주요사항보고서(해외 증권시장 주권등 상장폐지) 내에 주요 정보를 제공합니다. 반환값에는 상장폐지시장, 폐지일자, 폐지사유, 후속조치 등이 포함됩니다.",
    tags={"주요사항보고서", "해외 증권시장", "주권등", "상장", "폐지"}
)
def get_foreign_delisting(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    해외 증권시장 주권등 상장폐지 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020032
    """
    result = with_context(ctx, "get_foreign_delisting", lambda context: context.ds005.get_foreign_delisting(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_convertible_bond",
    description="주요사항보고서(전환사채권 발행결정) 내에 주요 정보를 제공합니다. 반환값에는 발행총액, 전환비율, 전환가액, 전환청구기간 등이 포함됩니다.",
    tags={"주요사항보고서", "전환사채권", "발행결정", "전환"}
)
def get_convertible_bond(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    전환사채권 발행결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020033
    """
    result = with_context(ctx, "get_convertible_bond", lambda context: context.ds005.get_convertible_bond(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_bond_with_warrant",
    description="주요사항보고서(신주인수권부사채권 발행결정) 내에 주요 정보를 제공합니다. 반환값에는 발행총액, 행사비율, 행사기간, 발행조건 등이 포함됩니다.",
    tags={"주요사항보고서", "신주인수권부사채권", "발행결정", "신주"}
)
def get_bond_with_warrant(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    신주인수권부사채권 발행결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020034
    """
    result = with_context(ctx, "get_bond_with_warrant", lambda context: context.ds005.get_bond_with_warrant(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_exchangeable_bond",
    description="주요사항보고서(교환사채권 발행결정) 내에 주요 정보를 제공합니다. 반환값에는 발행총액, 교환대상종목, 교환가액, 교환청구기간 등이 포함됩니다.",
    tags={"주요사항보고서", "교환사채권", "발행결정", "교환"}
)
def get_exchangeable_bond(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    교환사채권 발행결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020035
    """
    result = with_context(ctx, "get_exchangeable_bond", lambda context: context.ds005.get_exchangeable_bond(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_creditor_management_termination",
    description="주요사항보고서(채권은행 등의 관리절차 중단) 내에 주요 정보를 제공합니다. 반환값에는 중단일자, 중단사유, 채권은행명, 향후계획 등이 포함됩니다.",
    tags={"주요사항보고서", "채권은행", "관리절차", "중단"}
)
def get_creditor_management_termination(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    채권은행 등의 관리절차 중단 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020036
    """
    result = with_context(ctx, "get_creditor_management_termination", lambda context: context.ds005.get_creditor_management_termination(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_write_down_bond",
    description="주요사항보고서(상각형 조건부자본증권 발행결정) 내에 주요 정보를 제공합니다. 반환값에는 발행조건, 상각요건, 발행총액, 발행일자 등이 포함됩니다.",
    tags={"주요사항보고서", "상각형 조건부자본증권", "발행결정", "상각"}
)
def get_write_down_bond(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    상각형 조건부자본증권 발행결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020037
    """
    result = with_context(ctx, "get_write_down_bond", lambda context: context.ds005.get_write_down_bond(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_treasury_stock_acquisition",
    description="주요사항보고서(자기주식 취득 결정) 내에 주요 정보를 제공합니다. 반환값에는 취득예정주식수, 취득금액, 취득기간, 목적 등이 포함됩니다.",
    tags={"주요사항보고서", "자기주식", "취득", "결정"}
)
def get_treasury_stock_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자기주식 취득 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020038
    """
    result = with_context(ctx, "get_treasury_stock_acquisition", lambda context: context.ds005.get_treasury_stock_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_treasury_stock_disposal",
    description="주요사항보고서(자기주식 처분 결정) 내에 주요 정보를 제공합니다. 반환값에는 처분예정주식수, 처분금액, 처분방법, 처분기간 등이 포함됩니다.",
    tags={"주요사항보고서", "자기주식", "처분", "결정"}
)
def get_treasury_stock_disposal(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자기주식 처분 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020039
    """
    result = with_context(ctx, "get_treasury_stock_disposal", lambda context: context.ds005.get_treasury_stock_disposal(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_treasury_stock_trust_contract",
    description="주요사항보고서(자기주식취득 신탁계약 체결 결정) 내에 주요 정보를 제공합니다. 반환값에는 계약체결일, 계약기간, 계약금액, 위탁기관 등이 포함됩니다.",
    tags={"주요사항보고서", "자기주식", "신탁계약", "체결", "결정"}
)
def get_treasury_stock_trust_contract(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자기주식취득 신탁계약 체결 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020040
    """
    result = with_context(ctx, "get_treasury_stock_trust_contract", lambda context: context.ds005.get_treasury_stock_trust_contract(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_treasury_stock_trust_termination",
    description="주요사항보고서(자기주식취득 신탁계약 해지 결정) 내에 주요 정보를 제공합니다. 반환값에는 해지일자, 해지사유, 계약금액, 이사회결의일 등이 포함됩니다.",
    tags={"주요사항보고서", "자기주식", "신탁계약", "해지", "결정"}
)
def get_treasury_stock_trust_termination(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자기주식취득 신탁계약 해지 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020041
    """
    result = with_context(ctx, "get_treasury_stock_trust_termination", lambda context: context.ds005.get_treasury_stock_trust_termination(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_business_acquisition",
    description="주요사항보고서(영업양도 결정) 내에 주요 정보를 제공합니다. 반환값에는 양도일자, 양도대상사업, 양도금액, 계약상대방 등이 포함됩니다.",
    tags={"주요사항보고서", "영업양도", "결정"}
)
def get_business_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    영업양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020043
    """
    result = with_context(ctx, "get_business_acquisition", lambda context: context.ds005.get_business_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_tangible_asset_transfer",
    description="주요사항보고서(유형자산 양수 결정) 내에 주요 정보를 제공합니다. 반환값에는 자산종류, 양수금액, 양수일자, 계약상대방 등이 포함됩니다.",
    tags={"주요사항보고서", "유형자산", "양수", "결정"}
)
def get_tangible_asset_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유형자산 양수 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020044
    """
    result = with_context(ctx, "get_tangible_asset_transfer", lambda context: context.ds005.get_tangible_asset_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_tangible_asset_acquisition",
    description="주요사항보고서(유형자산 양도 결정) 내에 주요 정보를 제공합니다. 반환값에는 자산종류, 양도금액, 양도일자, 계약상대방 등이 포함됩니다.",
    tags={"주요사항보고서", "유형자산", "양도", "결정"}
)
def get_tangible_asset_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유형자산 양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020045
    """
    result = with_context(ctx, "get_tangible_asset_acquisition", lambda context: context.ds005.get_tangible_asset_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_other_corp_stock_transfer",
    description="주요사항보고서(타법인 주식 및 출자증권 양수결정) 내에 주요 정보를 제공합니다. 반환값에는 양수대상 법인명, 양수주식수, 양수금액, 계약일자 등이 포함됩니다.",
    tags={"주요사항보고서", "타법인", "주식", "출자증권", "양수", "결정"}
)
def get_other_corp_stock_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    타법인 주식 및 출자증권 양수결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020046
    """
    result = with_context(ctx, "get_other_corp_stock_transfer", lambda context: context.ds005.get_other_corp_stock_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_other_corp_stock_acquisition",
    description="주요사항보고서(타법인 주식 및 출자증권 양도결정) 내에 주요 정보를 제공합니다. 반환값에는 양도대상 법인명, 양도주식수, 양도금액, 계약일자 등이 포함됩니다.",
    tags={"주요사항보고서", "타법인", "주식", "출자증권", "양도", "결정"}
)
def get_other_corp_stock_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    타법인 주식 및 출자증권 양도결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020047
    """
    result = with_context(ctx, "get_other_corp_stock_acquisition", lambda context: context.ds005.get_other_corp_stock_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_related_bond_transfer",
    description="주요사항보고서(주권 관련 사채권 양수 결정) 내에 주요 정보를 제공합니다. 반환값에는 사채종류, 양수금액, 양수일자, 대상회사명 등이 포함됩니다.",
    tags={"주요사항보고서", "주권", "사채권", "양수", "결정"}
)
def get_stock_related_bond_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주권 관련 사채권 양수 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020048
    """
    result = with_context(ctx, "get_stock_related_bond_transfer", lambda context: context.ds005.get_stock_related_bond_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_related_bond_acquisition",
    description="주요사항보고서(주권 관련 사채권 양도 결정) 내에 주요 정보를 제공합니다. 반환값에는 사채종류, 양도금액, 양도일자, 대상회사명 등이 포함됩니다.",
    tags={"주요사항보고서", "주권", "사채권", "양도", "결정"}
)
def get_stock_related_bond_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주권 관련 사채권 양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020049
    """
    result = with_context(ctx, "get_stock_related_bond_acquisition", lambda context: context.ds005.get_stock_related_bond_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_merger",
    description="주요사항보고서(회사합병 결정) 내에 주요 정보를 제공합니다. 반환값에는 합병상대회사, 합병비율, 합병기일, 합병방법 등이 포함됩니다.",
    tags={"주요사항보고서", "회사합병", "결정"}
)
def get_merger(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회사합병 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020050
    """
    result = with_context(ctx, "get_merger", lambda context: context.ds005.get_merger(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_division",
    description="주요사항보고서(회사분할 결정) 내에 주요 정보를 제공합니다. 반환값에는 분할방식, 분할기일, 분할회사명, 분할비율 등이 포함됩니다.",
    tags={"주요사항보고서", "회사분할", "결정"}
)
def get_division(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회사분할 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020051
    """
    result = with_context(ctx, "get_division", lambda context: context.ds005.get_division(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_division_merger",
    description="주요사항보고서(회사분할합병 결정) 내에 주요 정보를 제공합니다. 반환값에는 분할합병 상대회사, 분할합병 방식, 합병비율, 합병기일 등이 포함됩니다.",
    tags={"주요사항보고서", "회사분할합병", "결정"}
)
def get_division_merger(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회사분할합병 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020052
    """
    result = with_context(ctx, "get_division_merger", lambda context: context.ds005.get_division_merger(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_exchange",
    description="주요사항보고서(주식교환·이전 결정) 내에 주요 정보를 제공합니다. 반환값에는 교환상대회사, 교환비율, 교환기일, 교환방법 등이 포함됩니다.",
    tags={"주요사항보고서", "주식교환", "이전", "결정"}
)
def get_stock_exchange(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주식교환·이전 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020053
    """
    result = with_context(ctx, "get_stock_exchange", lambda context: context.ds005.get_stock_exchange(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

