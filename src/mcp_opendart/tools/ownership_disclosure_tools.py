import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")

@mcp.tool(
    name="get_major_holder_changes",
    description="""주식등의 대량보유상황보고서 내에서 특정 기업의 주요 주주(5% 이상 보유자)의 주식 보유 변동 내역을 조회하는 도구입니다.
        주주 지분율의 미세한 변화부터 대규모 지분 이동까지 상세하게 추적할 수 있으며,
        경영권 위협, 내부자 지분 이탈, 적대적 인수 리스크 등을 조기에 감지하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 대표보고자(repror): 주식 보유 주체로서 실제 영향력을 행사하는 주체 식별
        - 보고사유(report_resn): 지분 변동의 원인(신규 취득, 계약 변경, 처분 등) 명시
        - 보유주식 수 및 증감량(stkqy, stkqy_irds): 전체 보유수량과 직전 보고 대비 증감 규모
        - 보유비율 및 증감률(stkrt, stkrt_irds): 전체 발행주식 대비 지분율과 변화율
        - 주요 계약 체결 주식 수 및 비율(ctr_stkqy, ctr_stkrt): 계약 등을 통한 간접적 지배력 행사 여부 파악
        - 보고일자(rcept_dt): 지분 변동 시점 파악에 활용되는 기준일

        【연계 분석 도구】
        - get_executive_trading: 주요 주주가 임원일 경우 내부자거래 여부 병행 분석
        - get_single_acc: 대량 지분 이동 전후의 자본 변동 구조 심층 분석
        - get_disclosure_list: 대량보유보고서 외 다른 주요 공시 병행 추적
        - get_paid_in_capital_increase: 유상증자 이후 대주주 지분율 변화 여부 확인
        - get_free_capital_increase: 무상증자 이후 지배구조 개편 여부 병행 분석

        【활용 시나리오】
        - 동일 대표보고자의 연속 보고에서 지분율 점진적 감소 → 경영권 포기 가능성 시그널
        - 제3자 계약 체결(ctr_stkqy 존재)로 실질적인 지배구조 변화 발생 여부 탐지
        - stkrt_irds가 1% 이상 감소한 경우 → 단기 내 매도세 확산 여부 분석 필요
        - report_resn에 "보유계약 변경" 등 표기된 경우 → 우호/적대적 지분 연합 재편 가능성 분석
        - get_disclosure_list를 통해 동일 시점 공시(이사 변경, 증자 등) 병행 조회하여 배경 추론

        【효과적 활용 방법】
        - stkrt_irds 기준 0.5% 이상 증감 발생 시 LLM이 우선 모니터링 대상으로 분류
        - report_resn 내용에 따라 구조적 매각/매입인지, 일회성인지 분류하여 리스크 평가
        - ctr_stkrt와 stkrt의 차이를 분석하여 계약 기반 지분과 실보유 지분을 구분
        - 지분 감소 구간과 get_executive_trading을 병행 분석하여 내부자 이탈 탐지

        【주의사항 및 팁】
        - 지분율 감소가 있어도 보고사유에 "보유계약 변경"만 있는 경우, 실제 매도 없이 계약 전환일 수 있음
        - 복수의 보고서가 동일일자에 접수된 경우, stkqy_irds 누적합을 기준으로 실제 변화량 판단
        - 5% 미만으로 하락할 경우 보고 의무가 사라지므로, 마지막 보고 이후 추가 매도 가능성 존재
        """,
    tags={"대량보유상황보고서", "대량보유", "상황보고", "주식등"}
)
def get_major_holder_changes(
    corp_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    대량보유 상황보고 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        start_date (Optional[str]): 검색시작일 (예: 20240101)
        end_date (Optional[str]): 검색종료일 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019021
    """
    result = with_context(ctx, "get_major_holder_changes", lambda context: context.ds004.get_major_holder_changes(
        corp_code=corp_code,
        start_date=start_date,
        end_date=end_date
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_executive_trading",
    description="""상장법인 및 주요 비상장법인이 제출한 임원ㆍ주요주주 특정증권등 소유상황보고서를 조회하는 도구입니다. 
        임원 및 주요주주의 보유 지분 변동 내역을 통해 내부자 거래 패턴, 지배구조 변화 가능성, 경영진의 기업 전망 인식을 분석할 수 있습니다.

        【핵심 제공 데이터】
        - 보고자(repror): 실제 보고의 주체로, 내부자 거래 여부 식별
        - 발행회사 관계 및 직위(isu_exctv_rgist_at, isu_exctv_ofcps): 보고자가 등기임원 또는 대표이사인지 여부로 판단 가능
        - 주요 주주 여부(isu_main_shrholdr): 10% 이상 보유자 등 주요 주주의 행위 여부 분석
        - 특정 증권 소유 수 및 증감(sp_stock_lmp_cnt, sp_stock_lmp_irds_cnt): 보유 주식 수와 증감량으로 지분 이동 규모 파악
        - 소유 비율 및 증감 비율(sp_stock_lmp_rate, sp_stock_lmp_irds_rate): 지배력 변화 가능성 조기 탐지
        - 공시 접수일자(rcept_dt): 거래 시점의 외부 이벤트와 교차 분석 가능

        【연계 분석 도구】
        - get_major_holder_changes: 지분율 변화가 보고된 주요 주주의 행동과 일치 여부 확인
        - get_disclosure_list: 해당 시기 공시 전체 흐름 속 내부자 거래 분석
        - get_single_acc: 대규모 주식 매각 이전/이후의 자본 구조 변동 분석

        【활용 시나리오】
        - 대표이사 또는 등기임원의 대규모 지분 매각 → 내부 부정적 전망 인식 가능성 평가
        - sp_stock_lmp_irds_rate가 ±1% 이상일 경우, 내부자 거래로 인한 정보 비대칭성 의심
        - isu_main_shrholdr=O && sp_stock_lmp_irds_cnt<0 → 경영권 리스크, 방어 전략 필요성 점검
        - rcept_dt를 기준으로 30일 이내 공시(get_disclosure_list) 병행 분석 → 정보 이용 가능성 탐지

        【효과적 활용 방법】
        - 등기임원 또는 주요주주의 거래 내역만 필터링하여 분석 우선순위 설정
        - 증감 비율(sp_stock_lmp_irds_rate)이 연속적으로 나타나는 경우, 구조적 매각/매입 여부 판단
        - get_major_holder_changes와 병행 분석 시, 계약 기반 지분 변화와의 연계성 확인
        - get_single_acc 분석을 통해 내부자 거래 이후 자산·부채 구조 변화 유무 점검

        【주의사항 및 팁】
        - 증감 수량이 존재하더라도 보고자가 비등기/비주요주주일 경우 리스크 판단에서 제외 가능
        - 동일 시기 복수 공시 존재 시, 내부자 거래가 기업 이벤트(증자, 합병 등)와 관련되는지 병행 검토 필수
        """,
    tags={"임원주요주주", "소유상황보고서", "소유보고", "임원주요주주"}
)
def get_executive_trading(
    corp_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    임원ㆍ주요주주 소유보고 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        start_date (Optional[str]): 검색시작일 (예: 20240101)
        end_date (Optional[str]): 검색종료일 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019022
    """
    result = with_context(ctx, "get_executive_trading", lambda context: context.ds004.get_executive_trading(
        corp_code=corp_code,
        start_date=start_date,
        end_date=end_date
    ))
    return TextContent(type="text", text=str(result))
