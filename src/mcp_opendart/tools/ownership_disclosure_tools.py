from typing import Dict, Any, List
from mcp.server.fastmcp import Context

from opendart_mcp.server import mcp

@mcp.tool(
    name="get_major_holder_changes",
    description="주식등의 대량보유상황보고서 내에 대량보유 상황보고 정보를 제공합니다. 반환값에는 보고일자, 보고사유, 소유주식수, 지분율 등의 항목이 포함됩니다."
)
def get_major_holder_changes(ctx: Context, corp_code: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    """
    대량보유 상황보고 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        start_date (Optional[str]): 검색시작일 (예: 20230101)
        end_date (Optional[str]): 검색종료일 (예: 20231231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019021
    """
    return ctx.request_context.lifespan_context.ds004.get_major_holder_changes(
        corp_code=corp_code,
        start_date=start_date,
        end_date=end_date
    )

@mcp.tool(
    name="get_executive_trading",
    description="임원ㆍ주요주주특정증권등 소유상황보고서 내에 임원ㆍ주요주주 소유보고 정보를 제공합니다. 반환값에는 보고일자, 성명, 관계, 소유주식수, 변동사유 등이 포함됩니다."
)
def get_executive_trading(ctx: Context, corp_code: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
    """
    임원ㆍ주요주주 소유보고 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        start_date (Optional[str]): 검색시작일 (예: 20230101)
        end_date (Optional[str]): 검색종료일 (예: 20231231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019022
    """
    return ctx.request_context.lifespan_context.ds004.get_executive_trading(
        corp_code=corp_code,
        start_date=start_date,
        end_date=end_date
    )
