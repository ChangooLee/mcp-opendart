import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")
@mcp.tool(
    name="get_asset_transfer",
    description="자산양수도 및 풋백옵션 계약을 통한 경영전략 변화 및 추가 부채 리스크 분석",
    tags={"자산양수도", "풋백옵션", "경영전략", "재무리스크"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="부도 발생 사실을 기반으로 기업의 유동성 위기 및 구조적 부실 리스크 분석",
    tags={"부도", "유동성위기", "재무리스크", "구조적부실"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="사업부문 단위 영업정지를 통한 수익성 악화 및 기업 존속 리스크 평가",
    tags={"영업정지", "수익성악화", "사업중단", "존속리스크"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="회생절차 개시신청을 통해 기업의 구조조정 가능성과 회생전략 분석",
    tags={"회생절차", "구조조정", "재무위기", "경영정상화"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="해산사유 발생을 통해 기업의 법적 존속성 상실 및 청산 리스크 분석",
    tags={"해산", "청산리스크", "존속성상실", "지배구조변동"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="유상증자를 통한 자금조달 구조와 지분 희석 및 재무구조 개선 의도 분석",
    tags={"유상증자", "자금조달", "지분희석", "재무구조"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="무상증자를 통한 자본구조 조정 및 주주지분 변화 리스크 분석",
    tags={"무상증자", "자본조정", "지분변동", "재무리스크"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="유무상증자 병행 결정을 통한 복합 자본 전략 및 지배구조 재편 가능성 분석",
    tags={"유무상증자", "복합자본전략", "지배구조", "증자전략"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="감자 결정을 통한 자본 축소 목적 및 경영 리스크 대응 전략 분석",
    tags={"감자", "자본감축", "경영리스크", "재무전략"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="채권자 관리절차 개시를 통한 기업의 구조조정 진행 및 유동성 위기 분석",
    tags={"채권관리", "구조조정", "유동성위기", "재무위기"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="소송 제기 사실을 통한 경영권 분쟁 및 재무 리스크 조기 분석",
    tags={"소송", "경영권분쟁", "재무리스크", "법적위기"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="해외상장 결정을 통해 자금조달 전략 및 글로벌 리스크 요인 분석",
    tags={"해외상장", "자금조달", "글로벌리스크", "지배구조변동"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="해외증권시장 상장폐지 결정을 통한 글로벌 시장 철수 전략 및 지배구조 변동 리스크 분석",
    tags={"해외상장폐지", "글로벌리스크", "지배구조", "사업철수", "주요사항보고서"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="해외증권시장 상장을 통한 글로벌 시장 진출 전략 및 자금조달 구조 분석",
    tags={"해외상장", "글로벌전략", "자금조달", "지배구조", "주요사항보고서"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="해외증권시장 상장폐지를 통한 해외사업 축소 및 자본구조 변동성 리스크 분석",
    tags={"해외상장폐지", "사업축소", "지배구조", "자본구조", "주요사항보고서"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="전환사채 발행 결정을 통한 자금조달 전략 및 주주가치 희석 리스크 분석",
    tags={"전환사채", "자금조달", "지분희석", "주요사항보고서"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="신주인수권부사채 발행을 통한 지분희석 가능성과 재무레버리지 리스크 분석",
    tags={"신주인수권부사채", "지분희석", "재무리스크", "자금조달"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="교환사채 발행을 통한 특정 기업 지분 연결성과 주가 변동성 리스크 분석",
    tags={"교환사채", "지분변동", "주가연동", "자금조달", "주요사항보고서"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="채권자 관리절차 종료를 통한 구조조정 완료 여부 및 경영정상화 리스크 분석",
    tags={"채권자관리", "구조조정", "경영정상화", "재무리스크"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="상각형 조건부자본증권 발행을 통한 재무구조 보완 및 잠재적 상각 리스크 분석",
    tags={"조건부자본증권", "상각리스크", "자본보완", "재무리스크"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="자기주식 취득 결정을 통한 주가 방어 전략 및 경영권 방어 가능성 분석",
    tags={"자기주식취득", "주가방어", "지배구조", "경영권방어"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="자기주식 처분 결정을 통한 자본구조 변화 및 경영권 변동 가능성 분석",
    tags={"자기주식처분", "지배구조", "자본구조", "경영권변동"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="자기주식 신탁계약 체결을 통한 주가안정화 및 경영권 방어 수단 분석",
    tags={"신탁계약", "자기주식", "주가안정", "지배구조", "경영권방어"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="자기주식 신탁계약 해지를 통한 주가정책 변경 및 지배구조 리스크 분석",
    tags={"신탁해지", "자기주식", "지배구조", "주가정책변경"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="영업양수 결정을 통한 사업 확장 전략 및 내부거래 리스크 분석",
    tags={"영업양수", "사업확장", "내부거래", "지배구조"}
)
def get_business_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    영업양수 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020042
    """
    result = with_context(ctx, "get_business_acquisition", lambda context: context.ds005.get_business_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_business_transfer",
    description="영업양도 결정을 통한 사업 철수 전략 및 자산이전 리스크 분석",
    tags={"영업양도", "사업철수", "자산이전", "지배구조"}
)
def get_business_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    영업양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020043
    """
    result = with_context(ctx, "get_business_transfer", lambda context: context.ds005.get_business_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_tangible_asset_acquisition",
    description="유형자산 양수 결정을 통한 자산 구조 변화 및 특수관계자 거래 리스크 분석",
    tags={"유형자산", "자산양수", "특수관계자", "재무구조"}
)
def get_tangible_asset_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유형자산 양수 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020044
    """
    result = with_context(ctx, "get_tangible_asset_acquisition", lambda context: context.ds005.get_tangible_asset_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_tangible_asset_transfer",
    description="유형자산 양도 결정을 통한 유동성 확보 및 구조조정 리스크 분석",
    tags={"유형자산", "자산양도", "유동성", "구조조정"}
)
def get_tangible_asset_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유형자산 양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020045
    """
    result = with_context(ctx, "get_tangible_asset_transfer", lambda context: context.ds005.get_tangible_asset_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_other_corp_stock_acquisition",
    description="타법인 주식 양수를 통한 지배구조 강화 및 우회상장 가능성 분석",
    tags={"타법인", "주식양수", "지배구조", "우회상장"}
)
def get_other_corp_stock_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    타법인 주식 및 출자증권 양수결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020046
    """
    result = with_context(ctx, "get_other_corp_stock_acquisition", lambda context: context.ds005.get_other_corp_stock_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_other_corp_stock_transfer",
    description="타법인 주식 양도를 통한 자산 유동화 및 사업 철수 신호 분석",
    tags={"타법인", "주식양도", "자산유동화", "사업철수"}
)
def get_other_corp_stock_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    타법인 주식 및 출자증권 양도결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020047
    """
    result = with_context(ctx, "get_other_corp_stock_transfer", lambda context: context.ds005.get_other_corp_stock_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_related_bond_acquisition",
    description="주식 관련 사채권 양수를 통한 지분 확보 전략 및 내부거래 리스크 분석",
    tags={"사채권", "전환사채", "지분확보", "내부거래"}
)
def get_stock_related_bond_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주권 관련 사채권 양수 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020048
    """
    result = with_context(ctx, "get_stock_related_bond_acquisition", lambda context: context.ds005.get_stock_related_bond_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_related_bond_transfer",
    description="주식 관련 사채권 양도를 통한 자금 유동화 및 지분변동 리스크 분석",
    tags={"사채권", "전환사채", "자금유동화", "지분변동"}
)
def get_stock_related_bond_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주권 관련 사채권 양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020049
    """
    result = with_context(ctx, "get_stock_related_bond_transfer", lambda context: context.ds005.get_stock_related_bond_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_merger",
    description="합병 결정을 통한 지배구조 재편 및 소액주주 보호 리스크 분석",
    tags={"합병", "지배구조", "소액주주", "재무구조"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="회사분할 결정을 통한 사업 구조 재편 및 상장 우회 리스크 분석",
    tags={"회사분할", "사업재편", "지배구조", "우회상장"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="분할합병 결정을 통한 사업 재편 및 합병 공정성 리스크 분석",
    tags={"분할합병", "사업재편", "지배구조", "합병공정성"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="주식교환·이전 결정을 통한 완전자회사화 및 지배구조 개편 리스크 분석",
    tags={"주식교환", "지배구조", "완전자회사", "우회상장"}
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020053
    """
    result = with_context(ctx, "get_stock_exchange", lambda context: context.ds005.get_stock_exchange(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

