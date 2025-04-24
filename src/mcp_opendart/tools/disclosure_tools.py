from typing import Dict, Any, List, Optional, cast
from mcp.server.fastmcp import Context
from mcp_opendart.server import OpenDartContext, mcp

@mcp.tool()
def get_corporation_code_by_name(ctx: Context[OpenDartContext, Any], corp_name: str) -> Dict[str, Any]:
    """기업명으로 고유번호 검색
    
    Args:
        corp_name (str): 회사명
        
    Returns:
        Dict[str, Any]: 검색 결과 (status, message, list)
    """
    return cast(Dict[str, Any], ctx.request_context.lifespan_context.ds001.get_corporation_code_by_name(corp_name))

@mcp.tool(
    name="get_disclosure_list",
    description="지정한 회사의 고유번호와 기간을 기준으로 공시목록(보고서)을 조회합니다. 보고서 종류, 접수번호, 제출일자 등의 정보를 포함하며, 최신 보고서부터 최대 10,000건까지 검색 가능합니다."
)
def get_disclosure_list(ctx: Context[OpenDartContext, Any], corp_code: str, bgn_de: str, end_de: str) -> Dict[str, Any]:
    """
    공시 목록 조회

    Args:
        corp_code (str): 공시대상회사의 고유번호 (8자리)
        bgn_de (str): 조회 시작일 (YYYYMMDD)
        end_de (str): 조회 종료일 (YYYYMMDD)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001
    """
    return cast(Dict[str, Any], ctx.request_context.lifespan_context.ds001.get_disclosure_list(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))


@mcp.tool(
    name="get_corporation_info",
    description="기업의 고유번호를 입력받아 해당 기업의 개황정보를 조회합니다. 반환되는 정보에는 회사명, 대표자명, 법인구분, 주소, 전화번호, 홈페이지 주소 등이 포함됩니다."
)
def get_corporation_info(ctx: Context[OpenDartContext, Any], corp_code: str) -> Dict[str, Any]:
    """
    기업 개황정보 조회

    Args:
        corp_code (str): 공시대상회사의 고유번호(8자리)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019002
    """
    return cast(Dict[str, Any], ctx.request_context.lifespan_context.ds001.get_corporation_info(
        corp_code=corp_code
    ))


@mcp.tool(
    name="get_disclosure_document",
    description="접수번호(rcp_no)를 이용하여 공시서류 원본파일(XML)의 다운로드 정보를 조회합니다."
)
def get_disclosure_document(ctx: Context[OpenDartContext, Any], rcp_no: str) -> Dict[str, Any]:
    """
    공시서류 원본파일 조회

    Args:
        rcp_no (str): 공시서류의 접수번호 (14자리)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019003
    """
    return cast(Dict[str, Any], ctx.request_context.lifespan_context.ds001.get_disclosure_document(
        rcp_no=rcp_no
    ))


@mcp.tool(
    name="get_corporation_code",
    description="OpenDART에서 제공하는 모든 공시대상 회사의 고유번호 전체 목록(XML 파일)을 조회합니다. 기업명 검색 또는 고유번호 매핑에 사용됩니다."
)
def get_corporation_code(ctx: Context[OpenDartContext, Any]) -> Dict[str, Any]:
    """
    고유번호 목록 조회

    Returns:
        Dict[str, Any]: 고유번호 목록 (기업명, 고유번호, 종목코드 등 포함)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018
    """
    return cast(Dict[str, Any], ctx.request_context.lifespan_context.ds001.get_corporation_code())
