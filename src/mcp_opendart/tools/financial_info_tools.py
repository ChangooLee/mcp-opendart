import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")
@mcp.tool(
    name="get_single_acnt",
    description="상장법인 및 주요 비상장법인이 제출한 정기보고서 내에 XBRL재무제표의 주요계정과목을 제공합니다. 반환값에는 계정명, 당기금액, 전기금액, 계정과목코드, 재무제표구분 등이 포함됩니다.",
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
    description="상장법인 및 주요 비상장법인이 제출한 정기보고서 내에 XBRL재무제표의 주요계정과목을 제공합니다. 대상법인 복수조회가 가능합니다. 반환값에는 법인명, 계정명, 당기금액, 전기금액, 재무제표구분 등이 포함됩니다.",
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
        corp_code (str): 고유번호 목록 (콤마로 구분된 복수의 8자리 문자열)
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

@mcp.tool(
    name="get_xbrl_file",
    description="상장법인 및 주요 비상장법인이 제출한 정기보고서 내에 XBRL재무제표의 원본파일(XBRL)을 제공합니다. 반환값에는 XBRL 압축파일의 저장 경로 및 다운로드 상태 정보가 포함됩니다.",
    tags={"XBRL", "원본파일", "첨부파일", "정기보고서"}
)
def get_xbrl_file(
    rcept_no: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    재무제표 원본파일(XBRL) 다운로드

    Args:
        rcept_no (str): 접수번호 (예: 20240117000238)
        reprt_code (str): 보고서 코드 (11011: 사업보고서, 11012: 반기보고서 등)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019019
    """
    result = with_context(ctx, "get_xbrl_file", lambda context: context.ds003.get_xbrl_file(
        rcept_no=rcept_no,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_single_acc",
    description="상장법인 및 주요 비상장법인이 제출한 정기보고서 내에 XBRL재무제표의 모든계정과목을 제공합니다. 반환값에는 계정명, 재무제표구분, 당기/전기 금액, 계정과목코드 등이 포함됩니다.",
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
    description="금융감독원 회계포탈에서 제공하는 IFRS 기반 XBRL 재무제표 공시용 표준계정과목체계를 제공합니다. 반환값에는 표준계정명, 계정코드, 순서, 국문/영문 계정명이 포함됩니다.",
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
    description="상장법인 및 주요 비상장법인이 제출한 정기보고서 내에 XBRL재무제표의 주요 재무지표를 제공합니다. 반환값에는 지표명, 당기/전기 값, 지표분류, 지표코드 등이 포함됩니다.",
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
    description="다중회사 상장법인 및 주요 비상장법인이 제출한 정기보고서 내에 XBRL재무제표의 주요 재무지표를 제공합니다. 대상법인 복수조회가 가능합니다. 반환값에는 법인명, 지표명, 당기/전기 값, 지표코드 등이 포함됩니다.",
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
        corp_code (str): 고유번호 목록 (콤마로 구분된 복수의 8자리 문자열)
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
