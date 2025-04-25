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
    description="지정한 회사의 고유번호와 기간을 기준으로 공시목록(보고서)을 조회합니다. 보고서 종류, 접수번호, 제출일자 등의 정보를 포함하며, 최신 보고서부터 최대 10,000건까지 검색 가능합니다.",
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
    description="기업의 고유번호를 입력받아 해당 기업의 개황정보를 조회합니다. 반환되는 정보에는 회사명, 대표자명, 법인구분, 주소, 전화번호, 홈페이지 주소 등이 포함됩니다.",
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


@mcp.tool(
    name="get_disclosure_document",
    description="접수번호(rcp_no)를 이용하여 공시서류 원본파일(XML)의 다운로드 정보를 조회합니다.",
    tags={"공시서류", "원본파일", "다운로드", "XML"}
)
def get_disclosure_document(
    rcp_no: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    공시서류 원본파일 조회

    Args:
        rcp_no (str): 공시서류의 접수번호 (14자리)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019003
    """
    result = with_context(ctx, "get_disclosure_document", lambda context: context.ds001.get_disclosure_document(rcp_no))
    return TextContent(type="text", text=str(result))


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
