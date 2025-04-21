from typing import Dict, Any, List
from mcp.server.fastmcp import Context

from opendart_mcp.server import mcp

@mcp.tool()
def get_corporation_code_by_name(ctx: Context, corp_name: str) -> Dict[str, Any]:
    """기업명으로 고유번호 검색
    
    Args:
        corp_name (str): 회사명
        
    Returns:
        Dict[str, Any]: 검색 결과 (status, message, list)
    """
    return ctx.request_context.lifespan_context.ds001.get_corporation_code_by_name(corp_name)

@mcp.tool()
def get_disclosure_list(ctx: Context, corp_code: str, bgn_de: str, end_de: str) -> Dict[str, Any]:
    """공시 검색
    
    Args:
        corp_code (str): 고유번호
        bgn_de (str): 시작일 (YYYYMMDD)
        end_de (str): 종료일 (YYYYMMDD)
        
    Returns:
        Dict[str, Any]: 검색 결과 (status, message, list)
    """
    return ctx.request_context.lifespan_context.ds001.get_disclosure_list(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    )

@mcp.tool()
def get_corporation_info(ctx: Context, corp_code: str) -> Dict[str, Any]:
    """기업개황 조회
    
    Args:
        corp_code (str): 고유번호
        
    Returns:
        Dict[str, Any]: 기업 정보 (status, message, corp_name, corp_name_eng, stock_name, stock_code, ceo_nm, etc...)
    """
    return ctx.request_context.lifespan_context.ds001.get_corporation_info(corp_code)

@mcp.tool()
def get_disclosure_document(ctx: Context, rcp_no: str) -> Dict[str, Any]:
    """공시서류원본파일 조회
    
    Args:
        rcp_no (str): 접수번호
        
    Returns:
        Dict[str, Any]: 문서 정보 (status, message, url)
    """
    return ctx.request_context.lifespan_context.ds001.get_disclosure_document(rcp_no)

@mcp.tool()
def get_corporation_code(ctx: Context) -> Dict[str, Any]:
    """고유번호 조회 및 저장
    
    전체 고유번호 목록을 조회하고 로컬에 저장합니다.
    이 작업은 서버 시작 시 자동으로 수행되므로, 일반적으로 이 툴을 직접 호출할 필요는 없습니다.
    
    Returns:
        Dict[str, Any]: 결과 (status, message, path)
    """
    return ctx.request_context.lifespan_context.ds001.get_corporation_code() 