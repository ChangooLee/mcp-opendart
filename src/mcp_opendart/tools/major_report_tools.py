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

 