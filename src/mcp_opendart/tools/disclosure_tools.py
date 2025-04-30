import logging, datetime
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context
from mcp_opendart.registry.initialize_registry import initialize_registry

logger = logging.getLogger("mcp-opendart")
tool_registry = initialize_registry()

@mcp.tool(
    name="get_opendart_tool_info",
    description="기업의 심층 분석을 위해 mcp 도구의 이름을 정확히 입력하여 도구의 목적, 활용 흐름, 필수 파라미터, 연관 도구 등을 확인 후 진행, 예: get_opendart_tool_info(tool_name='get_corporation_info')",
    tags={"심층분석", "기업분석", "도구흐름"}
)
async def get_opendart_tool_info(
    tool_name: str,
) -> TextContent:
    tool = tool_registry.get_tool(tool_name)
    if not tool:
        return TextContent(type="text", text=f"❌ '{tool_name}'이라는 이름의 도구를 찾을 수 없습니다.")

    # 파라미터 설명 추출
    param_lines = []
    props = tool.parameters.get("properties", {})
    for param, meta in props.items():
        desc = meta.get("description", "")
        param_lines.append(f"- {param}: {desc}")

    # linked 도구 리스트
    linked = tool.linked_tools or []
    linked_str = ", ".join(linked) if linked else "(연관 도구 없음)"

    # 현재 날짜
    today = datetime.date.today().strftime("%Y-%m-%d")

    # 응답 생성
    text = f"""
        📌 {tool.name} ({tool.korean_name or '도구명 미정'})

        이 도구는 특정 기업의 "{tool.name}"을(를) 다음과 같은 파라미터를 이용하여 조회할 수 있습니다:
        {chr(10).join(param_lines)}

        날짜가 필요한 경우, 반드시 시스템 기준일({today})을 기준으로 조회를 시작해야 합니다.

        이 정보를 바탕으로, 사용자는 다음과 같은 흐름으로 도구를 활용할 수 있습니다:

        1. 먼저 get_corporation_code_by_name 도구를 통해 기업명을 고유번호로 변환합니다.
        2. {tool.name}을 사용해 관련 정보를 조회합니다.
        3. 연관된 다음 도구를 반드시 확인해야 합니다:
        {linked_str}

        이 도구는 정보 흐름의 중심 축으로 활용되며, 다른 도구들과 결합되어 기업 리스크 분석에 핵심적인 역할을 합니다.
        """

    return TextContent(type="text", text=text.strip())

@mcp.tool(
    name="get_corporation_code_by_name",
    description="기업명을 이용하여 기업 고유번호 조회, 공시조회를 위해 가장 먼저 실행하여 고유번호를 얻어야 함",
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
    description="지정 기간 내 공시 접수 목록을 조회하여 기업 활동의 주요 이벤트 발생 여부 탐색",
    tags={"공시", "목록", "접수내역", "이벤트탐지"}
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
    description="대표자, 결산월, 상장상태 등 기업 기본 정보 기반 지배구조 및 공시 일정 분석",
    tags={"기업기초정보", "지배구조", "공시일정", "대표자분석", "가족경영"}
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
