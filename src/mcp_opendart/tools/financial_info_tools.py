import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")
@mcp.tool(
    name="get_single_acnt",
    description="단일 기업의 핵심 재무 지표와 주요 계정 정보를 분석 가능한 형태로 제공합니다. XBRL 형식으로 제출된 재무제표에서 매출액, 영업이익, 당기순이익 등 핵심 재무 계정을 추출합니다.\n\n【제공 데이터】\n- 주요 재무상태표 항목: 자산총계, 부채총계, 자본총계, 유동자산, 비유동자산 등\n- 주요 손익계산서 항목: 매출액, 영업이익, 법인세차감전이익, 당기순이익 등\n- 연결재무제표(CFS)와 개별재무제표(OFS) 모두 제공\n- 당기 및 전기 데이터 비교 가능\n\n【입력 파라미터】\n- corp_code: 기업 고유번호 (8자리)\n- bsns_year: 사업연도 (예: 2025)\n- reprt_code: 보고서 코드 (11011:사업보고서, 11012:반기보고서, 11013:1분기보고서, 11014:3분기보고서)\n- fs_div (선택): 재무제표 구분 (OFS:개별, CFS:연결)\n\n【활용 시나리오】\n- 기업 분기별/연간 실적 분석\n- 전기 대비 성장성 및 수익성 변화 추세 파악\n- 핵심 재무지표 기반 기업 건전성 평가\n- 투자 의사결정을 위한 기본 재무 정보 확인\n\n【분석 팁】\n- 계정 순서(ord)에 따라 정렬하여 재무제표 구조 파악\n- 통화 단위(currency) 확인 (대부분 KRW, 단위는 원)\n- 금액은 문자열로 반환되므로 분석 시 숫자로 변환 필요\n- 전기 대비 성장률 계산: (당기금액-전기금액)/전기금액*100",
    tags={"재무제표", "계정과목", "정기보고서", "단일회사"}
)
def get_single_acnt(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    fs_div: Optional[str] = None,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    단일회사 주요계정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서 코드 (예: 11011: 사업보고서, 11012: 반기보고서 등)
        fs_div (Optional[str]): 개별/연결 구분 (OFS: 개별, CFS: 연결). 기본값 없음.

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019016
    """
    result = with_context(ctx, "get_single_acnt", lambda context: context.ds003.get_single_acnt(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code,
        fs_div=fs_div
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_multi_acnt",
    description="기업의 연결재무제표를 통해 그룹 전체의 재무 건전성과 경영성과를 종합적으로 분석할 수 있는 핵심 도구입니다. 기업집단의 실질적 경제력과 잠재적 위험요소를 파악하는 데 필수적입니다.\n\n【핵심 분석 요소】\n- 연결 매출액/이익: 그룹 전체의 실질적 사업 규모와 수익성 파악\n- 부채비율: 연결기준 재무 안정성과 차입 의존도 평가\n- 자본구조: 그룹 전체의 자본 건전성과 자본잠식 위험 분석\n- 시계열 변화: 3개년 재무지표 추이로 성장성과 지속가능성 평가\n- 내부거래 제거: 계열사 간 거래를 제외한 순수 외부 경영성과 확인\n\n【지배구조 분석 활용법】\n- 연결/개별 비교: 자회사 의존도와 수익 기여도 파악(연결-개별 매출액 차이)\n- 위험요소 평가: 지배회사 외 종속회사 문제가 전체 그룹에 미치는 영향 분석\n- 차입 비교: 지배회사와 그룹 전체의 부채비율 차이로 숨겨진 부채 파악\n- 수익구조 분석: 지배회사와 종속회사 간 수익성 차이 및 그룹 내 역할 분석\n\n【연계 분석 시나리오】\n- 기업 개황 파악: get_corporation_info로 기업 기본정보 및 결산월 확인\n- 공시 일정 확인: get_disclosure_list로 최근 재무제표 공시 여부 확인\n- 상세 계정 분석: get_single_acc로 전체 계정과목 세부내역 확인\n- 산업 비교 분석: 동종업계 여러 기업의 코드를 검색해 개별 get_single_acnt로 비교\n- 경영자 위험요소 점검: get_executive_trading으로 대표이사의 주식거래 분석\n- 재무비율 계산: get_single_index로 수익성/안정성/성장성/활동성 지표 확인\n\n【분석 진행 단계】\n1. 기본정보 확인: 연결대상 종속회사 수, 주요 계열사 현황 파악\n2. 재무상태표 분석: 자산/부채/자본 구조와 전년 대비 변화 분석\n3. 손익계산서 분석: 매출, 영업이익, 당기순이익의 추이와 변동성 평가\n4. 현금흐름 분석: 영업/투자/재무활동 현금흐름의 건전성 점검\n5. 종합 평가: 그룹 전체의 재무 건전성, 수익성, 성장성 종합 판단\n\n【주의사항 및 팁】\n- 연결재무제표는 내부거래가 제거된 금액으로 그룹 외부와의 거래만 반영\n- 종속회사 변동(인수/매각)이 있는 경우 전년 대비 단순 비교는 왜곡될 수 있음\n- 재무제표 주석사항에서 연결대상 종속회사 목록 및 지분율 확인 필요\n- 연결기준 부채비율과 개별기준 부채비율의 큰 차이는 종속회사의 과도한 차입 의심",
    tags={"재무제표", "계정과목", "정기보고서", "다중회사"}
)
def get_multi_acnt(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    fs_div: Optional[str] = None,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    다중회사 주요계정 조회

    Args:
        corp_code (str): 고유번호 목록
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서 코드 (예: 11011: 사업보고서, 11012: 반기보고서 등)
        fs_div (Optional[str]): 개별/연결 구분 (OFS: 개별, CFS: 연결). 기본값 없음.

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019017
    """
    result = with_context(ctx, "get_multi_acnt", lambda context: context.ds003.get_multi_acnt(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code,
        fs_div=fs_div
    ))
    return TextContent(type="text", text=str(result))

# @mcp.tool(
#     name="get_xbrl_file",
#     description="상장법인 및 주요 비상장법인이 제출한 정기보고서 내에 XBRL재무제표의 원본파일(XBRL)을 제공합니다. 반환값에는 XBRL 압축파일의 저장 경로 및 다운로드 상태 정보가 포함됩니다.",
#     tags={"XBRL", "원본파일", "첨부파일", "정기보고서"}
# )
# def get_xbrl_file(
#     rcept_no: str,
#     reprt_code: str,
#     ctx: Optional[Any] = None
# ) -> TextContent:
#     """
#     재무제표 원본파일(XBRL) 다운로드
# 
#     Args:
#         rcept_no (str): 접수번호 (예: 20240117000238)
#         reprt_code (str): 보고서 코드 (11011: 사업보고서, 11012: 반기보고서 등)
# 
#     참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019019
#     """
#     result = with_context(ctx, "get_xbrl_file", lambda context: context.ds003.get_xbrl_file(
#         rcept_no=rcept_no,
#         reprt_code=reprt_code
#     ))
#     return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_single_acc",
    description="상장법인 및 주요 비상장법인의 정기보고서에 포함된 전체 XBRL 재무제표 데이터를 원본 그대로 제공하는 필수 분석 도구입니다. 모든 계정과목의 정확한 공시 수치를 분석할 수 있어 투자 의사결정과 재무분석에 필수적인 데이터를 확보할 수 있습니다.\n\n【핵심 제공 데이터】\n- 재무상태표: 자산, 부채, 자본 관련 모든 계정과목의 정확한 공시 수치\n- 손익계산서: 매출액, 영업이익, 당기순이익 등 수익성 관련 모든 항목의 정확한 금액\n- 현금흐름표: 영업활동, 투자활동, 재무활동 등 현금흐름의 세부 내역과 규모\n- 자본변동표: 자본금, 이익잉여금, 기타자본 항목의 변동 내역 및 정확한 금액\n- 포괄손익계산서: 당기손익 외 기타포괄손익 항목의 세부 내역과 공시 금액\n\n【분석 활용 특징】\n- 계정과목 위계구조: 계정 순서(ord)를 통한 재무제표 체계적 구조 파악\n- 계정과목 상세: IFRS 표준코드(account_id)로 정확한 계정정보 제공\n- 다년도 비교: 당기, 전기, 전전기의 3개년 데이터를 동시에 제공하여 추세 분석 가능\n- 통화단위 명시: 화폐단위(currency)와 원단위 금액 정보로 정밀한 분석 가능\n- 세부 구분: 재무제표 유형(sj_div) 및 명칭(sj_nm)으로 명확한 분류 제공\n\n【연계 분석 도구】\n- get_corporation_info: 기업 기본정보 확인 후 해당 corp_code로 재무제표 조회\n- get_single_acnt: 주요 계정만 요약 분석 후 get_single_acc로 전체 계정 상세 분석\n- get_xbrl_taxonomy: 표준 계정체계 확인 후 계정과목 코드 맵핑에 활용\n- get_disclosure_list: 최신 공시 확인 후 해당 보고서의 재무제표 상세 분석\n- get_multi_acnt: 동종업계 여러 기업의 주요 계정 비교 후 특정 기업 심층 분석\n\n【활용 시나리오】\n- 정밀 재무분석: 모든 계정과목의 정확한 공시 수치 기반 종합적 재무상태 진단\n- 회계 실사: 세부 계정과목별 변동 추이와 규모를 정확히 파악하여 회계 건전성 평가\n- 투자 모델링: 정확한 공시 데이터를 기반으로 한 정교한 기업가치 평가 모델 구축\n- 동종업계 비교: 산업 내 경쟁사 간 세부 계정과목별 구조 차이와 특성 비교 분석\n- 규제 대응: 금융감독원 제출 공시자료 기반 정확한 기업 정보 확인 및 규제 준수 평가\n\n【효과적 활용 방법】\n- 원하는 항목의 정확한 계정코드(account_id)를 파악하여 특정 계정 추적 분석\n- 3개년 연속 데이터로 CAGR, YoY 성장률, 복합성장률 등 변동 추이 정밀 분석\n- 개별(OFS)과 연결(CFS) 재무제표 간 차이를 비교하여 종속기업 영향도 파악\n- 분기별 실적 변화와 계절성 패턴을 파악하기 위해 reprt_code 변경하여 시계열 분석\n- 계정과목 간 비율과 구성 비중을 계산하여 기업 구조와 전략적 특성 분석",
    tags={"재무제표", "전체계정", "정기보고서", "단일회사"}
)
def get_single_acc(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    fs_div: str = "OFS",
    ctx: Optional[Any] = None
) -> TextContent:
    """
    단일회사 전체 재무제표 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서 코드 (예: 11011: 사업보고서)
        fs_div (str): 개별/연결 구분 (OFS: 개별, CFS: 연결). 기본값: "OFS"

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019020
    """
    result = with_context(ctx, "get_single_acc", lambda context: context.ds003.get_single_acc(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code,
        fs_div=fs_div
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_xbrl_taxonomy",
    description="금융감독원 회계포탈에서 제공하는 IFRS 기반 XBRL 재무제표 공시용 표준 계정체계를 조회하는 도구입니다. 재무제표 항목별 정확한 표준코드 매칭과 데이터 정형화, 비교 분석 체계를 구축하는 데 활용됩니다.\n\n【핵심 제공 데이터】\n- 표준 계정코드(account_id), 순서(ord), 국문 계정명, 영문 계정명\n- 재무제표 구분(BS: 재무상태표, IS: 손익계산서, CIS: 포괄손익계산서 등)\n- XBRL 공시를 위한 재무제표 양식 구조\n\n【분석 활용 특징】\n- 계정 순서(ord) 기반으로 재무제표 항목의 체계적 구조 파악\n- IFRS 표준코드를 활용한 정확한 계정과목 매칭\n- 특정 기업(corp_code), 특정 연도(bsns_year) 기준으로 세부 계정체계 조회 가능\n- 보고서 유형(reprt_code)별 차이 확인 가능\n\n【연계 분석 도구】\n- get_single_acc: 전체 재무제표 원본 데이터와 계정체계 연동 분석\n- get_single_acnt: 주요 재무계정 요약 분석 후 표준계정 연계\n- get_multi_acnt: 그룹 전체 주요 계정 비교 후 세부 계정 매칭\n- get_disclosure_list: 공시된 재무제표 식별 후 표준계정 기반 재구성\n\n【활용 시나리오】\n- XBRL 기반 RAG 재무분석 시스템 구축\n- 기업별, 연도별 재무제표 구조 차이 분석 및 자동화 매칭\n- IFRS 기준 표준화 데이터셋 구축 및 비정형 데이터 정형화\n- 재무제표 항목별 정확한 비교 분석 및 모델 학습 데이터 전처리\n\n【효과적 활용 방법】\n- sj_div를 명확히 지정하여 필요한 재무제표 양식만 조회\n- corp_code와 bsns_year를 지정해 기업별 특수 항목 파악\n- 계정코드(account_id)별 시계열 추적 및 비율 분석 적용\n- IFRS 국제 표준과 국내 기업별 실제 공시 데이터 간 매칭 차이 주의",
    tags={"XBRL", "IFRS", "계정체계", "표준화"}
)
def get_xbrl_taxonomy(
    sj_div: str,
    corp_code: Optional[str] = None,
    bsns_year: Optional[str] = None,
    reprt_code: Optional[str] = None,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    XBRL 택사노미 재무제표 양식 조회

    Args:
        sj_div (str): 재무제표 구분 (BS: 재무상태표, IS: 손익계산서, CIS: 포괄손익계산서 등)
        corp_code (Optional[str]): 고유번호 (선택)
        bsns_year (Optional[str]): 사업연도 (선택)
        reprt_code (Optional[str]): 보고서 코드 (선택)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2020001
    """
    result = with_context(ctx, "get_xbrl_taxonomy", lambda context: context.ds003.get_xbrl_taxonomy(
        sj_div=sj_div,
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_single_index",
    description="상장법인 및 주요 비상장법인이 제출한 정기보고서를 기반으로, 단일 기업의 주요 재무지표를 조회하는 도구입니다. 수익성, 안정성, 성장성, 활동성 지표별로 기업의 핵심 재무 상태를 빠르게 파악할 수 있으며, 특히 당기, 전기, 전전기의 수치 비교를 통해 재무지표의 변동성과 추세를 분석하는 데 필수적으로 활용됩니다.\n\n【핵심 제공 데이터】\n- 수익성 지표: 매출액영업이익률, 매출액순이익률, ROA, ROE 등\n- 안정성 지표: 부채비율, 유동비율, 비유동비율 등\n- 성장성 지표: 매출액증가율, 총자산증가율, 순이익증가율 등\n- 활동성 지표: 총자산회전율, 매출채권회전율, 재고자산회전율 등\n\n【지표 분류별 연계 분석 도구】\n- 수익성 지표(M210000)\n  - get_single_acnt: 매출액, 영업이익, 순이익 등 핵심 항목 수치 확인\n  - get_single_acc: 손익계산서 세부 항목(매출원가, 판관비 등) 심층 분석\n  - get_disclosure_list: 수익성 급변 요인에 대한 공시자료 확인\n- 안정성 지표(M220000)\n  - get_single_acc: 유동자산, 유동부채, 장기부채 등 항목 세부 분석\n  - get_debt_securities_issued, get_corporate_bond_outstanding: 부채성 증권 발행 및 상환 구조 확인\n  - get_major_holder_changes: 최대주주 변동이 안정성에 미치는 영향 분석\n- 성장성 지표(M230000)\n  - get_single_acc: 3개년 매출, 자산, 순이익 성장 추이 심층 분석\n  - get_disclosure_list: 신규 투자, 인수합병 공시 자료 추적\n- 활동성 지표(M240000)\n  - get_single_acc: 매출채권, 재고자산, 총자산 회전 관련 세부 계정 추적\n  - get_single_acnt: 활동성 지표 관련 요약 계정 분석\n\n【공통 보조 분석 도구】\n- get_corporation_info: 기업 기본정보 및 결산월 확인\n- get_executive_trading: 임원/주요주주 주식매매 패턴 분석\n- get_major_holder_changes: 지배구조 변동 모니터링\n\n【활용 시나리오】\n- 단일 기업의 수익성, 안정성, 성장성, 활동성 종합 진단\n- 3개년 지표 추이를 통한 장기 성장성 및 위험성 평가\n- 수익성 급락, 부채비율 급증 등 이상징후 사전 탐지 및 심층 분석 대상 선정\n- 성장성 높은 기업 선별 후 get_single_acc 기반 성장요인 추적\n- 활동성 악화(회전율 감소) 시 자산운용 효율성 분석 및 개선 필요성 평가\n\n【효과적 활용 방법】\n- idx_cl_code를 명확히 설정하여 목적별 분석(수익성/안정성/성장성/활동성) 집중 조회\n- 지표별 3개년 수치 변화율을 계산하여 CAGR, YoY 분석 적용\n- 이상지표 발견 시, get_single_acc와 get_disclosure_list를 연계하여 세부 원인 심층 추적\n- 기업 투자 타당성, 위험도 평가, 경영진 전략 변동 검토 등에 선제 활용",
    tags={"재무지표", "단일회사", "수익성", "성장성", "활동성", "안정성"}
)
def get_single_index(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    idx_cl_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    단일회사 주요 재무지표 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서 코드 (예: 11011: 사업보고서)
        idx_cl_code (str): 지표분류코드 (M210000: 수익성지표, M220000: 안정성지표, M230000: 성장성지표, M240000: 활동성지표)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2022001
    """
    result = with_context(ctx, "get_single_index", lambda context: context.ds003.get_single_index(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code,
        idx_cl_code=idx_cl_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_multi_index",
    description="상장법인 및 주요 비상장법인이 제출한 연결재무제표를 기반으로, 그룹 전체의 주요 재무지표를 조회하는 도구입니다. 그룹 소속 회사들의 종합 재무건전성, 수익성, 성장성, 활동성 상태를 빠르게 파악할 수 있으며, 그룹 차원의 위험 신호나 성장 동력을 선별하여 심층 분석을 위한 출발점으로 활용됩니다.\n\n【핵심 제공 데이터】\n- 수익성 지표: 매출액영업이익률, 매출액순이익률, ROA, ROE 등\n- 안정성 지표: 부채비율, 유동비율, 비유동비율 등\n- 성장성 지표: 매출액증가율, 총자산증가율, 순이익증가율 등\n- 활동성 지표: 총자산회전율, 매출채권회전율, 재고자산회전율 등\n\n【지표 분류별 연계 분석 도구】\n- 수익성 지표(M210000)\n  - get_single_acnt: 연결 매출액, 영업이익, 순이익 세부 항목 확인\n  - get_single_acc: 매출원가, 판관비 등 세부 손익 항목 추적\n  - get_multi_acnt: 그룹 전체 손익구조 변동 확인\n- 안정성 지표(M220000)\n  - get_multi_acnt: 자산/부채 구조 연결 기준 분석\n  - get_single_acc: 유동자산, 유동부채 항목 세부 분석\n  - get_debt_securities_issued, get_corporate_bond_outstanding: 부채성 증권 발행 내역 확인\n- 성장성 지표(M230000)\n  - get_single_acc: 3개년 매출, 자산, 순이익 성장 추이 분석\n  - get_multi_acnt: 그룹 차원의 성장성 동향 파악\n  - get_disclosure_list: 인수합병, 신사업 진출 공시 추적\n- 활동성 지표(M240000)\n  - get_single_acc: 매출채권, 재고자산 회전 관련 항목 세부 분석\n  - get_single_acnt: 총자산회전율, 재고자산회전율 추출\n  - get_single_index: 활동성 지표 빠른 검토\n\n【공통 보조 분석 도구】\n- get_major_holder_changes: 대주주 변동 탐지\n- get_executive_trading: 임원/주요주주 주식 매도·매수 모니터링\n- get_corporation_info: 계열사 기본정보 및 결산월 확인\n\n【활용 시나리오】\n- 부채비율, 차입금 의존도 상승 등 그룹 재무 리스크 조기 탐지\n- 총자산 증가율, 순이익 증가율 기반 유망 성장 계열사 발굴\n- 영업이익률/순이익률 변동 분석 통한 수익구조 재편 필요성 평가\n- 매출채권회전율/재고자산회전율 분석 통한 자산운용 효율성 진단\n- 지표 급변 기업 식별 후, get_single_acc 및 공시자료 기반 심층 분석\n\n【효과적 활용 방법】\n- idx_cl_code를 정확히 설정하여 수익성/안정성/성장성/활동성별 목표 조회\n- 지표 이상징후 발생 시 종속기업별(get_single_acc) 또는 개별계정(get_single_acnt) 심화 분석 진행\n- 연결재무제표 전반적인 흐름과 종속회사의 위험요소를 체계적으로 파악",
    tags={"재무지표", "다중회사", "수익성", "안정성", "성장성", "활동성"}
)
def get_multi_index(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    idx_cl_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    다중회사 주요 재무지표 조회

    Args:
        corp_code (str): 고유번호 목록
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서 코드 (예: 11011: 사업보고서)
        idx_cl_code (str): 지표분류코드 (M210000: 수익성지표, M220000: 안정성지표, M230000: 성장성지표, M240000: 활동성지표)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2022002
    """
    result = with_context(ctx, "get_multi_index", lambda context: context.ds003.get_multi_index(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code,
        idx_cl_code=idx_cl_code
    ))
    return TextContent(type="text", text=str(result))
