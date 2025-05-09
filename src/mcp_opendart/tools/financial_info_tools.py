import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")

@mcp.tool(
    name="get_single_acnt",
    description="단일 기업의 핵심 재무계정 기반 수익성과 재무건전성 분석",
    tags={"재무제표", "단일회사", "요약계정", "실적분석"}
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
        bsns_year (str): 사업연도 (예: 2025)
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
    description="연결 재무제표 기반 그룹 전체 재무 건전성 및 수익성 구조 분석",
    tags={"재무제표", "그룹분석", "연결재무", "재무건전성"}
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
        bsns_year (str): 사업연도 (예: 2025)
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
#         rcept_no (str): 접수번호 (예: 20250117000238)
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
    description="단일 기업의 전체 XBRL 재무제표 데이터를 기반으로 세부 계정까지 정밀 분석",
    tags={"전체계정", "단일회사", "정밀분석", "XBRL"}
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
        bsns_year (str): 사업연도 (예: 2025)
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
    description="XBRL 재무제표 항목의 표준 계정체계 분석을 통한 IFRS 기반 비교 및 정형화",
    tags={"XBRL", "IFRS", "표준계정", "계정체계"}
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
    description="단일 기업의 수익성, 안정성, 성장성, 활동성 지표 기반 재무 리스크 분석",
    tags={"재무지표", "단일회사", "수익성", "안정성", "성장성", "활동성"}
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
        bsns_year (str): 사업연도 (예: 2025)
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
    description="그룹 단위의 주요 재무지표 분석을 통한 계열사 리스크 및 성장성 평가",
    tags={"재무지표", "다중회사", "그룹분석", "수익성", "안정성", "성장성", "활동성"}
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
        bsns_year (str): 사업연도 (예: 2025)
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
