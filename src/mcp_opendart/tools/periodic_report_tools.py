from typing import Dict, Any, List
from mcp.server.fastmcp import Context

from opendart_mcp.server import mcp

@mcp.tool(
    name="get_stock_increase_decrease",
    description="지정한 기업의 증자(감자) 현황을 조회합니다. 사업연도와 보고서 코드에 따라 최근 보고서에 제출된 주식발행 변경 정보를 확인할 수 있습니다."
)
def get_stock_increase_decrease(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    증자(감자) 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019004
    """
    return ctx.request_context.lifespan_context.ds002.get_stock_increase_decrease(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_dividend_info",
    description="지정한 기업의 사업연도와 보고서 기준으로 배당에 관한 사항을 조회합니다. 배당금총액, 배당성향, 시가배당율 등 주요 배당 정보를 확인할 수 있습니다."
)
def get_dividend_info(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    배당에 관한 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019005
    """
    return ctx.request_context.lifespan_context.ds002.get_dividend_info(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_treasury_stock",
    description="지정한 기업의 자기주식 취득 및 처분 현황을 조회합니다. 사업연도 및 보고서 기준으로 보유 주식 수량, 변동내역 등의 정보를 확인할 수 있습니다."
)
def get_treasury_stock(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    자기주식 취득 및 처분현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019006
    """
    return ctx.request_context.lifespan_context.ds002.get_treasury_stock(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_major_shareholder",
    description="지정한 기업의 최대주주에 관한 사항을 조회합니다. 최대주주의 성명, 소유 지분율, 변동 내역 등을 포함하며, 사업연도 및 보고서 기준으로 제공합니다."
)
def get_major_shareholder(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    최대주주에 관한 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019007
    """
    return ctx.request_context.lifespan_context.ds002.get_major_shareholder(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_major_shareholder_changes",
    description="지정한 기업의 최대주주의 주식 보유 변동사항을 조회합니다. 최대주주 또는 그와 특수관계인의 지분 증가/감소 내역을 사업연도 및 보고서 기준으로 제공합니다."
)
def get_major_shareholder_changes(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    최대주주의 주식변동 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019008
    """
    return ctx.request_context.lifespan_context.ds002.get_major_shareholder_changes(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_minority_shareholder",
    description="지정한 기업의 소액주주에 관한 사항을 조회합니다. 소액주주 수, 소유 주식 수 및 비율 등의 정보를 사업연도와 보고서 기준으로 제공합니다."
)
def get_minority_shareholder(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    소액주주에 관한 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019009
    """
    return ctx.request_context.lifespan_context.ds002.get_minority_shareholder(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_executive_info",
    description="지정한 기업의 임원 현황을 조회합니다. 임원의 성명, 직위, 성별, 생년월일, 등기임원 여부, 주요 경력 등을 사업연도와 보고서 기준으로 제공합니다."
)
def get_executive_info(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    임원의 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019010
    """
    return ctx.request_context.lifespan_context.ds002.get_executive_info(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_employee_info",
    description="지정한 기업의 직원 현황을 조회합니다. 정규직/비정규직, 남녀별 인원 수 및 1인당 평균 급여 등의 정보를 사업연도와 보고서 기준으로 제공합니다."
)
def get_employee_info(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    직원 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019011
    """
    return ctx.request_context.lifespan_context.ds002.get_employee_info(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_individual_compensation",
    description="5억원 이상 보수를 지급받은 등기임원에 대한 보수 현황을 조회합니다. 이름, 직위, 급여총액, 상여금 등의 정보를 사업연도 및 보고서 기준으로 제공합니다."
)
def get_individual_compensation(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    개별 임원 보수 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019012
    """
    return ctx.request_context.lifespan_context.ds002.get_individual_compensation(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_total_compensation",
    description="지정한 기업의 전체 임원 보수 현황을 조회합니다. 전체 등기/미등기임원의 인원 수, 급여총액 및 1인당 평균보수 등의 정보를 제공합니다."
)
def get_total_compensation(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    임원 전체 보수 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019013
    """
    return ctx.request_context.lifespan_context.ds002.get_total_compensation(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_individual_compensation_amount",
    description="정기보고서(사업, 분기, 반기보고서) 내에 개인별 보수지급 금액(5억이상 상위5인)을 제공합니다. 반환값에는 임원의 성명, 직위, 성별, 담당업무, 보수총액 및 비고가 포함됩니다."
)
def get_individual_compensation_amount(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    개인별 보수지급 금액 조회 (5억 이상 상위 5인)

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019014
    """
    return ctx.request_context.lifespan_context.ds002.get_individual_compensation_amount(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_investment_in_other_corp",
    description="정기보고서(사업, 분기, 반기보고서) 내에 타법인 출자현황을 제공합니다. 반환값에는 출자대상 법인의 명칭, 고유번호, 출자목적, 출자금액, 보유주식 수, 지분율 및 비고가 포함됩니다."
)
def get_investment_in_other_corp(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    타법인 출자현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019015
    """
    return ctx.request_context.lifespan_context.ds002.get_investment_in_other_corp(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_stock_total",
    description="정기보고서(사업, 분기, 반기보고서) 내에 주식의총수현황을 제공합니다. 반환값에는 주식종류, 주식의 총수, 1주당 금액, 비고 등이 포함됩니다."
)
def get_stock_total(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    주식의 총수 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020002
    """
    return ctx.request_context.lifespan_context.ds002.get_stock_total(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_debt_securities_issued",
    description="정기보고서(사업, 분기, 반기보고서) 내에 채무증권 발행실적을 제공합니다. 반환값에는 증권종류, 발행일자, 만기일자, 발행금액, 비고 등이 포함됩니다."
)
def get_debt_securities_issued(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    채무증권 발행실적 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020003
    """
    return ctx.request_context.lifespan_context.ds002.get_debt_securities_issued(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_commercial_paper_outstanding",
    description="정기보고서(사업, 분기, 반기보고서) 내에 기업어음증권 미상환 잔액을 제공합니다. 반환값에는 증권종류, 발행일자, 만기일자, 미상환잔액, 비고 등이 포함됩니다."
)
def get_commercial_paper_outstanding(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    기업어음증권 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020004
    """
    return ctx.request_context.lifespan_context.ds002.get_commercial_paper_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_short_term_bond_outstanding",
    description="정기보고서(사업, 분기, 반기보고서) 내에 단기사채 미상환 잔액을 제공합니다. 반환값에는 증권종류, 발행일자, 만기일자, 미상환잔액, 비고 등이 포함됩니다."
)
def get_short_term_bond_outstanding(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    단기사채 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020005
    """
    return ctx.request_context.lifespan_context.ds002.get_short_term_bond_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_corporate_bond_outstanding",
    description="정기보고서(사업, 분기, 반기보고서) 내에 회사채 미상환 잔액을 제공합니다. 반환값에는 증권종류, 발행일자, 만기일자, 미상환잔액, 비고 등이 포함됩니다."
)
def get_corporate_bond_outstanding(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    회사채 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020006
    """
    return ctx.request_context.lifespan_context.ds002.get_corporate_bond_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_hybrid_securities_outstanding",
    description="정기보고서(사업, 분기, 반기보고서) 내에 신종자본증권 미상환 잔액을 제공합니다. 반환값에는 증권종류, 발행일자, 만기일자, 미상환잔액, 비고 등이 포함됩니다."
)
def get_hybrid_securities_outstanding(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    신종자본증권 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020007
    """
    return ctx.request_context.lifespan_context.ds002.get_hybrid_securities_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_contingent_convertible_bond_outstanding",
    description="정기보고서(사업, 분기, 반기보고서) 내에 조건부 자본증권 미상환 잔액을 제공합니다. 반환값에는 증권종류, 발행일자, 만기일자, 미상환잔액, 비고 등이 포함됩니다."
)
def get_contingent_convertible_bond_outstanding(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    조건부 자본증권 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020008
    """
    return ctx.request_context.lifespan_context.ds002.get_contingent_convertible_bond_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_accounting_auditor_opinion",
    description="정기보고서(사업, 분기, 반기보고서) 내에 회계감사인의 명칭 및 감사의견을 제공합니다. 반환값에는 감사인 명칭, 감사의견, 의견변경 여부 및 사유, 비고 등이 포함됩니다."
)
def get_accounting_auditor_opinion(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    회계감사인의 명칭 및 감사의견 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020009
    """
    return ctx.request_context.lifespan_context.ds002.get_accounting_auditor_opinion(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_audit_service_contract",
    description="정기보고서(사업, 분기, 반기보고서) 내에 감사용역체결현황을 제공합니다. 반환값에는 감사인명, 계약금액, 계약일자, 계약기간, 비고 등이 포함됩니다."
)
def get_audit_service_contract(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    감사용역체결현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020010
    """
    return ctx.request_context.lifespan_context.ds002.get_audit_service_contract(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_non_audit_service_contract",
    description="정기보고서(사업, 분기, 반기보고서) 내에 회계감사인과의 비감사용역 계약체결 현황을 제공합니다. 반환값에는 감사인명, 용역내용, 계약일자, 계약기간, 계약금액, 비고 등이 포함됩니다."
)
def get_non_audit_service_contract(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    회계감사인과의 비감사용역 계약체결 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020011
    """
    return ctx.request_context.lifespan_context.ds002.get_non_audit_service_contract(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_outside_director_status",
    description="정기보고서(사업, 분기, 반기보고서) 내에 사외이사 및 그 변동현황을 제공합니다. 반환값에는 성명, 직위, 변동유형, 변동일자, 임기, 비고 등이 포함됩니다."
)
def get_outside_director_status(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    사외이사 및 그 변동현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020012
    """
    return ctx.request_context.lifespan_context.ds002.get_outside_director_status(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_unregistered_exec_compensation",
    description="정기보고서(사업, 분기, 반기보고서) 내에 미등기임원 보수현황을 제공합니다. 반환값에는 직위, 인원수, 보수총액, 비고 등이 포함됩니다."
)
def get_unregistered_exec_compensation(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    미등기임원 보수현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020013
    """
    return ctx.request_context.lifespan_context.ds002.get_unregistered_exec_compensation(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_executive_compensation_approved",
    description="정기보고서(사업, 분기, 반기보고서) 내에 이사·감사 전체의 보수현황(주주총회 승인금액)을 제공합니다. 반환값에는 직위, 인원수, 승인된 보수총액, 비고 등이 포함됩니다."
)
def get_executive_compensation_approved(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    이사·감사 전체의 보수현황 (주주총회 승인금액) 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020014
    """
    return ctx.request_context.lifespan_context.ds002.get_executive_compensation_approved(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_executive_compensation_by_type",
    description="정기보고서(사업, 분기, 반기보고서) 내에 이사·감사 전체의 보수현황(보수지급금액 - 유형별)을 제공합니다. 반환값에는 직위, 인원수, 보수 유형, 지급금액, 비고 등이 포함됩니다."
)
def get_executive_compensation_by_type(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    이사·감사 전체의 보수현황 (보수지급금액 - 유형별) 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020015
    """
    return ctx.request_context.lifespan_context.ds002.get_executive_compensation_by_type(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_public_fund_usage",
    description="정기보고서(사업, 분기, 반기보고서) 내에 공모자금의 사용내역을 제공합니다. 반환값에는 사용 사업명, 조달금액, 사용금액, 잔액, 향후 사용계획, 비고 등이 포함됩니다."
)
def get_public_fund_usage(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    공모자금의 사용내역 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020016
    """
    return ctx.request_context.lifespan_context.ds002.get_public_fund_usage(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool(
    name="get_private_fund_usage",
    description="정기보고서(사업, 분기, 반기보고서) 내에 사모자금의 사용내역을 제공합니다. 반환값에는 사용 사업명, 조달금액, 사용금액, 잔액, 향후 사용계획, 비고 등이 포함됩니다."
)
def get_private_fund_usage(ctx: Context, corp_code: str, bsns_year: str, reprt_code: str) -> Dict[str, Any]:
    """
    사모자금의 사용내역 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2023)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020017
    """
    return ctx.request_context.lifespan_context.ds002.get_private_fund_usage(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )
