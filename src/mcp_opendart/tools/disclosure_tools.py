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
    description="""기업의 모든 공시 내역을 날짜별로 검색하여 기업 활동의 타임라인을 체계적으로 파악할 수 있는 핵심 도구입니다.  
        정기보고서, 주요사항보고서, 지분변동 등 모든 유형의 공시를 망라하여, 경영활동, 재무현황, 지배구조 변화 등 기업 리스크 요인을 신속하게 모니터링할 수 있습니다.

        【핵심 제공 데이터】
        - corp_cls: 법인구분 (Y: 유가증권시장, K: 코스닥, N: 코넥스, E: 기타)
        - corp_name: 종목명 또는 법인명
        - corp_code: 공시대상회사의 고유번호(8자리)
        - stock_code: 상장회사의 종목코드(6자리)
        - report_nm: 보고서명 (정정, 첨부추가, 변경등록 등 상태표시 포함)
        - rcept_no: 접수번호(14자리) — 공시 원문 조회에 필수
        - flr_nm: 공시 제출인명 (기업명 또는 개인명)
        - rcept_dt: 공시 접수일자 (YYYYMMDD)
        - rm: 비고 (공시의 추가 속성: 유, 코, 채, 넥, 공, 연, 정, 철)

        【페이징 관련 데이터】
        - page_no: 현재 페이지 번호
        - page_count: 페이지당 건수
        - total_count: 총 조회 건수
        - total_page: 총 페이지 수

        【주요 활용 시나리오】
        - 지정 기간 동안 기업의 전체 공시 이력 추적
        - 정기보고서(사업/분기/반기) 및 주요사항보고서 접수번호 확보
        - 인수합병(M&A), 유상증자, 지분변동 등 기업 이벤트 조기 감지
        - 정정공시, 철회공시 등 비정상 이벤트 모니터링
        - IR, 실적발표 등 투자 관련 공시 일자 파악

        【효과적 활용 방법】
        - report_nm의 상태 태그(기재정정, 첨부정정 등) 분석으로 정정 공시 여부 확인
        - rm(비고) 항목 분석으로 유가/코스닥/코넥스 소속 시장 구분 및 연결 재무정보 포함 여부 판단
        - rcept_no를 기반으로 상세 공시(API 호출 또는 웹 링크) 조회 및 후속 심층 분석
        - 최근 접수일자(rcept_dt) 기준 최신 공시 흐름 파악 및 리스크 사전 인지

        【주의사항 및 팁】
        - report_nm에 [정정명령부과], [정정제출요구] 태그가 포함된 경우, 기업 리스크 징후로 해석할 수 있으므로 별도 주의
        - rm 항목 중 '정', '철' 플래그가 있는 경우, 해당 보고서의 원본 또는 철회 사유를 추가로 검토하는 것이 필요
        - 페이지별 조회(page_no, page_count) 시 최대 10,000건까지 검색 가능하므로 대량 데이터 처리시 적절한 페이징 전략 필요
        """,
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
    description="""기업의 핵심 프로필과 지배구조 분석에 필요한 기초 정보를 제공하는 도구입니다.  
        대표이사 특수관계인 확인, 결산 시기 파악, 상장 상태 등 기업 분석의 시작점이 되는 정보를 통합 제공합니다.

        【핵심 분석 요소】
        - 대표자명(ceo_nm): 대표이사가 최대주주나 특수관계인인지 확인하는 기준 정보
        - 결산월(acc_mt): 정기보고서 공시 예상 시기 파악에 필수 (예: 12월 결산 → 다음해 3월 사업보고서 공시)
        - 법인구분(corp_cls): 상장 여부 및 시장구분 확인 (Y: 유가증권, K: 코스닥, N: 코넥스, E: 기타)
        - 설립일(est_dt): 기업 업력 및 성장 단계 파악에 활용
        - 업종코드(induty_code): 기업 산업 분류 참고 (※참고용으로만 활용 가능)
        - 종목명(stock_name), 종목코드(stock_code): 상장사 여부 및 시장내 식별 용이성 확보
        - 주소(adres), 홈페이지(hm_url), IR홈페이지(ir_url): 기업 정보 접근성 확인
        - 법인등록번호(jurir_no), 사업자등록번호(bizr_no): 기업의 공식 등록 정보 파악

        【지배구조 분석 활용법】
        - 대표이사명(ceo_nm)과 get_major_shareholder 결과 비교로 오너경영 여부 파악
        - 대표이사 지분변동은 get_executive_trading으로 추적하여 내부자 거래 패턴 분석
        - 동일인 또는 계열사 간 지분 관계 파악을 위한 기초 정보로 활용

        【공시 일정 계획】
        - 결산월(acc_mt) 기준 정기보고서 예상 공시일 계산:
        - 사업보고서: 결산월 + 90일 이내
        - 분기보고서: 분기 종료 후 45일 이내
        - 반기보고서: 반기 종료 후 45일 이내
        - 결산발표 시즌에 get_disclosure_list로 집중 모니터링 계획 수립

        【주의사항 및 한계】
        - 업종코드(induty_code)는 조회용으로만 제공되며, 이를 기반으로 직접 동종업계 기업을 검색할 수 없음
        - 동일 업종 기업 비교를 위해 별도 산업분류 체계 또는 수동 리스트 작성 필요
        - 대표자명(ceo_nm), 주소(adres), 전화번호(phn_no), 팩스번호(fax_no) 등은 변경 가능성이 있으므로 get_disclosure_list로 최신 공시 병행 확인 권장

        【추가 정보 획득 경로】
        - 상세 재무정보: get_single_acnt 또는 get_single_acc 호출
        - 지분구조 분석: get_major_shareholder, get_executive_trading 도구 활용
        - 배당정책 확인: get_dividend_info를 통해 배당성향 파악
        - 경영진 변동 확인: get_disclosure_list를 통해 '대표이사 변경' 공시 모니터링""",
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
