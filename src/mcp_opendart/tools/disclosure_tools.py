import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context
logger = logging.getLogger("mcp-opendart")

@mcp.tool(
    name="get_corporation_code_by_name",
    description="기업명을 이용하여 기업 고유번호를 조회합니다. 공시조회를 위해 가장 먼저 실행하여 고유번호를 얻어야 합니다.",
    tags={"기업검색", "고유번호", "기업기초정보", "기업식별"}
)
async def get_corporation_code_by_name(
    corp_name: str,
    ctx: Optional[Any] = None,
) -> TextContent:
    result = with_context(ctx, "get_corporation_code_by_name", lambda context: context.ds001.get_corporation_code_by_name(corp_name))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_disclosure_list",
    description="기업의 모든 공시 내역을 날짜별로 검색하여 기업 활동의 타임라인을 파악할 수 있는 핵심 도구입니다. 주요 공시, 재무 보고서, 지분 변동 등 투자 의사결정에 필수적인 공시 정보의 목록과 접근 경로를 제공합니다.\n\n【핵심 기능】\n- 지정 기간 내 기업의 모든 공시 내역 조회 (최대 10,000건)\n- 최신순 정렬로 최근 중요 이벤트 우선 확인 가능\n- 정기보고서, 주요사항보고서, 지분변동 등 모든 유형의 공시 포함\n- 각 공시의 고유 접수번호(rcept_no) 제공으로 상세 정보 조회 가능\n\n【입력 파라미터】\n- corp_code: 기업 고유번호 (8자리, get_corporation_code_by_name으로 획득)\n- bgn_de: 조회 시작일 (YYYYMMDD 형식, 예: 20250101)\n- end_de: 조회 종료일 (YYYYMMDD 형식, 예: 20250430)\n\n【반환 데이터】\n- report_nm: 공시/보고서 종류 (예: 분기보고서, 주요사항보고서 등)\n- rcept_no: 공시 접수번호 (다른 API 호출에 필요한 고유 식별자)\n- flr_nm: 공시 제출자 (기업명 또는 개인명)\n- rcept_dt: 공시 접수일자 (YYYYMMDD 형식)\n- rm: 정정여부 표시 ('유'는 정정공시를 의미)\n\n【주요 활용 시나리오】\n- 기업의 최근 주요 이벤트 및 전략 변화 추적\n- 정기보고서(사업, 분기, 반기) 접수번호 확인 후 재무정보 상세 조회\n- 지분변동, 경영진 변경 등 기업지배구조 변화 모니터링\n- 기업설명회(IR), 실적발표 등 투자 관련 일정 확인\n- 인수합병, 유상증자 등 주가 영향 이벤트 조기 파악\n\n【조회 전략】\n- 최근 30일: 단기 중요 이벤트 파악\n- 분기 단위(3개월): 정기보고서 및 실적 관련 공시 확인\n- 1년 단위: 기업의 장기적 변화 및 전략 파악\n- 특정 이벤트 전후: 중요 사건 전후의 관련 공시 확인\n\n【후속 분석을 위한 연계 활용】\n- 정기보고서 발견 시 get_single_acnt로 재무제표 상세 분석\n- 지분변동 공시 발견 시 get_major_holder_changes로 주요 주주 변동 추적\n- 주요사항보고서 발견 시 해당 유형별 상세 API 호출(get_merger, get_capital_reduction 등)",
    tags={"공시리스트", "보고서목록", "기업이슈", "중대사건", "타임라인"}
)
def get_disclosure_list(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    공시 목록 조회

    Args:
        corp_code (str): 공시대상회사의 고유번호 (8자리)
        bgn_de (str): 조회 시작일 (YYYYMMDD)
        end_de (str): 조회 종료일 (YYYYMMDD)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001
    """
    result = with_context(ctx, "get_disclosure_list", lambda context: context.ds001.get_disclosure_list(corp_code, bgn_de, end_de))
    return TextContent(type="text", text=str(result))


@mcp.tool(
    name="get_corporation_info",
    description="기업의 핵심 프로필과 지배구조 분석에 필요한 기초 정보를 제공하는 도구입니다. 대표이사 특수관계인 확인, 결산 시기 파악, 상장 상태 등 기업 분석의 시작점이 되는 정보를 통합 제공합니다.\n\n【핵심 분석 요소】\n- 대표이사 정보(ceo_nm): 대표이사가 최대주주나 특수관계인인지 확인하는 기준점\n- 결산월(acc_mt): 정기보고서 공시 예상 시기 파악에 필수 (예: 12월 결산 → 다음해 3월 사업보고서 공시)\n- 법인구분(corp_cls): 상장 여부 및 시장구분 확인 (Y:유가증권, K:코스닥, N:비상장)\n- 설립일(est_dt): 기업 업력 및 성장 단계 파악에 활용\n- 업종코드(induty_code): 기업의 산업 분류 참고 (※참고용으로만 활용 가능)\n\n【지배구조 분석 활용법】\n- 대표이사명(ceo_nm)과 get_major_shareholder 결과 비교로 오너경영 여부 파악\n- 대표이사의 지분변동은 get_executive_trading으로 추적하여 경영진 매매 패턴 분석\n- 동일인 또는 계열사 간 지분 관계 파악을 위한 기초 정보로 활용\n\n【공시 일정 계획】\n- 결산월(acc_mt) 기준으로 정기보고서 예상 공시일 계산:\n  - 사업보고서: 결산월 + 90일 이내\n  - 분기보고서: 분기 종료 후 45일 이내\n  - 반기보고서: 반기 종료 후 45일 이내\n- 결산발표 시즌에 get_disclosure_list로 집중 모니터링 계획 수립\n\n【주의사항 및 한계】\n- 업종코드(induty_code)는 조회용으로만 제공되며, 이 코드로 다른 API에서 동종업계 기업을 검색할 수 없음\n- 동일 업종 기업 파악을 위해서는 별도의 산업 분류 자료를 참고하거나 수동으로 기업 리스트 작성 필요\n- 대표이사 정보는 변경될 수 있으므로 최신 공시(get_disclosure_list)를 통해 현재 경영진 확인 권장\n\n【추가 정보 획득 경로】\n- 상세 재무정보: get_single_acnt, get_single_acc 도구 활용\n- 지분구조 분석: get_major_shareholder, get_executive_trading 도구 활용\n- 배당정책 확인: get_dividend_info 도구로 배당 성향 파악\n- 경영진 변동 확인: get_disclosure_list에서 '대표이사 변경' 공시 검색",
    tags={"기업기초정보", "기업개요", "회사정보"}
)
def get_corporation_info(
    corp_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    기업 개황정보 조회

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019002
    """
    result = with_context(ctx, "get_corporation_info", lambda context: context.ds001.get_corporation_info(corp_code))
    return TextContent(type="text", text=str(result))


# @mcp.tool(
#     name="get_disclosure_document",
#     description="접수번호(rcp_no)를 이용하여 공시서류 원본파일(XML)의 다운로드 정보를 조회합니다.",
#     tags={"공시서류", "원본파일", "다운로드", "XML"}
# )
# def get_disclosure_document(
#     rcp_no: str,
#     ctx: Optional[Any] = None
# ) -> TextContent:
#     """
#     공시서류 원본파일 조회
# 
#     Args:
#         rcp_no (str): 공시서류의 접수번호 (14자리)
# 
#     참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019003
#     """
#     result = with_context(ctx, "get_disclosure_document", lambda context: context.ds001.get_disclosure_document(rcp_no))
#     return TextContent(type="text", text=str(result))


@mcp.tool(
    name="get_corporation_code",
    description="OpenDART에서 제공하는 모든 공시대상 회사의 고유번호 전체 목록(XML 파일)을 조회합니다. 기업명 검색 또는 고유번호 매핑에 사용됩니다.",
    tags={"기업전체목록", "고유번호전체", "기업식별", "코드매핑"}
)
def get_corporation_code(
    ctx: Optional[Any] = None
) -> TextContent:
    """
    고유번호 목록 조회

    Returns:
        Dict[str, Any]: 고유번호 목록 (기업명, 고유번호, 종목코드 등 포함)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018
    """
    result = with_context(ctx, "get_corporation_code", lambda context: context.ds001.get_corporation_code())
    return TextContent(type="text", text=str(result))
