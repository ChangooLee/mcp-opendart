import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")

@mcp.tool(
    name="get_stock_increase_decrease",
    description="정기보고서 기반 주식 증자·감자 내역을 통한 자본금 변동 및 지배구조 재편 리스크 분석",
    tags={"증자", "감자", "자본금", "지배구조", "정기보고서"}
)
def get_stock_increase_decrease(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    증자(감자) 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019004
    """
    result = with_context(ctx, "get_stock_increase_decrease", lambda context: context.ds002.get_stock_increase_decrease(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_dividend_info",
    description="배당금 총액 및 배당성향을 통한 이익 분배 정책과 재무 건전성 리스크 분석",
    tags={"배당", "현금배당", "배당성향", "유동성리스크", "정기보고서"}
)
def get_dividend_info(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    배당에 관한 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019005
    """
    result = with_context(ctx, "get_dividend_info", lambda context: context.ds002.get_dividend_info(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_treasury_stock",
    description="자기주식의 취득·처분·소각 내역을 통한 주가 방어 및 지배구조 조정 리스크 분석",
    tags={"자기주식", "소각", "지배구조", "주가방어", "정기보고서"}
)
def get_treasury_stock(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자기주식 취득 및 처분현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019006
    """
    result = with_context(ctx, "get_treasury_stock", lambda context: context.ds002.get_treasury_stock(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_major_shareholder",
    description="최대주주 및 특수관계인의 지분 현황을 통한 지배구조 안정성과 승계 리스크 분석",
    tags={"최대주주", "지배구조", "특수관계자", "승계", "정기보고서"}
)
def get_major_shareholder(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    최대주주에 관한 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019007
    """
    result = with_context(ctx, "get_major_shareholder", lambda context: context.ds002.get_major_shareholder(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_major_shareholder_changes",
    description="최대주주 지분 변동 내역을 통한 경영권 변동 및 승계 흐름 리스크 분석",
    tags={"최대주주", "지분변동", "경영권", "승계", "정기보고서"}
)
def get_major_shareholder_changes(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    최대주주의 주식변동 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019008
    """
    result = with_context(ctx, "get_major_shareholder_changes", lambda context: context.ds002.get_major_shareholder_changes(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_minority_shareholder",
    description="소액주주 수 및 지분율을 통한 지배구조 분산도와 M&A 방어력 리스크 분석",
    tags={"소액주주", "지배구조", "M&A", "주주분포", "정기보고서"}
)
def get_minority_shareholder(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    소액주주에 관한 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019009
    """
    result = with_context(ctx, "get_minority_shareholder", lambda context: context.ds002.get_minority_shareholder(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_executive_info",
    description="임원 현황을 통한 경영진 구성, 경력 적합성 및 지배구조 리스크 분석",
    tags={"임원", "경영진", "지배구조", "경영리스크", "정기보고서"}
)
def get_executive_info(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    임원의 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019010
    """
    result = with_context(ctx, "get_executive_info", lambda context: context.ds002.get_executive_info(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_employee_info",
    description="직원 수, 급여, 고용 형태 등을 통한 인건비 구조 및 조직 안정성 리스크 분석",
    tags={"직원", "인건비", "고용형태", "조직안정성", "정기보고서"}
)
def get_employee_info(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    직원 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019011
    """
    result = with_context(ctx, "get_employee_info", lambda context: context.ds002.get_employee_info(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_individual_compensation",
    description="개별 임원 보수 내역을 통한 보상 집중도 및 내부자 리스크 분석",
    tags={"임원", "보수", "급여", "지배구조", "정기보고서"}
)
def get_individual_compensation(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    개별 임원 보수 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019012
    """
    result = with_context(ctx, "get_individual_compensation", lambda context: context.ds002.get_individual_compensation(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_total_compensation",
    description="전체 임원 보수 총액을 통한 보상 구조의 투명성과 집중도 리스크 분석",
    tags={"임원", "보수총액", "보상구조", "투명성", "정기보고서"}
)
def get_total_compensation(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    임원 전체 보수 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019013
    """
    result = with_context(ctx, "get_total_compensation", lambda context: context.ds002.get_total_compensation(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_individual_compensation_amount",
    description="고액 수령자 중심 임원 보수 정보를 통한 보상 불균형 및 지배구조 리스크 분석",
    tags={"개별임원", "보수", "고액수령자", "지배구조", "정기보고서"}
)
def get_individual_compensation_amount(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    개인별 보수지급 금액 조회 (5억 이상 상위 5인)

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019014
    """
    result = with_context(ctx, "get_individual_compensation_amount", lambda context: context.ds002.get_individual_compensation_amount(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_investment_in_other_corp",
    description="타법인 출자 내역을 통한 계열 리스크 및 재무 건전성 분석",
    tags={"출자", "타법인", "계열사", "재무건전성", "정기보고서"}
)
def get_investment_in_other_corp(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    타법인 출자현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019015
    """
    result = with_context(ctx, "get_investment_in_other_corp", lambda context: context.ds002.get_investment_in_other_corp(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_total",
    description="주식 총수 내역을 통한 자본금 구성 및 유통물량 리스크 분석",
    tags={"주식총수", "유통주식", "자본구조", "지배구조", "정기보고서"}
)
def get_stock_total(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주식의 총수 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020002
    """
    result = with_context(ctx, "get_stock_total", lambda context: context.ds002.get_stock_total(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_debt_securities_issued",
    description="채무증권 발행 실적을 통한 자금조달 구조 및 부채 리스크 분석",
    tags={"채무증권", "회사채", "자금조달", "부채", "정기보고서"}
)
def get_debt_securities_issued(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    채무증권 발행실적 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020003
    """
    result = with_context(ctx, "get_debt_securities_issued", lambda context: context.ds002.get_debt_securities_issued(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_commercial_paper_outstanding",
    description="기업어음 미상환 내역을 통한 단기 유동성 및 차환 리스크 분석",
    tags={"기업어음", "단기차입", "유동성", "리스크", "정기보고서"}
)
def get_commercial_paper_outstanding(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    기업어음증권 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020004
    """
    result = with_context(ctx, "get_commercial_paper_outstanding", lambda context: context.ds002.get_commercial_paper_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_short_term_bond_outstanding",
    description="단기사채 미상환 내역을 통한 단기 자금조달 구조 및 유동성 리스크 분석",
    tags={"단기사채", "단기자금", "유동성", "차환리스크", "정기보고서"}
)
def get_short_term_bond_outstanding(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    단기사채 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020005
    """
    result = with_context(ctx, "get_short_term_bond_outstanding", lambda context: context.ds002.get_short_term_bond_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_corporate_bond_outstanding",
    description="회사채 미상환 내역을 통한 장기 부채 구조 및 상환 리스크 분석",
    tags={"회사채", "장기부채", "상환리스크", "레버리지", "정기보고서"}
)
def get_corporate_bond_outstanding(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회사채 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020006
    """
    result = with_context(ctx, "get_corporate_bond_outstanding", lambda context: context.ds002.get_corporate_bond_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_hybrid_securities_outstanding",
    description="신종자본증권 미상환 내역을 통한 자본성 부채 리스크 및 회계 분류 리스크 분석",
    tags={"신종자본증권", "하이브리드", "자본성부채", "상환리스크", "정기보고서"}
)
def get_hybrid_securities_outstanding(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    신종자본증권 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020007
    """
    result = with_context(ctx, "get_hybrid_securities_outstanding", lambda context: context.ds002.get_hybrid_securities_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_conditional_capital_securities_outstanding",
    description="상각형 조건부자본증권 미상환 내역을 통한 자본손실 및 상각 리스크 분석",
    tags={"조건부자본", "상각", "자본손실", "레버리지", "정기보고서"}
)
def get_conditional_capital_securities_outstanding(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    조건부 자본증권 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020008
    """
    result = with_context(ctx, "get_conditional_capital_securities_outstanding", lambda context: context.ds002.get_conditional_capital_securities_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_accounting_auditor_opinion",
    description="감사의견 및 강조사항을 통한 회계 신뢰성 및 지속가능성 리스크 분석",
    tags={"감사의견", "회계감사", "강조사항", "지속가능성", "정기보고서"}
)
def get_accounting_auditor_opinion(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회계감사인의 명칭 및 감사의견 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020009
    """
    result = with_context(ctx, "get_accounting_auditor_opinion", lambda context: context.ds002.get_accounting_auditor_opinion(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_audit_service_contract",
    description="감사용역계약 체결 내역을 통한 감사품질 및 독립성 리스크 분석",
    tags={"감사용역", "계약", "보수", "감사품질", "정기보고서"}
)
def get_audit_service_contract(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    감사용역체결현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020010
    """
    result = with_context(ctx, "get_audit_service_contract", lambda context: context.ds002.get_audit_service_contract(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_non_audit_service_contract",
    description="비감사용역 계약 내역을 통한 감사인의 독립성 훼손 및 이해상충 리스크 분석",
    tags={"비감사용역", "계약", "이해상충", "감사독립성", "정기보고서"}
)
def get_non_audit_service_contract(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회계감사인과의 비감사용역 계약체결 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020011
    """
    result = with_context(ctx, "get_non_audit_service_contract", lambda context: context.ds002.get_non_audit_service_contract(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_outside_director_status",
    description="사외이사 현황을 통한 이사회 독립성과 지배구조 감시 기능 리스크 분석",
    tags={"사외이사", "이사회", "지배구조", "독립성", "정기보고서"}
)
def get_outside_director_status(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    사외이사 및 그 변동현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020012
    """
    result = with_context(ctx, "get_outside_director_status", lambda context: context.ds002.get_outside_director_status(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_unregistered_exec_compensation",
    description="미등기임원 보수 내역을 통한 내부자 보상 투명성 및 통제 리스크 분석",
    tags={"미등기임원", "보수", "보상투명성", "지배구조", "정기보고서"}
)
def get_unregistered_exec_compensation(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    미등기임원 보수현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020013
    """
    result = with_context(ctx, "get_unregistered_exec_compensation", lambda context: context.ds002.get_unregistered_exec_compensation(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_executive_compensation_approved",
    description="주총 승인 보수 한도를 통한 보상 지배구조 및 집행 투명성 리스크 분석",
    tags={"이사", "감사", "보수승인", "주총", "정기보고서"}
)
def get_executive_compensation_approved(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    이사·감사 전체의 보수현황 (주주총회 승인금액) 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020014
    """
    result = with_context(ctx, "get_executive_compensation_approved", lambda context: context.ds002.get_executive_compensation_approved(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_executive_compensation_by_type",
    description="임원 유형별 보수지급 내역을 통한 보상 집중도 및 지배구조 리스크 분석",
    tags={"이사", "감사", "보수유형", "보상집중도", "정기보고서"}
)
def get_executive_compensation_by_type(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    이사·감사 전체의 보수현황 (보수지급금액 - 유형별) 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020015
    """
    result = with_context(ctx, "get_executive_compensation_by_type", lambda context: context.ds002.get_executive_compensation_by_type(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_public_capital_usage",
    description="공모자금 사용 계획과 집행 내역을 통한 자금 운용 투명성과 전용 리스크 분석",
    tags={"공모자금", "자금운용", "사용계획", "전용리스크", "정기보고서"}
)
def get_public_capital_usage(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    공모자금의 사용내역 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020016
    """
    result = with_context(ctx, "get_public_capital_usage", lambda context: context.ds002.get_public_capital_usage(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_private_capital_usage",
    description="사모자금 사용 내역을 통한 계획 이행률 및 유동성 전용 리스크 분석",
    tags={"사모자금", "자금사용", "계획이행", "유동성", "정기보고서"}
)
def get_private_capital_usage(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    사모자금의 사용내역 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020017
    """
    result = with_context(ctx, "get_private_capital_usage", lambda context: context.ds002.get_private_capital_usage(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))
