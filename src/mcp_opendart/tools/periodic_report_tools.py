import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")

@mcp.tool(
    name="get_stock_increase_decrease",
    description="""지정한 기업의 정기보고서 내 주식발행 관련 내역(증자·감자)을 조회하는 도구입니다. 
        발행주식 수의 증가 또는 감소 내역을 통해 자본금 변화, 기업의 지배구조 재편 가능성, 경영진의 재무 전략 방향을 파악할 수 있습니다.

        【핵심 제공 데이터】
        - isu_dcrs_de (발행 감소일자): 실제 증자·감자 실행일로, 자본금 변동 시점 판단
        - isu_dcrs_stle (발행 감소 형태): 소각, 병합, 감자 등 주식 감소 방식 명시
        - isu_dcrs_stock_knd (감자 주식 종류): 보통주, 우선주 등 감자 대상 주식 종류 파악
        - isu_dcrs_qy (감자 수량): 감소된 주식 수량으로 자본 구조 변화 규모 평가
        - isu_dcrs_mstvdv_fval_amount (주당 액면가): 감자 대상 주식의 액면가 확인
        - stlm_dt (결산기준일): 분석 기준 시점 설정

        【연계 분석 도구】
        - get_single_acc: 감자 이후 자산·자본 변동 여부 정밀 분석
        - get_disclosure_list: 감자와 관련된 추가 공시 또는 후속 조치 확인
        - get_major_holder_changes: 감자 이후 주요 주주 지분율 변화 여부 점검
        - get_executive_trading: 감자 시점 임원 지분매매 여부 병행 분석

        【활용 시나리오】
        - 감자 형태가 '무상감자'인 경우 → 누적 결손금 보전 목적일 가능성 평가
        - isu_dcrs_qy 값이 클 경우 → 자본잠식 해소 시도 혹은 주가 부양 목적 의심
        - get_major_holder_changes 병행 시, 감자 후 지배구조 개편 여부 확인
        - get_single_acc와 비교하여 자본금 감소가 재무제표에 미친 영향 분석
        - 감자 직후 get_disclosure_list로 유상증자 또는 경영진 교체 공시 병행 분석

        【효과적 활용 방법】
        - isu_dcrs_qy를 기존 총발행주식수와 비교하여 감자 비율 산출
        - isu_dcrs_stle에 따른 감자 목적 구분 (예: 병합 → 소액주주 정리 가능성)
        - stlm_dt 기준 1개월 이내 다른 공시와의 교차 분석으로 연속된 자본정책 흐름 파악
        - 감자일자 이후 get_executive_trading으로 내부자 주식거래 변화 감지

        【주의사항 및 팁】
        - 감자와 증자는 보고서 기준으로 확인되며, 실제 이사회 결의 및 실행일과 차이가 있을 수 있음
        - 감자 방식이 비정상적일 경우 투자자 보호 이슈나 소송 가능성도 존재하므로 get_disclosure_list로 병행 확인 필요
        """,
    tags={"증자", "감자", "주식발행", "변경"}
)
def get_stock_increase_decrease(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    증자(감자) 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019004
    """
    result = with_context(ctx, "get_stock_increase_decrease", lambda context: context.ds002.get_stock_increase_decrease(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_dividend_info",
    description="""지정한 기업의 정기보고서 내 배당에 관한 사항을 조회하는 도구입니다. 
        배당금 총액, 배당성향, 시가배당률 등을 통해 경영진의 이익 분배 전략, 재무 건전성, 미래 투자 여력 등을 종합적으로 평가할 수 있습니다. 과도한 배당은 유동성 리스크로, 반대로 무배당 지속은 수익성 약화나 재무 악화 신호로 해석될 수 있습니다.

        【핵심 제공 데이터】
        - dvdn_bas_amt (배당기준일): 배당 권리 확정 시점 파악
        - cash_dvdn_amt (현금배당총액): 현금 유출 규모를 통한 유동성 분석
        - cash_dvdn_rate (주당 현금배당금): 이익 환원의 실질 규모 평가
        - stbd_vs_dvdn_rt (시가배당률): 시장 주가 대비 배당수익률로, 배당 정책의 투자 매력도 분석
        - earn_vs_dvdn_rt (배당성향): 순이익 대비 배당 비율로 재투자 여력 또는 과도한 배당 여부 판단
        - rcept_no (접수번호): 배당 정보의 출처 추적

        【연계 분석 도구】
        - get_single_acc: 당기순이익과 비교하여 배당 여력 검토
        - get_disclosure_list: 동일 결산기에 발표된 다른 공시와 병행 분석 (예: 감자, 유상증자 등)
        - get_treasury_stock: 자사주 보유 후 배당률 조정 여부 분석
        - get_major_shareholder: 최대주주 배당 수혜 규모 추정
        - get_executive_trading: 배당기준일 직전 임원 지분변동 여부로 내부 정보 거래 감지

        【활용 시나리오】
        - 배당성향이 100% 초과 → 순이익보다 많은 배당으로 현금 유출 압박 가능성
        - 시가배당률이 급등 또는 급락 → 배당정책 변경 신호 또는 일시적 실적 착시 가능성 분석
        - get_single_acc와 비교하여 영업현금흐름이 마이너스 상태에서 고배당 → 지속 불가능한 배당정책 가능성 탐지
        - get_disclosure_list와 병행 분석하여 감자 또는 증자와 같은 자본 정책 변화 병행 여부 확인
        - 동일 결산기의 배당 결정과 임원 매매(get_executive_trading) 사이의 시점 교차 분석

        【효과적 활용 방법】
        - cash_dvdn_amt와 현금 및 현금성 자산(get_single_acc 기반) 비교로 배당 여력 정밀 평가
        - earn_vs_dvdn_rt가 과도하게 높을 경우 재투자 여력 부족 또는 경영진의 단기 주가 부양 전략 의심
        - stbd_vs_dvdn_rt 급등 → 주가 하락 및 고배당 유지에 따른 시장 오해 가능성 분석

        【주의사항 및 팁】
        - 배당 정보는 보고서 기준이며, 실제 지급일 또는 확정일은 공시상 별도 확인 필요
        - 자사주 보유율이 높을 경우, 배당총액 대비 실제 외부 유출 현금은 낮을 수 있음
        - 이사회 또는 주총결의와 관련된 공시(get_disclosure_list)로 배당 결정 변경 가능성 상시 모니터링
        """,
    tags={"배당", "배당금", "배당성향", "시가배당율"}
)
def get_dividend_info(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    배당에 관한 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019005
    """
    result = with_context(ctx, "get_dividend_info", lambda context: context.ds002.get_dividend_info(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_treasury_stock",
    description="""지정한 기업의 정기보고서에 공시된 자기주식의 취득·처분·소각 내역을 조회하는 도구입니다. 
        자기주식은 기업의 자본정책, 주가 방어 전략, 지배구조 조정, 내부자 보상 수단 등으로 활용되며, 이에 따라 내부 리스크와 시장 왜곡 신호를 조기에 포착할 수 있습니다.

        【핵심 제공 데이터】
        - acqs_mth1~3 (취득방법 대/중/소분류): 장내 매수, 신탁계약, 공개매수 등 자기주식 확보 수단 구체화
        - stock_knd (주식 종류): 보통주, 우선주 등 보유 주식 유형 파악
        - bsis_qy / trmend_qy (기초/기말 보유 수량): 보유량 변화를 통한 자기주식 운용 정책 확인
        - change_qy_acqs / change_qy_dsps / change_qy_incnr (취득/처분/소각 수량): 연도 내 실제 자기주식 변동 내역 분석
        - stlm_dt (결산 기준일): 분석 시점 일치 기준

        【연계 분석 도구】
        - get_major_holder_changes: 대주주와의 거래 여부, 우호지분 확보 시도 확인
        - get_disclosure_list: 자기주식 관련 주요 공시 병행 분석 (소각결의, 임원보상 등)
        - get_single_acc: 자기주식 보유에 따른 자본 감소 영향 여부 분석
        - get_executive_trading: 임원 보유 지분과 자기주식 변화 시점 비교로 내부거래 가능성 점검

        【활용 시나리오】
        - 장내 직접취득이 집중되었을 경우 → 단기 주가 부양 목적 또는 자사주 소각 계획 가능성
        - 공개매수로 대량 자기주식 확보 → 경영권 방어 또는 특정 주주 이탈 차단 의도
        - 처분 수량 증가 + get_executive_trading 결과와 일치 → 내부자에 대한 현물 보상 가능성
        - trmend_qy 급증 → 장기 자사주 활용 계획 (M&A, 스톡옵션 등) 추정
        - change_qy_incnr > 0 → 자본금 감소 및 주당 지표 개선 목적의 소각 시도

        【효과적 활용 방법】
        - bsis_qy와 trmend_qy 비교로 자기주식 누적 정책 분석
        - acqs_mth3 내역 중 "공개매수" 포함 시 지배구조 방어 목적 가능성 우선 검토
        - change_qy_acqs 대비 change_qy_incnr 비율로 소각 의지 및 실제 실행 여부 평가
        - get_disclosure_list와 시계열 연계로 소각결의, 신탁계약 연장, 처분공시 확인

        【주의사항 및 팁】
        - 자기주식은 자산으로 분류되지 않으며, 재무제표에서 자본 차감 항목임을 고려해 해석 필요
        - 신탁계약 방식의 보유 주식은 실제 통제 불가능할 수 있어 활용 제약이 있음
        - 정기보고서 기준이므로 분기 내 발생한 단기 거래는 반영되지 않을 수 있음
        """,
    tags={"자기주식", "취득", "처분", "현황"}
)
def get_treasury_stock(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자기주식 취득 및 처분현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019006
    """
    result = with_context(ctx, "get_treasury_stock", lambda context: context.ds002.get_treasury_stock(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_major_shareholder",
    description="""상장법인 및 주요 비상장법인이 정기보고서에서 공시한 최대주주 및 특수관계인의 지분 현황을 조회하는 도구입니다. 
        지배구조 안정성, 경영권 집중도, 내부자 중심 의사결정 구조의 위험성 등을 분석할 수 있으며, 보고 기간 내 지분율 변화는 경영권 분쟁 또는 승계 이슈의 신호로 활용될 수 있습니다.

        【핵심 제공 데이터】
        - nm / relate (성명 및 관계): 최대주주 본인, 배우자, 자녀, 계열회사 등으로 지배구조 핵심 인물 식별
        - stock_knd (주식 종류): 보통주, 우선주 등 의결권 포함 여부 판단
        - bsis_posesn_stock_co / qota_rt (기초 소유 주식 수 및 지분율): 분석 시작점의 보유 현황
        - trmend_posesn_stock_co / qota_rt (기말 소유 주식 수 및 지분율): 보고 종료 시점 보유 지분
        - rcept_no / stlm_dt (접수번호 / 결산 기준일): 공시 시점 기반 교차 분석 가능

        【연계 분석 도구】
        - get_major_holder_changes: 5% 이상 주주의 대량지분변동과 비교하여 지배구조 안정성 이중 검증
        - get_disclosure_list: 최대주주 관련 공시(지분매각, 승계, 증여 등) 추적
        - get_executive_trading: 최대주주가 임원인 경우 내부자 주식 거래 병행 분석
        - get_single_acc: 최대주주 지분율 변화 이후 자본금 변동 여부 정밀 검토

        【활용 시나리오】
        - 최대주주의 보유 지분율이 전년 대비 하락 → 경영권 이탈 또는 승계 가능성
        - 우선주 비중이 증가 → 의결권 없는 주식으로 자본 확충 시도 의심
        - 계열사 및 재단 등 특수관계인의 지분 집중 → 우호 지분 확보를 통한 지배력 유지 전략
        - get_major_holder_changes와 비교 시 지분 변동 없는 신고 누락 가능성 탐지
        - stlm_dt 기준 직후 get_disclosure_list로 증여, 매각, 지분 구조조정 공시 탐색

        【효과적 활용 방법】
        - bsis_posesn_qota_rt와 trmend_posesn_qota_rt 비교로 지분율 변동 추적
        - 성명 및 관계 항목 분석을 통해 동일 가문/법인의 지분 집중 구조 도출
        - "계" 항목으로 표시된 전체 합산 수치와 개별 지분율의 합계 차이로 공시 누락 가능성 판단
        - 우선주와 보통주의 보유 비중을 나눠서 분석하여 실질 지배력 파악

        【주의사항 및 팁】
        - 단일 공시 내 다양한 관계자의 지분이 나열되므로, 동일 계열로 분류된 항목 간 교차 분석 필수
        - "신규선임", "이사사임" 등 비고(rm) 항목의 이력 변화와 지분 변화는 반드시 병행 해석 필요
        - 기초 지분이 0 → 신규 취득 또는 승계의 시작점일 수 있으므로 get_disclosure_list와 연결 필요
        """,
    tags={"최대주주", "최대주주", "최대주주", "최대주주"}
)
def get_major_shareholder(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    최대주주에 관한 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019007
    """
    result = with_context(ctx, "get_major_shareholder", lambda context: context.ds002.get_major_shareholder(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_major_shareholder_changes",
    description="""상장법인 및 주요 비상장법인이 정기보고서에서 공시한 최대주주의 지분 변동 내역을 조회하는 도구입니다. 
        최대주주의 보유 지분 수량 및 지분율 변화, 변동 원인 등을 분석하여 경영권 안정성, 승계 진행 여부, 경영 리스크 발생 가능성 등을 종합적으로 평가할 수 있습니다.

        【핵심 제공 데이터】
        - change_on (변동일): 지분 변동이 발생한 정확한 시점으로, 다른 공시와 시계열 분석 가능
        - mxmm_shrholdr_nm (최대주주명): 변동 주체가 법인인지 개인인지 구분
        - posesn_stock_co / qota_rt (변동 후 보유 주식 수 / 지분율): 변동 후 최대주주의 실질 지배력 수준 판단
        - change_cause (변동 원인): 매매, 증여, 상속, 유상증자 참여 등 지분 변동의 직접 원인
        - stlm_dt (결산 기준일): 해당 정보가 포함된 보고서 기준일로 분석 타이밍 설정

        【연계 분석 도구】
        - get_major_shareholder: 결산 시점 기준 최대주주 보유지분 상태와 비교하여 변화 추적
        - get_disclosure_list: change_on 기준 전후 공시에서 배경 확인 (예: 증여, 임원 해임 등)
        - get_executive_trading: 최대주주가 임원인 경우 내부자 거래 패턴과 병행 분석
        - get_major_holder_changes: 대량 보유자 지분 변동과의 차이 비교로 이중 보고 또는 누락 여부 확인

        【활용 시나리오】
        - 지분율이 5% 미만으로 하락 → 최대주주 지위 상실로 인한 경영권 불안 가능성
        - change_cause가 '증여' → 경영권 승계 신호, 후계자 지분 상승 여부 병행 분석
        - 변동일(change_on) 이후 get_disclosure_list 상 임원교체 또는 주요 의사결정 여부 확인
        - 지분 감소 + rm 항목에 '이사사임', '계열사 매각' 등 병기 → 지배구조 개편 또는 계열 분리 가능성

        【효과적 활용 방법】
        - posesn_stock_co 및 qota_rt 값의 전기 대비 증감으로 지배력 변화 수치화
        - change_cause에 따른 리스크 분류: 매각(유동성 문제), 상속(승계 흐름), 증여(분산 지배 가능성)
        - get_major_shareholder과의 교차 분석으로 공시 간 불일치 여부 점검
        - get_disclosure_list로 변동 원인과 관련된 추가 공시 추적 (예: 유상증자, 기업분할 등)

        【주의사항 및 팁】
        - 지분율 변화가 작아도 실제 지배력 변화가 클 수 있으므로, 전체 발행 주식 수 추정 병행 필요
        - change_cause 항목이 비어 있거나 '기타'인 경우, 반드시 get_disclosure_list로 해석 보완 필요
        - 비고(rm) 항목의 '이사사임', '신규선임' 등 인사 정보는 지배력 교체의 신호일 수 있음
        """,
    tags={"최대주주", "최대주주", "최대주주", "최대주주"}
)
def get_major_shareholder_changes(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    최대주주의 주식변동 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019008
    """
    result = with_context(ctx, "get_major_shareholder_changes", lambda context: context.ds002.get_major_shareholder_changes(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_minority_shareholder",
    description="""상장법인 및 주요 비상장법인이 정기보고서에서 공시한 소액주주 현황을 조회하는 도구입니다. 
        소액주주 수와 보유 지분율을 분석하여 지배구조의 안정성, 경영권 방어 가능성, 적대적 인수합병(M&A) 위험 등을 평가할 수 있습니다.

        【핵심 제공 데이터】
        - shrholdr_co (소액주주 수): 지분 분산 정도 및 경영권 방어 기반 판단
        - shrholdr_tot_co (전체 주주 수): 전체 주주 중 소액주주 비중 평가
        - shrholdr_rate (소액주주 수 비율): 전체 주주 대비 소액주주 수 비율
        - hold_stock_co (소액주주 보유 주식 수): 소액주주 집단의 총 지분 규모 파악
        - stock_tot_co (총발행 주식 수): 기준이 되는 전체 주식 수량
        - hold_stock_rate (소액주주 보유 주식 비율): 전체 주식 대비 소액주주 집단 지분율
        - stlm_dt (결산 기준일): 데이터 기준 시점

        【연계 분석 도구】
        - get_major_shareholder: 최대주주 및 특수관계자 지분과 비교하여 소액주주 지배력 분포 분석
        - get_major_holder_changes: 대량 보유 주주 변동과 교차 분석하여 소액주주 비율 변화 여부 감지
        - get_disclosure_list: 소액주주 권익 관련 공시(배당, 합병, 주식병합 등) 모니터링
        - get_treasury_stock: 자사주와 소액주주 지분 비율의 상호작용 분석

        【활용 시나리오】
        - 소액주주 보유 지분율(hold_stock_rate)이 50% 이상 → 경영권 방어 취약성 증가
        - 소액주주 수(shrholdr_co) 급감 → 특정 세력에 의한 지분 집중 가능성
        - 소액주주 비율 급증 + 최대주주 지분율 하락 → 경영권 분쟁 가능성 사전 포착
        - hold_stock_rate 상승 → 적대적 M&A 시도에 대한 방어력 약화 경고

        【효과적 활용 방법】
        - hold_stock_rate를 최대주주 지분율과 비교하여 지배구조 안정성 진단
        - shrholdr_co 및 shrholdr_rate가 동시에 상승하는 경우 주주구성이 다변화되고 있는 신호로 해석
        - get_disclosure_list와 연결하여 소액주주 이익에 영향을 미칠 수 있는 주식 병합/감자 계획 여부 추적
        - get_major_holder_changes와 병행하여 지배력 이동의 숨은 조짐 포착

        【주의사항 및 팁】
        - 소액주주 정의는 공시 기준에 따라 변동 가능(일반적으로 5% 미만 보유자)
        - 합병, 인수, 유상증자 등 이벤트 전후로 소액주주 비율이 급변할 수 있으므로 시계열 데이터 병행 분석 필요
        - stock_tot_co가 변경된 경우, hold_stock_rate 단순 비교는 왜곡될 수 있으므로 주의
        """,
    tags={"소액주주", "소액주주소유주식", "소액주주비율"}
)
def get_minority_shareholder(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    소액주주에 관한 사항 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019009
    """
    result = with_context(ctx, "get_minority_shareholder", lambda context: context.ds002.get_minority_shareholder(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_executive_info",
    description="""상장법인 및 주요 비상장법인이 제출한 임원 현황 공시 데이터를 조회하는 도구입니다.  
        기업 경영진의 구조, 임원의 이력과 경영 역량, 지배구조 리스크 요인을 심층 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 성명(nm), 성별(sexdstn), 출생연월(birth_ym): 임원의 기본 인적 사항
        - 직위(ofcps), 담당업무(chrg_job): 임원의 조직 내 역할 및 책임 범위
        - 등기임원 여부(rgist_exctv_at): 법적 책임과 권한 유무 판단
        - 상근 여부(fte_at): 경영참여 실질성 분석
        - 주요 경력(main_career): 임원의 전문성 및 과거 경영 경험 검토
        - 최대주주 관계(mxmm_shrholdr_relate): 지배구조와의 이해상충 가능성 평가
        - 재직기간(hffc_pd), 임기만료일(tenure_end_on): 경영 연속성 및 이직 가능성 분석
        - 결산기준일(stlm_dt): 정보 기준 시점 명시

        【연계 분석 도구】
        - get_executive_trading: 임원 주식거래 이력을 통한 내부자 거래 리스크 탐색
        - get_major_holder_changes: 임원 변동과 주요 주주 지분율 변동 간 연관성 분석
        - get_disclosure_list: 임원 선임, 해임, 중도사임 등 관련 공시 병행 모니터링

        【활용 시나리오】
        - 등기임원 중 재직기간이 짧거나, 잦은 임원 교체 패턴을 통해 경영 불안정성 탐지
        - 주요 경력(main_career) 분석을 통해 외부 영입 vs 내부 승진 경향 파악 및 경영 전략 변화 예측
        - 최대주주 관계(mxmm_shrholdr_relate)가 존재하는 경우, 사익 추구 가능성 및 내부자 리스크 사전 점검
        - 대표이사, 이사회 의장 등 핵심 직위 임원의 이력 분석을 통해 기업 전략방향성과 리스크 감수성 평가
        - get_executive_trading 호출로 임원의 주식 매도 패턴을 교차 분석하여 경영진의 내부 전망 변화 조기 포착

        【효과적 활용 방법】
        - 임기만료일(tenure_end_on) 기준으로 임원 교체 예정 가능성 및 후속 리스크 모니터링
        - 상근 여부(fte_at)와 직무(chrg_job)를 비교하여 명목직 여부 판별
        - 주주총회 결과나 이사회 구성 변동(get_disclosure_list)과 연계하여 임원 선임, 해임 패턴 심층 분석
        - 주요 경력(main_career)과 현재 담당업무(chrg_job)를 비교해 직무적합성 평가

        【주의사항 및 팁】
        - 결산기준일(stlm_dt)이 과거 시점일 경우, 최신 임원 변동사항은 get_disclosure_list 병행 조회 필수
        - 성별(sexdstn), 출생연월(birth_ym)은 법적 공시 항목이나, 실제 분석 시에는 개인정보 보호 측면 고려 필요
        """,
    tags={"임원", "현황", "임원", "현황"}
)
def get_executive_info(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    임원의 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019010
    """
    result = with_context(ctx, "get_executive_info", lambda context: context.ds002.get_executive_info(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_employee_info",
    description="""상장법인 및 주요 비상장법인이 제출한 직원 현황 공시 데이터를 조회하는 도구입니다.  
        사업부문별·성별 인력 구성, 근속연수, 계약직 비중, 평균 급여 수준 등을 통해 조직 안정성, 노동 비용 구조, 성별 다양성 및 고용 형태 불균형을 진단하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 성별(sexdstn), 사업부문(fo_bbm): 인력 구성의 다변성과 부문별 조직 특성 파악
        - 정규직/계약직 수(rgllbr_co, cnttk_co), 단시간 근로자 수(rgllbr_abacpt_labrr_co, cnttk_abacpt_labrr_co): 고용 안정성 및 유연근무제 운용 실태 평가
        - 평균 근속연수(avrg_cnwk_sdytrn): 조직 충성도, 인력 이탈률 간접 추정
        - 1인당 평균 급여(jan_salary_am), 연간 총급여(fyer_salary_totamt): 보상수준, 인건비 부담 정도 진단
        - 개정 전 인원수(reform_bfe_emp_co_*): 조직개편 전후 인력 이동 파악
        - 결산기준일(stlm_dt): 정보의 시점 명시

        【연계 분석 도구】
        - get_single_acc: 급여 총액 대비 매출액, 영업이익 대비 인건비 비중 분석
        - get_executive_info: 임원 대비 일반 직원 보상 구조 및 조직 간 형평성 분석
        - get_disclosure_list: 정리해고, 조직개편, 복지제도 변경 등 고용 관련 공시 병행 확인

        【활용 시나리오】
        - 특정 사업부 인력의 평균 근속연수가 급감했을 경우, 대규모 이직 또는 구조조정 신호로 해석
        - 계약직 비중이 높은 부문 확인을 통해 외주화 또는 불안정 고용 리스크 진단
        - 급여 총액과 인당 평균 급여 간의 불일치 여부를 통해 고연봉 소수집단 존재 여부 추정
        - 성별 합계 기준으로 남녀 간 보상 격차 존재 여부 확인 및 다양성 정책 실행 여부 검토
        - get_single_acc와 연계하여 인건비가 수익성에 미치는 영향 정량 평가

        【효과적 활용 방법】
        - 부문별 인원수 대비 평균 근속연수를 교차 분석해 조직의 성장성과 이직률 평가
        - 정규직 대비 계약직 비율로 노동 유연화 수준 및 고용 불안정성 판단
        - 총급여 대비 정규직 수 추정치를 활용하여 연봉 추정치 역산 및 업계 평균과 비교 분석
        - 연도별 공시 비교를 통해 인건비 증가 추이 및 인사 정책 변화 모니터링

        【주의사항 및 팁】
        - 평균 급여(jan_salary_am)와 총급여(fyer_salary_totamt)가 '-'인 경우는 공시 생략 혹은 미제공이므로 별도 공시(get_disclosure_list) 병행 분석 필요
        - ‘성별합계’ 구분은 전체 현황 파악용이며, 동일 성별의 부문별 중복 집계가 있을 수 있으므로 해석 시 주의
        """,
    tags={"직원", "현황", "조직안정성", "급여"}
)
def get_employee_info(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    직원 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019011
    """
    result = with_context(ctx, "get_employee_info", lambda context: context.ds002.get_employee_info(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_individual_compensation",
    description="""상장법인 및 주요 비상장법인이 공시한 개별 임원의 보수 내역을 조회하는 도구입니다.  
        고액 보수 수령 임원 식별, 보수 체계의 불균형 여부, 경영성과 대비 과도한 보상 리스크 등을 분석하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 성명(nm), 직위(ofcps): 보수 대상 임원의 기본 정보
        - 보수 총액(mendng_totamt): 해당 연도 지급된 총 보수(급여, 상여, 퇴직금 포함)
        - 비포함 보수(mendng_totamt_ct_incls_mendng): 지급 총액에 포함되지 않은 보수 항목
        - 결산기준일(stlm_dt): 보수 산정 기준 시점
        - 접수번호(rcept_no): 공시 원문 확인을 위한 식별자

        【연계 분석 도구】
        - get_executive_info: 임원의 재직기간, 담당업무와 보수 비교를 통한 적정성 평가
        - get_employee_info: 일반 직원 평균급여 대비 임원 보수 격차 분석
        - get_disclosure_list: 추가 보수 관련 공시(성과급 지급 결정 등) 병행 확인

        【활용 시나리오】
        - 특정 임원이 퇴직 후에도 고액 보수를 수령한 경우, 퇴직금 또는 일시 상여 여부 확인
        - 동일 직급 간 보수 격차가 클 경우 내부 보상 시스템의 불균형성 여부 평가
        - 비포함 보수 항목 존재 시, 현금 외 보상 또는 이연지급 구조 여부 파악
        - get_employee_info와 연계하여 대표이사와 일반 직원 간 보수 비율 분석(Gap Ratio)
        - 결산기준일(stlm_dt)과 연계하여 연도별 보수 추이 분석

        【효과적 활용 방법】
        - 보수총액 순으로 정렬하여 최고보수 수령자 식별 및 경영권 집중 여부 파악
        - 동일 기업 내 직위별 평균 보수와 비교하여 과도한 보상 여부 정량 평가
        - get_executive_info의 재직기간(hffc_pd)과 cross-check하여 단기 재직 후 고액 수령 여부 확인
        - 이사회 또는 보상위원회 결의 이력(get_disclosure_list)와 함께 해석하여 투명성 확보 여부 점검

        【주의사항 및 팁】
        - 비포함 보수 항목이 '-'로 표시될 경우, 공시 생략 혹은 일괄포함일 수 있으므로 공시원문 확인 권장
        - 본 도구는 주로 '5억 원 초과 보수 수령자'에 대해 공시 의무가 있기 때문에, 기업 전체 임원 보수 데이터와는 차이가 있을 수 있음
        """,
    tags={"개별임원", "보수", "급여총액", "상여금"}
)
def get_individual_compensation(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    개별 임원 보수 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019012
    """
    result = with_context(ctx, "get_individual_compensation", lambda context: context.ds002.get_individual_compensation(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_total_compensation",
    description="""상장법인 및 주요 비상장법인이 제출한 임원 전체 보수 총액 공시 데이터를 조회하는 도구입니다.  
        임원 보수 집계 수준, 평균 보수 수준, 보상 구조의 집중도 및 기업의 보수 투명성을 종합적으로 분석하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 인원수(nmpr): 보수를 지급받은 등기임원 수
        - 보수 총액(mendng_totamt): 해당 연도 전체 등기임원에게 지급된 총 보수 금액(급여, 상여, 퇴직급 등 포함)
        - 1인 평균 보수액(jan_avrg_mendng_am): 단순평균 기준 보수 규모 파악
        - 결산기준일(stlm_dt): 보수 산정 기준 시점
        - 접수번호(rcept_no): 상세 공시 확인용 식별자

        【연계 분석 도구】
        - get_individual_compensation: 평균값과 개별 최고 보수자 간 괴리 확인
        - get_executive_info: 임원 재직기간 및 직무 대비 보수 적정성 평가
        - get_employee_info: 일반 직원 대비 임원 보수 격차 분석
        - get_disclosure_list: 보수 관련 결의사항(보상위원회, 정관 변경 등) 병행 추적

        【활용 시나리오】
        - 평균 보수(jan_avrg_mendng_am)가 급증한 경우, 일회성 상여금 또는 퇴직금 포함 여부 확인
        - 보수 총액 대비 인원수로 구성원의 보상 집중도 추정(소수 고액 보상 구조 여부 파악)
        - 동일 기업의 연도별 공시를 비교하여 보수 정책의 변화 및 리스크 감지
        - get_individual_compensation과 교차 비교하여 최고 보수자의 과도한 비중 탐지
        - get_employee_info 연계하여 직원 대비 수십 배 이상 격차 존재 시 경영 불균형 평가

        【효과적 활용 방법】
        - 1인 평균 보수액과 개별 최고 보수액의 비율을 계산해 보상 집중도 분석
        - 보수총액과 get_single_acc의 영업이익 또는 당기순이익과 비교하여 보수지급 여력 및 무리한 배분 여부 판단
        - 보수 수령 임원 수가 이사회 구성원보다 적은 경우, 보수 미공시자 또는 비등기임원 여부 확인 필요
        - 연도별 시계열 공시를 비교하여 보상 구조의 지속성 및 급격한 변동 여부 평가

        【주의사항 및 팁】
        - 본 공시는 5억 원 이상 개별 보수자가 존재할 경우 의무제출 대상이 되므로, 미제출 시 get_individual_compensation을 함께 조회해야 정보 누락 여부를 판단할 수 있습니다.
        - 단순 평균값은 보상의 불균형을 가릴 수 있으므로, 개별 보수 공시와 병행해 확인하는 것이 권장됩니다.
        """,
    tags={"임원", "보수", "현황", "임원"}
)
def get_total_compensation(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    임원 전체 보수 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (11011: 사업보고서, 11012: 반기, 11013: 1분기, 11014: 3분기)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019013
    """
    result = with_context(ctx, "get_total_compensation", lambda context: context.ds002.get_total_compensation(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_individual_compensation_amount",
    description="""정기보고서(사업, 분기, 반기보고서) 내에 개인별 보수지급 금액(5억이상 상위5인)을 제공합니다.
        등기 여부와 관계없이 일정 금액 이상의 보수를 수령한 임원을 식별할 수 있어, 내부자 보상 불균형, 퇴직자 고액 보상 문제, 지배구조 리스크 탐지에 활용됩니다.

        【핵심 제공 데이터】
        - 이름(nm), 직위(ofcps): 고액 보수 수령자 신원 및 조직 내 역할 확인
        - 보수 총액(mendng_totamt): 퇴직금, 상여, 급여 등을 포함한 총 보수
        - 보수총액 비포함 항목(mendng_totamt_ct_incls_mendng): 주석상 별도 보상 또는 이연 보상 여부 확인
        - 결산기준일(stlm_dt): 공시 기준 시점
        - 접수번호(rcept_no): 공시 원문 확인용 식별자

        【연계 분석 도구】
        - get_total_compensation: 전체 등기임원 보수 총액과 비교해 보상 집중도 분석
        - get_individual_compensation: 등기임원 여부 확인 및 직무연계 검토
        - get_executive_info: 재직기간(hffc_pd), 담당업무와 보수 간의 적절성 평가
        - get_disclosure_list: 퇴직금 특별지급, 보상기준 변경 등 관련 결의사항 공시 병행 확인

        【활용 시나리오】
        - 퇴직자 또는 前임원이 재직 당시보다 높은 보수를 수령한 경우, 퇴직금 일시지급 또는 성과보상 의심
        - get_individual_compensation과 비교하여 등기 여부가 다른 경우, 내부자 보상 규정의 일관성 여부 검토
        - 평균 보수 수준 대비 이례적으로 높은 금액이 지급된 경우, 특별상여 또는 지배주주 편의성 지급 여부 분석
        - stlm_dt 기준으로 해마다 고액 수령자 변화를 추적하여 보상 집중 패턴 또는 정책 변화 여부 탐색

        【효과적 활용 방법】
        - 동일 이름이 get_individual_compensation에 존재하지 않을 경우, 비등기임원 또는 퇴직자 고액 보수 가능성으로 간주
        - mendng_totamt 순으로 정렬하여 최고 보수자 식별 후 get_executive_info로 직무 적합성 및 경력 확인
        - 연도별 비교를 통해 고액 보수자가 일정 인물군에 집중되는 구조적 보상 불균형 여부 판단
        - 비포함 보수 항목이 있는 경우, 그 의미를 공시 주석 또는 get_disclosure_list와 함께 해석하여 이연 보상 또는 스톡옵션 지급 여부 확인

        【주의사항 및 팁】
        - 본 도구는 등기임원 외에 연구원, 고문 등 특정 직위자에게도 고액 보수가 지급되었는지 확인할 수 있어, 보수 체계의 사각지대를 파악하는 데 유용합니다.
        - 동일한 인물이 여러 공시에 반복 등장할 경우, 지급 항목 중복 여부를 주의 깊게 해석해야 합니다.
        """,
    tags={"개인별", "보수", "지급", "금액"}
)
def get_individual_compensation_amount(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    개인별 보수지급 금액 조회 (5억 이상 상위 5인)

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019014
    """
    result = with_context(ctx, "get_individual_compensation_amount", lambda context: context.ds002.get_individual_compensation_amount(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_investment_in_other_corp",
    description="""상장법인 및 주요 비상장법인이 제출한 사업보고서 내 '타법인 출자현황' 정보를 조회하는 도구입니다. 
        계열사 또는 비계열사에 대한 출자 내역을 통해 지분구조, 출자목적, 재무적 건전성 및 잠재 리스크를 종합적으로 파악할 수 있습니다.

        【핵심 제공 데이터】
        - 출자법인명(inv_prm): 타법인 명칭을 통해 출자 대상 식별
        - 최초취득일자(frst_acqs_de), 최초취득금액(frst_acqs_amount): 출자 시점 및 초기 투자규모
        - 출자목적(invstmnt_purps): 단순 투자, 자회사 설립, 경영권 확보 목적 등 분류
        - 기초 및 기말 잔액 수량/지분율/장부가액: 기간 내 보유 지분 변동 및 평가 변화
        - 기초잔액: bsis_blce_qy, bsis_blce_qota_rt, bsis_blce_acntbk_amount
        - 기말잔액: trmend_blce_qy, trmend_blce_qota_rt, trmend_blce_acntbk_amount
        - 취득·처분 관련 변동 수량 및 금액: incrs_dcrs_acqs_dsps_qy, incrs_dcrs_acqs_dsps_amount
        - 평가손익 변동액: incrs_dcrs_evl_lstmn
        - 피출자법인의 재무현황: 총자산(recent_bsns_year_fnnr_sttus_tot_assets), 당기순이익(recent_bsns_year_fnnr_sttus_thstrm_ntpf)
        - 결산기준일(stlm_dt): 해당 데이터 기준일

        【연계 분석 도구】
        - get_major_holder_changes: 출자 이후 주요 주주 지분율 변화 분석
        - get_single_acc: 출자 관련 자산·지분 항목의 회계 반영 여부 확인
        - get_business_acquisition: 동일 출자 기업의 영업 양수 여부 병행 탐색
        - get_disclosure_list: 출자와 관련된 공시 이력 추가 확인

        【활용 시나리오】
        - 계열사/비계열사 출자 내역 검토를 통해 그룹 확장 전략 및 계열사 리스크 탐지
        - 출자 목적이 단순 수익성 확보인지, 지배력 확보 목적(자회사 설립 등)인지 구분
        - 평가손익(incrs_dcrs_evl_lstmn) 급변 여부로 출자 지분 가치의 변동성 파악
        - 피출자법인의 재무성과(총자산, 당기순이익)와 보유 지분율을 교차 분석하여 투자 효율성 평가
        - 출자금액 대비 피출자기업 실적이 저조한 경우, 손상차손 또는 추가 평가손실 가능성 사전 탐지

        【효과적 활용 방법】
        - 기초/기말 장부가액 차이를 분석하여 평가이익 또는 손실 발생 여부 추적
        - 보유 지분율(trmend_blce_qota_rt)이 20% 이상이면 관계기업으로 회계 반영 가능성 점검
        - 출자 목적(invstmnt_purps)이 모호하거나 부실기업에 대한 반복 출자인 경우, 내부거래 또는 부실계열사 지원 가능성 탐지
        - 동일한 rcept_no로 여러 출자 항목이 존재할 경우, 보고서 내 '합계' 행을 필터링하여 분석 대상 정제 필요

        【주의사항 및 팁】
        - '합계', '-', '0' 등으로 표시된 항목은 데이터 비제공 또는 불완전 공시이므로 신중한 해석 필요
        - 출자법인이 비상장일 경우, 외부 데이터와의 비교 분석이 제한될 수 있음
        """,
    tags={"타법인", "출자", "현황", "타법인"}
)
def get_investment_in_other_corp(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    타법인 출자현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019015
    """
    result = with_context(ctx, "get_investment_in_other_corp", lambda context: context.ds002.get_investment_in_other_corp(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_total",
    description="""사업보고서 또는 분기/반기보고서 내 '주식총수에 관한 사항'을 조회하는 도구입니다. 
        발행가능 주식 수, 실제 발행주식 수, 유통주식 수, 감자 및 소각 주식 수 등의 정보는 자본금 변화, 유통 물량 리스크, 지배구조 변동 가능성 등을 정량적으로 분석하는 데 필수적입니다.

        【핵심 제공 데이터】
        - 발행할 주식의 총수(isu_stock_totqy): 회사 정관상 허용된 최대 발행 한도
        - 현재까지 발행한 주식 수(now_to_isu_stock_totqy): 누적 신주 발행 규모 확인
        - 현재까지 감소한 주식 수(now_to_dcrs_stock_totqy): 감자(redc), 이익소각(profit_incnr), 상환주식(rdmstk_repy) 등 포함
        - 발행주식 총수(istc_totqy): 실질 유효한 주식 수 (Ⅱ - Ⅲ 계산값)
        - 자기주식수(tesstk_co): 기업이 보유한 자사주 수량 (Ⅳ - Ⅴ → 유통주식수에 직접 영향)
        - 유통주식수(distb_stock_co): 시장에 실제 유통되는 주식 수
        - 결산기준일(stlm_dt): 해당 데이터 기준 시점

        【연계 분석 도구】
        - get_paid_in_capital_increase, get_free_capital_increase: 유상/무상증자에 따른 발행 주식 수 변화 확인
        - get_capital_reduction: 감자 이후 감소 주식 수 반영 여부 확인
        - get_major_holder_changes: 유통주식수 변화에 따른 지배력 변동 추적
        - get_treasury_stock_acquisition, get_treasury_stock_disposal: 자사주 취득/처분에 따른 유통주식 변동 영향 확인

        【활용 시나리오】
        - 주식총수 변동 분석을 통해 증자, 감자, 자사주 취득 후 지분구조 변화 감지
        - distb_stock_co의 급증 여부를 통해 유통물량 확대 → 주가 변동성 가능성 평가
        - redc, profit_incnr 항목 활용하여 자본 축소, 주주가치 보호 목적의 구조조정 여부 분석
        - tesstk_co 증가 시, 향후 자사주 처분 가능성 및 경영권 방어 전략 여부 사전 분석
        - isu_stock_totqy와 now_to_isu_stock_totqy 비교로 추가 신주 발행 여력 파악

        【효과적 활용 방법】
        - 감자 및 소각 항목(now_to_dcrs_stock_totqy)을 통해 총발행주식 대비 감축률 계산
        - 유상/무상증자 결정 후 본 도구 호출하여 실제 발행된 주식 반영 여부 확인
        - distb_stock_co를 기준으로 get_major_holder_changes 결과와 교차분석 → 지배력 희석 또는 집중 여부 탐지
        - tesstk_co(자기주식) 수량 변화 추적을 통해 주가 방어 정책 또는 지배권 방어 가능성 사전 탐색

        【주의사항 및 팁】
        - '합계', '비고' 등 se 필드는 정제 후 분석 필요
        - 결산기준일(stlm_dt)을 기준으로 시계열 분석 시 유의
        """,
    tags={"주식", "총수", "현황", "주식"}
)
def get_stock_total(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주식의 총수 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020002
    """
    result = with_context(ctx, "get_stock_total", lambda context: context.ds002.get_stock_total(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_debt_securities_issued",
    description="""사업보고서 및 분기/반기보고서 내 '채무증권 발행내역'을 조회하는 도구입니다. 
        회사가 발행한 회사채를 중심으로, 발행시기·규모·이자율·신용등급 등을 바탕으로 자금조달 구조 및 부채 리스크를 정량적으로 평가하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 발행회사(isu_cmpny): 실제 채권 발행 주체 (자회사 또는 해외 법인 포함)
        - 증권종류(scrits_knd_nm): 회사채, 전환사채, 교환사채 등 구분
        - 발행방법(isu_mth_nm): 공모/사모 구분을 통한 투자자 분산 여부 판단
        - 발행일자(issu_de), 만기일(mtd): 채권의 잔존 기간 분석
        - 권면총액(facvalu_totamt): 채무 총액 (원화 기준)
        - 이자율(intrt): 고정금리/변동금리 포함, 자금조달 비용 평가
        - 평가등급 및 기관(evl_grad_instt): 채무 리스크에 대한 외부 신용도
        - 상환여부(repy_at): 일부상환, 미상환 등 상환 진행 현황
        - 주관회사(mngt_cmpny): 발행 당시 주요 금융기관(신뢰성 및 구조조정 협상력 판단 가능)
        - 결산기준일(stlm_dt): 보고 기준일

        【연계 분석 도구】
        - get_single_acc: 회사채 총액과 재무제표 내 부채비율 비교
        - get_write_down_bond: 상각형 조건부 자본증권 여부 병행 확인
        - get_major_holder_changes: 대규모 채권 상환 직후 주요 주주 지분 변동 여부 분석
        - get_disclosure_list: 채권 관련 조건 변경, 만기 연장 등 추가 공시 추적

        【활용 시나리오】
        - 다수의 자회사(예: Harman) 또는 해외법인을 통한 발행 → 연결 부채 집중 여부 탐지
        - facvalu_totamt가 총자산의 일정 비율 초과 시 → 과도한 외부차입 리스크 경고
        - 상환여부(repy_at)가 '미상환'인 경우 잔존채무로 추적 → 유동성 압박 가능성 평가
        - intrt가 5% 이상 등 고금리 채권 존재 시 → 재무 레버리지에 의한 이익 잠식 가능성 분석
        - evl_grad_instt에 낮은 신용등급(BBB 이하)이 포함된 경우 → 추후 리파이낸싱 부담 가중 여부 모니터링

        【효과적 활용 방법】
        - 이자율(intrt) 평균과 신용등급(evl_grad_instt)을 종합적으로 비교하여 기업의 자금조달 여건 추정
        - 발행회사(isu_cmpny)가 비상장 해외법인일 경우 연결재무제표 포함 여부를 get_single_acc로 교차 검증
        - 발행 후 5년 이상 경과한 채권은 만기 도래 리스크 사전 점검 필요
        - 주관회사(mngt_cmpny)가 복수 기관일 경우, 구조화채 여부 등 고위험 상품 포함 가능성 점검

        【주의사항 및 팁】
        - '합계' 항목은 분석 시 제외해야 하며, 실제 발행 법인별 개별 분석이 필요
        - 발행일자, 만기일 등의 포맷은 YYYY.MM.DD 형태로 제공되며, 날짜 정제 후 시계열 분석 필요
        """,
    tags={"채무증권", "발행", "실적", "채무증권"}
)
def get_debt_securities_issued(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    채무증권 발행실적 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020003
    """
    result = with_context(ctx, "get_debt_securities_issued", lambda context: context.ds002.get_debt_securities_issued(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_commercial_paper_outstanding",
    description="""사업보고서 및 분기/반기보고서 내 '기업어음(CP) 미상환 잔액 현황'을 조회하는 도구입니다. 
        기업이 발행한 상환 전단기채권의 잔존 만기 구조를 통해 단기차입 의존도, 유동성 리스크, 차환 부담 등을 종합적으로 분석할 수 있습니다.

        【핵심 제공 데이터】
        - 잔여만기구간별 미상환금액 (단위: 원)
        - 10일 이하(de10_below)
        - 10일 초과 ~ 30일 이하(de10_excess_de30_below)
        - 30일 초과 ~ 90일 이하(de30_excess_de90_below)
        - 90일 초과 ~ 180일 이하(de90_excess_de180_below)
        - 180일 초과 ~ 1년 이하(de180_excess_yy1_below)
        - 1년 초과 ~ 2년 이하(yy1_excess_yy2_below)
        - 2년 초과 ~ 3년 이하(yy2_excess_yy3_below)
        - 3년 초과(yy3_excess)
        - 발행 방식(remndr_exprtn2): 공모/사모 구분
        - 미상환 잔액 합계(sm): 전체 기업어음 미상환 금액
        - 결산기준일(stlm_dt): 보고 기준 시점

        【연계 분석 도구】
        - get_debt_securities_issued: 중장기 채권 구조와 비교해 만기구조 불균형 여부 파악
        - get_single_acc: 총부채 대비 CP 비중 확인을 통한 단기유동성 위험도 분석
        - get_creditor_management: 과도한 단기차입 → 채권단 관리 절차 돌입 가능성 사전 탐지
        - get_bankruptcy: 단기 CP 차환 실패에 따른 부도 리스크 연계 확인

        【활용 시나리오】
        - 단기 만기구간(90일 이하) 집중 시 차환 리스크 상존 여부 판단
        - 1년 미만 만기가 전체 CP의 80% 이상인 경우, 자금시장 변동에 매우 민감한 구조로 평가
        - 사모 위주 발행 시, 시장공개 가능성 부족 → 신뢰도 및 유동성 낮음
        - 공모 발행 비중이 높다면 공개조달을 통한 신뢰 확보 전략으로 해석 가능
        - 연속된 기간 동안 '잔여만기 10일 이하' 미상환 규모가 급증 시, 단기 유동성 위기 가능성 평가

        【효과적 활용 방법】
        - CP 만기 분포를 시계열로 추적하여 만기 집중 현상 발생 시점 예측
        - 총 미상환 금액(sm)이 자산총계(get_single_acc) 또는 현금성 자산 대비 과도한 경우 유동성 경고 신호로 해석
        - 사모 CP 발행이 지속되는 경우, 비공개 자금조달로 인한 투자자 정보 비대칭성 주의
        - get_disclosure_list 호출을 통해 CP 발행과 상환 관련 추가 공시 모니터링 병행

        【주의사항 및 팁】
        - 합계(remndr_exprtn2="합계") 및 '-' 값은 전처리 과정에서 제외하여 분석 필요
        - 실제 만기 도래일 기준 분석을 위해 결산기준일(stlm_dt)을 기준으로 경과 일수 계산 필요
        """,
    tags={"기업어음증권", "미상환", "잔액", "기업어음증권"}
)
def get_commercial_paper_outstanding(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    기업어음증권 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020004
    """
    result = with_context(ctx, "get_commercial_paper_outstanding", lambda context: context.ds002.get_commercial_paper_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_short_term_bond_outstanding",
    description="""사업보고서 및 분기/반기보고서 내 '단기사채(SB) 미상환 잔액 현황'을 조회하는 도구입니다. 
        기업이 단기 유동성 확보를 위해 발행한 단기사채의 잔존 만기 분포와 발행한도 정보를 기반으로 차입 구조의 단기 집중성, 유동성 압박 가능성, 차환 리스크 등을 진단하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 잔여만기구간별 미상환금액 (단위: 원)
        - 10일 이하(de10_below)
        - 10일 초과 ~ 30일 이하(de10_excess_de30_below)
        - 30일 초과 ~ 90일 이하(de30_excess_de90_below)
        - 90일 초과 ~ 180일 이하(de90_excess_de180_below)
        - 180일 초과 ~ 1년 이하(de180_excess_yy1_below)
        - 발행 한도 정보
        - 총 발행 한도(isu_lmt): 정관 또는 내규상 설정된 단기사채 총 발행 가능 금액
        - 잔여 발행 여력(remndr_lmt): 미사용 한도 (차입 확대 가능성 평가 지표)
        - 발행 방식(remndr_exprtn2): 공모/사모 구분 (공개성, 투명성 지표)
        - 총 미상환 금액(sm): 전 단기채 총액
        - 결산기준일(stlm_dt): 데이터 기준 시점

        【연계 분석 도구】
        - get_commercial_paper_outstanding: 기업어음(CP) 잔액과 병행 분석하여 단기 조달 수단의 분산 여부 확인
        - get_single_acc: 유동자산, 현금성자산, 총부채 대비 단기차입금 규모 분석
        - get_creditor_management: 단기사채 상환 부담 누적 → 채권자 관리 전환 가능성 탐지
        - get_bankruptcy: 유동성 위기 심화 시 부도 리스크 모니터링

        【활용 시나리오】
        - de30_excess_de90_below 또는 de90_excess_de180_below 항목 집중 시 → 분기 내 집중 상환 리스크 존재
        - 잔여 발행한도(remndr_lmt)가 낮거나 0일 경우 → 추가 차입 여력 한계 상황 평가
        - sm(미상환 총액)이 자산총계의 10% 이상일 경우 → 단기레버리지 과중 위험 경고
        - 공모보다 사모 비중이 과도할 경우 → 정보 비대칭 및 유동성 낮은 구조로 평가

        【효과적 활용 방법】
        - de180_excess_yy1_below 이하 항목 합계를 기준으로, 향후 1년 내 집중 상환 부담 수준 수치화
        - isu_lmt 대비 sm 비율을 계산하여 발행 한도 대비 실제 사용률 분석
        - 동일 결산기준일(stlm_dt) 기준 CP와 단기사채의 만기구조를 통합 분석하여 총 단기조달 리스크 정량화
        - 발행 방식(remndr_exprtn2)별로 공모·사모를 구분하여 시장 접근성 및 신뢰성 평가

        【주의사항 및 팁】
        - ‘합계’, ‘비고’ 항목은 데이터 전처리 단계에서 필터링 필요
        - 일부 항목 값이 '-'로 표시되는 경우 실제 미보유 또는 공시 생략 가능성이 있어 주석 또는 본문 확인 병행 필요
        - CP와 단기사채가 중복 또는 대체적으로 사용되는 경우 전체 차입구조 재정의 필요
        """,
    tags={"단기사채", "미상환", "잔액", "단기사채"}
)
def get_short_term_bond_outstanding(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    단기사채 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020005
    """
    result = with_context(ctx, "get_short_term_bond_outstanding", lambda context: context.ds002.get_short_term_bond_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_corporate_bond_outstanding",
    description="""사업보고서 및 분기/반기보고서 내 '회사채(CB) 미상환 잔액 현황'을 조회하는 도구입니다. 
        기업이 발행한 중·장기 회사채의 잔존 만기 구조를 기반으로 상환 부담 분포, 재무 레버리지 구조, 유동성 리스크 및 차환 전략 필요 여부 등을 정량적으로 분석할 수 있습니다.

        【핵심 제공 데이터】
        - 잔여만기구간별 미상환 회사채 금액 (단위: 원)
        - 1년 이하(yy1_below)
        - 1년 초과 ~ 2년 이하(yy1_excess_yy2_below)
        - 2년 초과 ~ 3년 이하(yy2_excess_yy3_below)
        - 3년 초과 ~ 4년 이하(yy3_excess_yy4_below)
        - 4년 초과 ~ 5년 이하(yy4_excess_yy5_below)
        - 5년 초과 ~ 10년 이하(yy5_excess_yy10_below)
        - 10년 초과(yy10_excess)
        - 미상환 총액(sm): 전체 미상환 회사채 잔액 합계
        - 발행 유형(remndr_exprtn2): 공모/사모 구분
        - 결산기준일(stlm_dt): 보고 기준 시점

        【연계 분석 도구】
        - get_debt_securities_issued: 실제 발행 조건 및 발행 당시 신용등급 비교
        - get_single_acc: 총부채 대비 회사채 비중 분석, 현금흐름 대비 상환 여력 진단
        - get_creditor_management: 대규모 만기집중이 구조조정이나 채권단 개입으로 이어질 가능성 사전 탐지
        - get_disclosure_list: 만기 연장, 조건 변경, 조기상환 등 공시 확인

        【활용 시나리오】
        - yy1_below 항목이 클 경우, 향후 1년 내 대규모 상환 예정 → 단기 유동성 위기 가능성 평가
        - yy5_excess_yy10_below 또는 yy10_excess 중심 구조 → 장기 레버리지 기반 투자 전략 가능성 추정
        - 공모 비중이 높을 경우 공개 신용시장 의존도 높음 → 금리 변동 리스크 민감
        - 사모 중심 구조는 정보 비대칭 가능성 및 특정 투자자 종속 우려
        - sm 값이 자본총계 대비 과도할 경우 장기적 재무 안정성 저하 위험 존재

        【효과적 활용 방법】
        - 잔존 만기구간별 비중을 그래프화하여 상환 집중 구간 시각화
        - sm(총 미상환금액)과 get_single_acc 결과의 부채총계 항목 비교 → 기업 전반의 레버리지 진단
        - 3년 내 만기(yy3_excess_yy4_below 이하) 항목 합계 비율이 70% 이상이면 중기 차환 부담 과중 위험으로 판단
        - get_disclosure_list 연계로 회사채 관련 리파이낸싱 계획 또는 리스크 대응 공시 병행 확인

        【주의사항 및 팁】
        - remndr_exprtn2='합계' 또는 '-' 값은 분석 시 제외 필요
        - yy10_excess 항목 값이 없는 경우에도 존재 가능성 있으므로 공시 본문에서 장기물 유무 병행 검토
        - 회사채는 대부분 원금 일시상환 구조이므로 잔존 만기 도래 시점에 상환 집중 리스크가 큼
        """,
    tags={"회사채", "미상환", "잔액", "회사채"}
)
def get_corporate_bond_outstanding(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회사채 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020006
    """
    result = with_context(ctx, "get_corporate_bond_outstanding", lambda context: context.ds002.get_corporate_bond_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_hybrid_securities_outstanding",
    description="""사업보고서 및 분기/반기보고서 내 '신종자본증권(하이브리드 증권) 미상환 잔액 현황'을 조회하는 도구입니다. 
        장기 만기 또는 영구 지속 가능성이 있는 신종자본증권은 자본으로 분류될 수 있으나, 실제로는 고정 이자부 부채 성격도 강해 기업의 재무 안정성과 레버리지 구조에 중요한 영향을 미칩니다.

        【핵심 제공 데이터】
        - 잔여만기구간별 미상환 금액 (단위: 원)
        - 1년 이하(yy1_below)
        - 1년 초과 ~ 5년 이하(yy1_excess_yy5_below)
        - 5년 초과 ~ 10년 이하(yy5_excess_yy10_below)
        - 10년 초과 ~ 15년 이하(yy10_excess_yy15_below)
        - 15년 초과 ~ 20년 이하(yy15_excess_yy20_below)
        - 20년 초과 ~ 30년 이하(yy20_excess_yy30_below)
        - 30년 초과(yy30_excess)
        - 발행방식(remndr_exprtn2): 공모 또는 사모 구분
        - 미상환 합계(sm): 전체 하이브리드 증권 잔액 총합
        - 결산기준일(stlm_dt): 데이터 기준일

        【연계 분석 도구】
        - get_write_down_bond: 상각 조건 여부 및 자본 인정 요건 비교
        - get_single_acc: 자본총계 대비 신종자본증권 비중 확인 및 부채비율 개선 효과 평가
        - get_debt_securities_issued: 일반 채권과의 이자 조건 및 만기구조 비교
        - get_major_holder_changes: 특정 투자자에게 집중된 사모 발행 리스크 여부 확인

        【활용 시나리오】
        - 신종자본증권 잔액이 자본총계의 일정 비율 이상일 경우 → 외형상 자본건전성 개선 효과 존재
        - 실제 만기(30년 초과 포함)가 존재하는 경우 → 자본이 아닌 장기부채로 재분류될 리스크 평가
        - 공모 방식이 아닌 사모 위주일 경우 → 조기 상환청구(풋옵션) 가능성 및 투자자 집중도 분석 필요
        - yy1_below 또는 yy1_excess_yy5_below 중심일 경우 → 상환부담이 자본보다 부채에 가까움

        【효과적 활용 방법】
        - sm(총 미상환액)과 get_single_acc 결과의 자본총계 대비 비율 분석 → 외형상 자본 확충 효과 검증
        - yy30_excess 등 장기 만기 집중 시 실제 상환 가능성 낮고 회계상 자본 인정 비율 높음 → 신용등급 영향 분석
        - get_write_down_bond와 병행하여 상각형 조건 여부 파악 → 재무제표상 손실 가능성 여부 판단
        - remndr_exprtn2='공모' 중심일 경우 시장 신뢰성 확보 및 리파이낸싱 유리

        【주의사항 및 팁】
        - 신종자본증권은 회계상 자본으로 인정되지만, 실제 이자 지급 의무가 존재하는 경우 재무적 압박 요소로 작용할 수 있음
        - 영구채 구조라도 콜옵션 행사 시점 또는 금리 리픽싱 조건을 반드시 검토해야 실질 리스크를 평가할 수 있음
        - 일부 항목이 '-'일 경우 실제 미보유가 아닌 미공시 가능성 있으므로 원문 공시와 병행 검토 필요
        """,
    tags={"신종자본증권", "미상환", "잔액", "신종자본증권"}
)
def get_hybrid_securities_outstanding(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    신종자본증권 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020007
    """
    result = with_context(ctx, "get_hybrid_securities_outstanding", lambda context: context.ds002.get_hybrid_securities_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_conditional_capital_securities_outstanding",
    description="""상장법인 및 주요 비상장법인이 정기보고서를 통해 공시한 '상각형 조건부자본증권(Write-down Bonds)'의 잔존 만기별 미상환 잔액 정보를 조회하는 도구입니다.  
        이 도구는 특정 조건 충족 시 원금이 전액 또는 일부 상각되는 자본성 증권의 만기 구조를 분석하여, 향후 자본 건전성 훼손 위험 및 상각 리스크 집중 시점을 진단하는 데 활용됩니다.

        【핵심 제공 데이터】
        - remndr_exprtn1: 잔존 항목 구분 (고정값 '미상환잔액')
        - remndr_exprtn2: 발행 방식 (공모, 사모, 합계로 구분)
        - yy1_below ~ yy30_excess: 잔존 만기 구간별 미상환 잔액 (1년 이하부터 30년 초과까지)
        - sm: 총 미상환 잔액 (전 구간 합계)
        - stlm_dt: 결산 기준일 (데이터의 기준 시점)
        - corp_name / corp_code / corp_cls: 회사명, 고유번호, 법인 구분(Y: 유가, K: 코스닥 등)
        - rcept_no: 공시문서 연결용 접수번호 (공시뷰어 연동 가능)

        【연계 분석 도구】
        - get_write_down_bond: 해당 조건부자본증권의 상각 트리거 및 조건 구조 병행 확인
        - get_single_acc: 상각 증권 발행 이전과 이후 자본총계 변동 여부 분석
        - get_disclosure_list: 상각 조건 도달, 조기 상환, 조건 변경 등 주요 이벤트 공시 모니터링

        【활용 시나리오】
        - 특정 만기 구간(예: 5년 초과 ~ 10년 이하)에 잔액이 집중되어 있는 경우 → 해당 시점에 상각 리스크 집중 가능성 평가
        - remndr_exprtn2가 "사모"로 집중된 경우 → 외부 공시 부족 및 내부자 중심 조달 구조 우려 가능
        - sm 값이 기업 자본총계 대비 비정상적으로 클 경우 → 손실 발생 시 자본잠식 우려 조기 탐지
        - get_write_down_bond와의 연계 분석을 통해 실제 상각 조건(예: CET1 비율, 회계 손실 등)과 비교 가능

        【효과적 활용 방법】
        - yyN_excess 항목의 시계열 비교를 통해 상환 진행 속도 및 장기 리파이낸싱 리스크 추적
        - sm(총 잔액)을 get_single_acc의 자본총계와 비교하여 자본구조 내 위험도 비중 파악
        - remndr_exprtn2별 비교를 통해 공모 중심 조달인지, 비공개 사모 중심인지 파악해 시장 투명성 판단
        - stlm_dt 기준 직후의 get_disclosure_list 호출로 상각 또는 조건 변경 이력 추적

        【주의사항 및 팁】
        - "-" 값은 해당 구간에 미상환 잔액이 없음을 의미하며, 단일 "합계" 항목만 제공된 경우 세부 만기 구조는 생략되었을 수 있음
        - 상각형 조건부자본증권은 은행 등 금융기관에서 바젤Ⅲ 기준 충족용으로 발행하는 경우가 많으며, 자본 손실 시점에서 빠르게 부실 전이될 수 있어 모니터링 필요
        """,
    tags={"조건부", "자본증권", "미상환", "잔액"}
)
def get_conditional_capital_securities_outstanding(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    조건부 자본증권 미상환 잔액 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020008
    """
    result = with_context(ctx, "get_conditional_capital_securities_outstanding", lambda context: context.ds002.get_conditional_capital_securities_outstanding(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_accounting_auditor_opinion",
    description="""상장법인 및 주요 비상장법인이 제출한 정기보고서 내 감사인의 감사의견, 핵심감사사항, 강조사항 등을 조회하는 도구입니다.  
        감사의견 유형, 핵심 이슈, 감사보고서 특기사항을 분석함으로써 회계 신뢰성, 내부통제 위험, 기업 지속가능성에 대한 경고 신호를 탐지하는 데 활용됩니다.

        【핵심 제공 데이터】
        - adt_opinion: 감사의견 유형 (적정, 한정, 의견거절, 부적정 등)
        - adtor: 감사인 명칭 (회계법인 이름)
        - adt_reprt_spcmnt_matter: 감사보고서 특기사항 (2019년 12월 8일까지 사용)
        - emphs_matter: 감사인이 강조한 사항 (2019년 12월 9일부터 적용)
        - core_adt_matter: 핵심감사사항 (2019년 12월 9일부터 적용된 KAM: Key Audit Matters)
        - bsns_year: 대상 사업연도
        - stlm_dt: 결산 기준일 (해당 감사보고서 기준일)
        - corp_name / corp_code / corp_cls: 회사명, 고유번호, 법인 구분
        - rcept_no: 공시 원문 확인용 접수번호 (공시뷰어 연결 가능)

        【연계 분석 도구】
        - get_single_acc: 의견 거절, 한정 시 특정 재무항목의 오류 또는 왜곡 여부 검토
        - get_disclosure_list: 감사 관련 이슈에 대한 전후 공시 흐름 분석
        - get_executive_info: 감사의견 변화와 경영진 교체 이력 간 연관성 확인
        - get_investment_in_other_corp: 특기사항 또는 강조사항에 포함된 계열사 출자 관련 이슈 병행 검토

        【활용 시나리오】
        - adt_opinion이 '한정' 또는 '의견거절'일 경우 → 회계 신뢰도 훼손, 상장폐지 사유 가능성 평가
        - emphs_matter에 '계속기업 존속성 관련' 언급 → 재무적 위기 또는 사업 지속성 불확실성 경고 신호
        - core_adt_matter에 '매출 인식', '자산 가치평가' 등 반복 등장 → 회계처리 핵심 쟁점 지속 여부 판단
        - 감사인(adtor) 변경 시기와 의견 유형 변화 비교 → 독립성 훼손 또는 감사 품질 저하 가능성 탐지

        【효과적 활용 방법】
        - 핵심감사사항(core_adt_matter)의 키워드를 요약 분석하여 반복적 리스크 영역 추적
        - emphs_matter와 get_disclosure_list를 연계하여 특정 강조 이슈 관련 이사회 또는 공시 이벤트 병행 분석
        - 감사의견 유형(ad_opinion)이 전년도 대비 변화한 경우, get_single_acc로 영향을 받은 항목 확인
        - 감사법인(adtor) 변경 시기와 get_executive_info 비교를 통해 회계 투명성 변화 감지

        【주의사항 및 팁】
        - emphs_matter와 core_adt_matter는 2019년 12월 9일부터 적용된 기준으로, 이전 데이터는 adt_reprt_spcmnt_matter 항목 참고
        - 일부 보고서에서 의견 유형이나 감사인 정보가 "-"로 표시된 경우, 비공시 또는 누락 가능성이 있어 rcept_no 기반 원문 검토 필요
        """,
    tags={"회계감사인", "명칭", "감사의견", "회계감사인"}
)
def get_accounting_auditor_opinion(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회계감사인의 명칭 및 감사의견 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020009
    """
    result = with_context(ctx, "get_accounting_auditor_opinion", lambda context: context.ds002.get_accounting_auditor_opinion(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_audit_service_contract",
    description="""상장법인 및 주요 비상장법인이 제출한 정기보고서 내 '감사용역계약 체결내역'을 조회하는 도구입니다.  
        계약 당시 약정 보수 및 소요 시간과 실제 수행 결과의 차이를 분석하여, 회계감사의 독립성, 감사 품질, 감사인과의 유착 가능성 등을 평가하는 데 활용됩니다.

        【핵심 제공 데이터】
        - adtor: 감사인(회계법인) 명칭
        - cn: 계약 체결 내용 요약 (2020년 7월 5일까지 사용)
        - mendng / tot_reqre_time: 계약 당시 보수 및 소요 시간 (2020년 7월 5일까지 사용)
        - adt_cntrct_dtls_mendng / adt_cntrct_dtls_time: 계약 기준 보수 및 시간 (2020년 7월 6일부터 적용)
        - real_exc_dtls_mendng / real_exc_dtls_time: 실제 감사 수행 기준 보수 및 시간 (2020년 7월 6일부터 적용)
        - bsns_year: 감사 계약이 속한 사업연도
        - stlm_dt: 결산 기준일
        - corp_name / corp_code / corp_cls: 회사명, 고유번호, 법인구분
        - rcept_no: 공시 원문 확인용 접수번호

        【연계 분석 도구】
        - get_accounting_auditor_opinion: 감사보고서 의견 유형과 계약 이행 수준의 불일치 여부 분석
        - get_executive_info: 감사 계약 시점의 경영진 변동 여부 확인
        - get_disclosure_list: 감사 보수 변동, 계약 변경, 분쟁 등 관련 공시 확인

        【활용 시나리오】
        - 계약 보수와 실제 보수 간 큰 차이 존재 시 → 감사 범위 확대/축소, 계약 변경 여부 분석
        - real_exc_dtls_time이 과도하게 낮은 경우 → 감사 품질 저하 또는 감사지연 우려
        - 특정 연도부터 감사인이 변경되고 보수 급증한 경우 → 회계처리 복잡성 또는 경영진의 전략 변경 가능성
        - 감사인(adtor)이 동일함에도 보수 증감폭이 큰 경우 → 내부 통제 취약 영역 증가 여부 점검

        【효과적 활용 방법】
        - adt_cntrct_dtls_mendng과 real_exc_dtls_mendng 비교로 감사 보수 이행 여부 분석
        - adt_cntrct_dtls_time과 real_exc_dtls_time 차이를 통해 감사 범위 변경 또는 이행 지연 여부 판단
        - 다년간 데이터 비교를 통해 감사인 교체 전후 보수 및 소요시간 추이 분석
        - get_accounting_auditor_opinion의 감사의견 유형과 교차 분석하여 감사 결과의 신뢰성 판단

        【주의사항 및 팁】
        - 2020년 7월 6일 이전 보고서의 경우, 과거 필드(mendng, tot_reqre_time)를 사용하고 이후 보고서에서는 새로운 필드로 분리됨
        - "-"로 표시된 값은 해당 연도의 감사계약 내역이 미공시되었거나 공시 대상이 아님을 의미하므로 rcept_no 기준 원문 공시 확인 권장
        """,
    tags={"감사용역", "체결", "현황", "감사용역"}
)
def get_audit_service_contract(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    감사용역체결현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020010
    """
    result = with_context(ctx, "get_audit_service_contract", lambda context: context.ds002.get_audit_service_contract(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_non_audit_service_contract",
    description="""상장법인 및 주요 비상장법인이 공시한 비감사용역(Non-Audit Service) 계약 내역을 조회하는 도구입니다.  
        회계법인 또는 그 계열사와 체결한 자문, 세무, 시스템 구축 등 비감사계약 정보를 바탕으로, 감사인의 독립성 훼손 여부, 이해상충 가능성, 과도한 외부용역 의존도 등을 분석하는 데 활용됩니다.

        【핵심 제공 데이터】
        - cntrct_cncls_de: 계약 체결일
        - servc_cn: 용역 내용 (예: 세무자문, 시스템 구축, 내부통제 컨설팅 등)
        - servc_exc_pd: 용역 수행 기간
        - servc_mendng: 계약 금액(용역 보수)
        - rm: 기타 비고사항 (특수관계 여부, 지적 재산권 귀속 등)
        - bsns_year: 해당 계약이 속한 사업연도
        - stlm_dt: 결산 기준일 (데이터 기준 시점)
        - corp_name / corp_code / corp_cls: 회사명, 고유번호, 법인구분
        - rcept_no: 공시 원문 확인용 접수번호

        【연계 분석 도구】
        - get_audit_service_contract: 동일 회계법인과의 감사 계약 여부 확인 → 독립성 훼손 가능성 진단
        - get_accounting_auditor_opinion: 감사의견이 적정이 아님에도 비감사용역 계약 유지 여부 확인
        - get_disclosure_list: 관련 이해관계자 거래나 계약 변경 공시 추적
        - get_executive_info: 특정 용역과 경영진 간 이해관계 유무 탐색

        【활용 시나리오】
        - servc_cn에 '내부통제 컨설팅' 포함 + 감사계약 유지 → 내부자 거래성 및 독립성 훼손 리스크
        - servc_mendng(보수) 규모가 감사계약 대비 과도할 경우 → 경제적 종속성에 따른 감사 왜곡 우려
        - 계약일자(cntrct_cncls_de)와 감사의견(ad_opinion) 사이 시점 분석 → 계약 영향 여부 탐색
        - rm 항목에 지분 보유 관계, 계열사 관계 등 표기된 경우 → 사적 이해관계 가능성 검토

        【효과적 활용 방법】
        - 감사인(adtor)이 동일한 상황에서 get_audit_service_contract와 servc_mendng을 비교하여 경제적 의존도 측정
        - get_disclosure_list와 병행 조회하여, 계약 체결 시 이사회 결의 또는 공시 여부 확인
        - 특정 회계법인과의 반복 계약 여부를 다년도 추적으로 파악하여 장기적 의존 리스크 평가
        - servc_exc_pd가 장기화된 경우 → 비감사용역이 기업 의사결정에 과도하게 관여하고 있을 가능성 분석

        【주의사항 및 팁】
        - "-"로 표기된 항목은 해당 연도에 비감사용역 공시가 없거나 생략되었을 수 있으며, rcept_no 기반 원문 확인 권장
        - 회계법인의 계열사 명의로 계약된 경우에도 독립성 침해로 간주될 수 있어 용역 제공 주체 명시 여부에 주의 필요
        """,
    tags={"회계감사인", "비감사용역", "계약", "현황"}
)
def get_non_audit_service_contract(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회계감사인과의 비감사용역 계약체결 현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020011
    """
    result = with_context(ctx, "get_non_audit_service_contract", lambda context: context.ds002.get_non_audit_service_contract(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_outside_director_status",
    description="""상장법인 및 주요 비상장법인이 정기보고서를 통해 공시한 사외이사 현황을 조회하는 도구입니다.  
        사외이사 수, 전체 이사 대비 비율, 선임 및 퇴임 현황 등의 정보를 기반으로, 이사회 독립성 수준, 지배구조 감시 기능, 사외이사 유지율 등을 진단하는 데 활용됩니다.

        【핵심 제공 데이터】
        - drctr_co: 전체 이사 수
        - otcmp_drctr_co: 사외이사 수
        - apnt: 당해 연도 사외이사 선임 수
        - rlsofc: 당해 연도 사외이사 해임 수
        - mdstrm_resig: 당해 연도 사외이사 중도퇴임 수
        - stlm_dt: 결산 기준일
        - corp_name / corp_code / corp_cls: 회사명, 고유번호, 법인구분
        - rcept_no: 공시 원문 확인용 접수번호 (공시뷰어 연결 가능)

        【연계 분석 도구】
        - get_executive_info: 이사회 내 사내이사와의 관계 분석, 경영진 교체 흐름 확인
        - get_disclosure_list: 사외이사 선임·해임과 관련된 이사회 결의 및 주주총회 공시 이력 확인
        - get_audit_committee: 감사위원회 구성과 사외이사 겸직 여부 확인
        - get_major_shareholder: 최대주주 지분율과 사외이사 독립성 간 상관관계 분석

        【활용 시나리오】
        - otcmp_drctr_co / drctr_co 비율이 낮은 경우 → 이사회 독립성 미달로 경영 감시 기능 약화 우려
        - apnt이 많고 mdstrm_resig도 많은 경우 → 사외이사 교체 빈도가 높아 독립성 및 지속성 부족 신호
        - rlsofc 발생 후 감사의견이 부정적으로 바뀐 경우 → 사외이사 교체가 내부 통제 악화와 연계되었을 가능성
        - drctr_co 수는 유지되나 otcmp_drctr_co가 감소한 경우 → 의도적인 사외이사 축소 여부 점검

        【효과적 활용 방법】
        - 사외이사 수를 전체 이사 수 대비 비율로 계산하여 독립성 확보 수준 정량 평가
        - apnt과 rlsofc, mdstrm_resig 항목을 시계열로 비교하여 사외이사 유지율 및 이직율 분석
        - get_disclosure_list와 연결하여 선임 당시 배경(주주제안, 이사회 추천 등)과 해임 사유 확인
        - get_audit_committee와 교차 분석하여 감사위원회 기능이 사외이사 중심으로 유지되고 있는지 확인

        【주의사항 및 팁】
        - 사외이사 수가 법적 최소 기준(자산 2조 이상 상장사: 3인 이상, 과반 이상) 미달 시 규제 위반 가능성 있음
        - mdstrm_resig 값이 높고 비고에 사유가 없는 경우, 강제성 퇴임 또는 내부 갈등 가능성 의심
        - '-' 값은 해당 연도에 공시 생략 또는 미제공일 수 있으므로 원문 공시(rcept_no) 확인 필요
        """,
    tags={"사외이사", "변동", "현황", "사외이사"}
)
def get_outside_director_status(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    사외이사 및 그 변동현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020012
    """
    result = with_context(ctx, "get_outside_director_status", lambda context: context.ds002.get_outside_director_status(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_unregistered_exec_compensation",
    description="""상장법인 및 주요 비상장법인이 제출한 사업보고서에서 미등기임원에 대한 보수 내역을 조회하는 도구입니다. 
        등기되지 않은 임원에게 지급된 연간 보수 총액과 인원, 1인당 평균 보수를 확인할 수 있어, 내부자 보상의 투명성, 보상 집중도, 인건비 부담 수준 등을 분석하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 인원수(nmpr): 미등기임원 수를 통해 보상 대상 범위 파악
        - 연간급여 총액(fyer_salary_totamt): 미등기임원에 지급된 연간 총보수로, 보상 규모 분석에 활용
        - 1인 평균 급여(jan_salary_am): 평균 보상 수준을 통해 보상의 과다 여부 또는 형평성 이슈 판단
        - 구분(se): '미등기임원'으로 고정되어, 등기임원 보수와의 비교 가능
        - 결산기준일(stlm_dt): 분석 기준 시점 명시

        【연계 분석 도구】
        - get_individual_compensation: 등기임원 보수와 비교하여 내부자 보상 격차 분석
        - get_employee_info: 일반 직원 평균 급여와 비교하여 보상 구조의 적절성 검토
        - get_total_compensation: 등기임원 전체 보수 대비 미등기임원 보수 비중 분석
        - get_disclosure_list: 보상 변경 관련 이사회 결의나 주주총회 안건 확인

        【활용 시나리오】
        - jan_salary_am 값이 지나치게 높을 경우, 사실상 경영 의사결정 권한을 가진 인물에게 등기 없이 고액 보상이 이루어지는지 분석
        - fyer_salary_totamt이 급증한 경우, 일시적 인센티브 지급 또는 퇴직금 지급 가능성 확인
        - get_employee_info와 비교하여 임직원 간 보수 격차 및 조직 내 보상 불균형 여부 평가
        - 동일 기업에서 등기임원 보수(get_total_compensation)와 비교하여 미등기임원의 영향력 과대 가능성 탐지

        【효과적 활용 방법】
        - nmpr(인원수)와 fyer_salary_totamt을 기반으로 직무무관한 평균급여 상승 여부 판단
        - jan_salary_am이 일반 직원 평균 급여 대비 수 배 이상일 경우, 내부자 보상 통제 구조의 미흡 가능성 평가
        - stlm_dt 기준으로 연도별 추이를 비교 분석하여 보상 구조 변화 및 집중도 분석
        - get_disclosure_list를 병행하여 미등기임원 보수 관련 규정 변경, 보상정책 개편 여부 탐색

        【주의사항 및 팁】
        - 미등기임원 보수는 이사회 승인 없이 결정될 수 있어, 지배주주 또는 내부자 편의 지급 여부에 대한 모니터링 필요
        - 비고(rm) 항목은 보통 공란이지만, 특수 상황이 기재되는 경우 상세 검토 필요
        """,
    tags={"미등기임원", "보수", "현황", "미등기임원"}
)
def get_unregistered_exec_compensation(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    미등기임원 보수현황 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020013
    """
    result = with_context(ctx, "get_unregistered_exec_compensation", lambda context: context.ds002.get_unregistered_exec_compensation(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_executive_compensation_approved",
    description="""상장법인 및 주요 비상장법인이 사업보고서에서 공시한 '임원 보수에 대한 주주총회 승인 금액' 내역을 조회하는 도구입니다. 
        등기이사, 사외이사, 감사위원 등에 대해 주총에서 사전 승인된 보수 한도를 통해 기업의 보상 지배구조, 투명성 수준, 주주통제력 강도 등을 평가하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 구분(se): 등기이사, 사외이사, 감사위원 등의 대상 구분
        - 인원수(nmpr): 각 직위별 보수 한도 적용 인원 수
        - 주주총회 승인금액(gmtsck_confm_amount): 해당 연도에 주총에서 승인된 전체 보수 한도
        - 결산기준일(stlm_dt): 승인 기준 시점
        - 비고(rm): 특이사항 기재

        【연계 분석 도구】
        - get_total_compensation: 실제 지급된 등기임원 보수 총액과 비교하여 승인 한도 대비 집행 수준 분석
        - get_individual_compensation_amount: 상위 5인 보수 수령자와 승인 한도와의 관계 파악
        - get_disclosure_list: 보수 한도 변경, 이사회 결의 내용, 보상위원회 관련 공시 확인
        - get_executive_info: 승인된 인원 수(nmpr)와 실제 등기임원 재직자 수 비교

        【활용 시나리오】
        - gmtsck_confm_amount 값이 '-'이거나 비정상적으로 낮은 경우 → 보수 한도 미승인 또는 공시 누락 여부 검토
        - se가 '계'로 표시된 항목을 중심으로 승인 총액 확인 → 개별 직위별 세부 분석 가능
        - get_total_compensation과의 비교를 통해 실제 집행률 평가 → 보수 초과 집행 여부 탐지
        - 결산기준일을 기준으로 해마다 gmtsck_confm_amount의 변동 추이 분석 → 보수정책 변화 여부 파악

        【효과적 활용 방법】
        - '계' 항목의 승인총액과 get_total_compensation의 총액을 비교해 집행률 산출
        - se 항목을 기준으로 감사위원, 사외이사 등 특정 직위에 과도한 한도 설정 여부 검토
        - 결산기준일(stlm_dt) 기준으로 동일 연도의 실제 보수 지급 내역과 비교하여 주총 승인 범위 내 집행 여부 판단
        - 보수 승인 금액이 대폭 상향된 경우, get_disclosure_list로 관련 이사회 결의 내용 병행 분석

        【주의사항 및 팁】
        - gmtsck_confm_amount가 '-'로 표기된 경우, 주총 승인 없거나 보고 누락 가능성 있으므로 추가 공시 병행 검토 필요
        - 계 항목 외 세부 구분별 항목은 별도 분석 대상으로 활용 가능하며, 실제 지급 내역과 교차 확인이 중요
        """,
    tags={"이사", "감사", "보수", "현황"}
)
def get_executive_compensation_approved(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    이사·감사 전체의 보수현황 (주주총회 승인금액) 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020014
    """
    result = with_context(ctx, "get_executive_compensation_approved", lambda context: context.ds002.get_executive_compensation_approved(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_executive_compensation_by_type",
    description="""사업보고서 내 등기이사, 사외이사, 감사위원회 위원 등 임원 유형별 보수 지급 내역을 조회하는 도구입니다. 
        직책별 인원 수, 보수총액, 1인당 평균 보수액 등을 구분하여 제공함으로써 보상 구조의 합리성, 특정 직위에 대한 과도한 보상 집중 여부, 지배구조 상의 리스크 등을 파악하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 구분(se): 등기이사, 사외이사, 감사위원 등 직책별 구분
        - 인원수(nmpr): 각 직책별 보수 수령 대상 인원 수
        - 보수총액(pymnt_totamt): 급여, 상여, 퇴직금 등을 포함한 총 보수 지급 금액
        - 1인당 평균 보수(psn1_avrg_pymntamt): 평균 수준의 보상 규모로, 과다 보상 여부 판단에 활용
        - 결산기준일(stlm_dt): 해당 정보의 기준 시점

        【연계 분석 도구】
        - get_executive_compensation_approved: 주주총회 승인 보수 한도와 비교해 집행률 분석
        - get_total_compensation: 전체 등기임원 보수 총액과 교차 분석하여 직위별 구성비 파악
        - get_individual_compensation: 개별 고액 수령 임원과의 보수 집중도 비교
        - get_executive_info: 동일 인물의 직위 및 역할과 보상 간의 적정성 평가

        【활용 시나리오】
        - 등기이사 평균 보수(psn1_avrg_pymntamt)가 과도하게 높을 경우, 내부 지배구조 문제 또는 단기성과 중심 보상체계 여부 평가
        - 사외이사 또는 감사위원 보수가 지나치게 낮거나 높을 경우, 명목직 여부 또는 이해상충 가능성 탐색
        - '감사' 항목이 '-'로 표시된 경우, 해당 직위에 대한 보수 미지급 또는 공시 누락 여부 검토
        - get_executive_compensation_approved의 승인 한도와 비교하여 직위별 집행률 차이 분석

        【효과적 활용 방법】
        - 직책별 pymnt_totamt 비중을 시각화하여 특정 직위에 대한 보수 집중 여부 분석
        - 평균 보수(psn1_avrg_pymntamt)를 동일 기업 내 직위 간 비교하여 내부 형평성 확인
        - stlm_dt 기준으로 연도별 비교 시, 특정 직위의 보수 급증 여부 파악 가능
        - 등기이사 중 일부가 사외이사나 감사위원으로 이중 역할을 수행하는 경우, get_executive_info와 병행 분석

        【주의사항 및 팁】
        - '감사', '계' 등 se 항목이 '-' 또는 생략된 경우, 실제 공시 누락이거나 지급 내역 없음 가능성 있음
        - 인원수(nmpr)가 '0' 또는 '-'로 기재되었더라도 pymnt_totamt가 있는 경우, 집계 오류 또는 공시 오류 가능성 있으므로 get_disclosure_list와 함께 해석 권장
        """,
    tags={"이사", "감사", "보수", "현황"}
)
def get_executive_compensation_by_type(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    이사·감사 전체의 보수현황 (보수지급금액 - 유형별) 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020015
    """
    result = with_context(ctx, "get_executive_compensation_by_type", lambda context: context.ds002.get_executive_compensation_by_type(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_public_capital_usage",
    description="""상장법인 및 주요 비상장법인이 유상증자, 전환사채 발행 등으로 조달한 자금(capital)의 사용 계획과 실제 사용 내역을 조회하는 도구입니다. 
        자금 운용 계획 대비 집행 현황을 분석하여, 운용의 투명성, 계획 대비 이탈 여부, 내부통제 리스크를 평가하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 구분(se_nm): 공시 대상 구분 (예: 유상증자, 전환사채 등)
        - 회차(tm): 자금 조달의 회차 정보
        - 납입일(pay_de): 조달 자금 납입일
        - 납입금액(pay_amount): 해당 회차 조달된 금액
        - 자금사용 계획(on_dclrt_cptal_use_plan, rs_cptal_use_plan_useprps, rs_cptal_use_plan_prcure_amount): 증권신고서상 계획된 자금 사용 용도와 조달금액
        - 실제 사용 현황(real_cptal_use_sttus, real_cptal_use_dtls_cn, real_cptal_use_dtls_amount): 실제 집행 내역과 금액
        - 차이 발생 사유(dffrnc_occrrnc_resn): 계획 대비 실제 사용의 차이 발생 원인
        - 결산기준일(stlm_dt): 데이터 기준 시점

        【연계 분석 도구】
        - get_paid_in_capital_increase: 자금조달(유상증자) 내역과 연결하여 조달금액 및 사용계획 적정성 검토
        - get_convertible_bond: 전환사채 발행으로 조달한 자금 사용계획과 실제 집행 비교
        - get_disclosure_list: 자금사용계획 변경 승인 이력, 변경 공시 추적
        - get_single_acc: 자금 운용 이후 재무제표상 자산·부채 변동사항 분석

        【활용 시나리오】
        - 실제 자금 사용 내역이 계획과 불일치할 경우 → 자금 전용, 내부통제 실패 가능성 탐지
        - pay_amount와 real_cptal_use_dtls_amount를 비교하여 납입 후 미집행 여부 탐색
        - dffrnc_occrrnc_resn을 통해 사용 변경 사유의 적절성 평가
        - get_paid_in_capital_increase 연계 분석으로 조달 목적(부채상환, 시설투자 등)과 실제 용도 일치 여부 점검

        【효과적 활용 방법】
        - 계획 대비 실제 집행 비율(Deviation Rate) 계산
        - pay_de 기준으로 자금 운용 지연 여부 분석
        - 자금 미사용분 또는 사용변경 이력(get_disclosure_list) 병행 조회
        - 동일 회차(tm)별 자금 흐름 시계열 정리로 전체 사용 추이 분석

        【주의사항 및 팁】
        - 2018년 1월 18일 이전과 이후 공시 양식이 다르므로, 데이터 제공 항목에 주의
        - '-'로 표시된 항목은 공시 생략 또는 해당 없음일 수 있어 신중한 해석 필요
        - 자금사용계획 변경 시 반드시 관련 공시(get_disclosure_list)로 추가 확인 필요
        """,
    tags={"공모자금", "사용", "내역", "자금사용"}
)
def get_public_capital_usage(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    공모자금의 사용내역 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020016
    """
    result = with_context(ctx, "get_public_capital_usage", lambda context: context.ds002.get_public_capital_usage(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_private_capital_usage",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 제3자배정 유상증자 등 사모자금 조달 이후 자금사용 계획 및 실제 사용내역을 조회하는 도구입니다.
        기업이 사모방식으로 조달한 자금을 어떻게 계획하고 실제로 집행했는지를 비교 분석하여, 자금집행 리스크, 계획과 실행 간 괴리, 숨은 유동성 위기 가능성을 평가하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 자금사용계획(cptal_use_plan, mtrpt_cptal_use_plan_useprps, mtrpt_cptal_use_plan_prcure_amount): 주요사항보고서에 명시된 자금 사용계획 및 조달금액
        - 실제자금사용현황(real_cptal_use_sttus, real_cptal_use_dtls_cn, real_cptal_use_dtls_amount): 실제 자금 집행 내역 및 금액
        - 차이발생사유(dffrnc_occrrnc_resn): 계획 대비 실제 집행의 차이 발생 사유
        - 납입일(pay_de) 및 납입금액(pay_amount): 자금조달 시점 및 금액
        - 회차정보(tm), 구분(se_nm): 사모자금 조달 유형 및 구분 정보
        - 결산기준일(stlm_dt): 분석 기준 시점
        - 접수번호(rcept_no): 공시 상세 조회용 식별자

        【연계 분석 도구】
        - get_paid_in_capital_increase: 동일 시기 유상증자 세부 조건 비교 분석
        - get_single_acc: 자금 조달 및 집행 이후 재무제표 변동 심층 분석
        - get_disclosure_list: 사모자금 집행 이후 추가 공시사항(변경공시 등) 모니터링

        【활용 시나리오】
        - 자금 사용 계획(mtrpt_cptal_use_plan_useprps)과 실제 집행내역(real_cptal_use_dtls_cn) 비교로 계획 이행률 평가
        - 조달 자금이 단기 차입금 상환이나 운영자금으로 전용된 경우, 유동성 압박 가능성 사전 탐지
        - 차이발생 사유(dffrnc_occrrnc_resn) 분석을 통해 사업 추진 실패, 계획 변경 등 리스크 요인 파악
        - 납입일(pay_de)과 결산기준일(stlm_dt) 간의 시차를 고려하여 자금 운용 지연 여부 평가
        - get_disclosure_list를 통해 자금 운용 변경이나 추가 차입 가능성 병행 탐색

        【효과적 활용 방법】
        - 자금사용 계획 대비 실제 집행 비율을 수치화하여 계획 신뢰성 평가
        - 사용계획 항목별 집행 여부를 검토하여 사업 진척도 및 실패 위험 조기 경고
        - 차이발생 사유가 빈번할 경우, 재무구조 불안정성 및 경영계획 부실 가능성 추가 분석
        - get_single_acc 호출로 자금 집행 이후 부채비율 및 유동성 지표 변동 교차 확인

        【주의사항 및 팁】
        - 2019년 1월 19일 이후 공시는 mtrpt_cptal_use_plan_useprps 항목을 기준으로 분석해야 하며, 그 이전 공시는 cptal_use_plan, real_cptal_use_sttus 기준으로 분석해야 합니다.
        - 납입금액(pay_amount)이 "-"로 표시된 경우, 실제 납입이 이루어지지 않은 사례일 수 있어 주의가 필요합니다.
        """,
    tags={"사모자금", "사용", "내역", "사모자금"}
)
def get_private_capital_usage(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    사모자금의 사용내역 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bsns_year (str): 사업연도 (예: 2024)
        reprt_code (str): 보고서코드 (예: 11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020017
    """
    result = with_context(ctx, "get_private_capital_usage", lambda context: context.ds002.get_private_capital_usage(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    ))
    return TextContent(type="text", text=str(result))
