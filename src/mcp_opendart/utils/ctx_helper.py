import logging
from typing import Any, Callable, Optional

from mcp_opendart.server import opendart_context

logger = logging.getLogger("mcp-opendart")

def with_context(
    ctx: Optional[Any],
    tool_name: str,
    fallback_func: Callable[[Any], Any]
) -> Any:
    """
    MCP context를 안전하게 처리하며, fallback으로 전역 컨텍스트 사용.

    Args:
        ctx: MCPContext or None
        tool_name: 도구명 (로깅용)
        fallback_func: context.ds001.get_something 등 context 의존 로직

    Returns:
        fallback_func 실행 결과
    """
    logger.info(f"📌 Tool: {tool_name} 호출됨")

    if ctx is not None:
        try:
            result = fallback_func(ctx.request_context.lifespan_context)
            logger.info("✅ MCP 내부 컨텍스트 사용")
            return result
        except Exception as e:
            logger.warning(f"⚠️ MCPContext 접근 실패: {e}")

    logger.warning("⚠️ Fallback 전역 컨텍스트 사용")
    return fallback_func(opendart_context)
