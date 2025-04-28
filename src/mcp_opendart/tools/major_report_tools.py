import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")
@mcp.tool(
    name="get_asset_transfer",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 자산양수도(기타) 및 풋백옵션 계약에 관한 주요 정보를 조회하는 도구입니다. 기업의 대규모 자산거래, 사업재편, 위험 관리 전략 등을 빠르게 파악할 수 있으며, 풋백옵션 조건 유무를 통해 거래 이후의 재무 리스크까지 분석할 수 있습니다.\n\n【핵심 제공 데이터】\n- 계약일자(ctrct_de): 양수도 계약 체결일\n- 자산명(asset_nm): 양수/양도 대상 자산명\n- 양수/양도 구분(trf_und_cd_nm): 거래 방향 구분(양수/양도)\n- 양수/양도 금액(trf_und_amt): 실제 거래 금액\n- 계약상대방(cntrct_opnt_nm): 계약 체결 상대 기업명\n- 풋백옵션 유무(putback_option_exist_yn): 옵션 존재 여부\n- 풋백옵션 조건(putback_option_cndt): 풋백 옵션 관련 조건 상세\n\n【분석 활용 특징】\n- 기업의 대규모 자산 이동 여부를 통해 사업구조 재편 여부 사전 탐지\n- 양수/양도 구분을 통해 성장 투자 vs 구조조정 여부 판단 가능\n- 풋백옵션 조건 분석을 통해 거래 이후 잠재적 재무 리스크(회수요건 등) 파악\n- 계약상대방 정보로 거래 상대방의 신용도 및 연관 리스크 분석 가능\n\n【연계 분석 도구】\n- get_business_acquisition: 영업양수도 계약 여부 병행 분석\n- get_tangible_asset_transfer, get_tangible_asset_acquisition: 유형자산 양수/양도 결정과 연계 분석\n- get_disclosure_list: 관련 주요사항보고서 전체 맥락 추적\n- get_single_acc: 자산 매각 또는 취득에 따른 재무제표 변동 확인\n- get_major_holder_changes: 대규모 자산거래 이후 대주주 지분 변동 여부 확인\n\n【활용 시나리오】\n- 자산 매각으로 단기 부채상환 자금을 마련하는 구조조정 분석\n- 신규 자산 투자(공장, 설비 등) 여부를 통한 성장 전략 확인\n- 풋백옵션이 설정된 경우, 미래 재무부담(회수 위험)을 평가\n- 거래 상대방 신용도 및 연관 리스크를 기반으로 계약 안정성 평가\n- 대규모 자산 이동 이후 재무상태표 상 주요 항목(자산총계, 부채총계) 변동 추적\n\n【효과적 활용 방법】\n- trf_und_cd_nm으로 양수/양도 방향을 구분하여 분석 초점 설정\n- 풋백옵션 존재 시, 향후 회수 조건과 이행 가능성을 별도로 검토\n- get_single_acc로 해당 자산 항목의 재무제표 반영 변동 확인\n- 연계 공시(get_disclosure_list)를 통해 추가 조건이나 후속 계약 여부 탐색",
    tags={"주요사항보고서", "자산양수도", "풋백옵션", "주요정보"}
)
def get_asset_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자산양수도(기타), 풋백옵션 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020018
    """
    result = with_context(ctx, "get_asset_transfer", lambda context: context.ds005.get_asset_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_bankruptcy",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 부도발생 사실을 공시한 내역을 조회하는 도구입니다. 기업의 신용리스크, 재무위험 발생 여부를 조기에 탐지할 수 있으며, 부도 사유 및 관련 채권자 정보를 기반으로 기업 파산 가능성 및 구조조정 리스크를 평가하는 데 활용됩니다.\n\n【핵심 제공 데이터】\n- 부도발생일자(failure_de): 부도 발생이 확정된 일자\n- 부도사유(failure_rsn): 부도 발생 원인에 대한 설명\n- 채권자명(creditor_nm): 부도와 관련된 주요 채권자\n- 부도금액(failure_amt): 부도에 해당하는 채무 금액\n- 기타사항(etc): 부도 관련 추가 설명\n\n【분석 활용 특징】\n- 부도발생일자와 부도금액을 통해 즉시 신용리스크 수준 파악\n- 부도사유 분석을 통해 일회성 부도인지, 구조적 재무위기인지 구분\n- 채권자 정보를 통해 부도 연쇄 위험도(시스템 리스크) 사전 탐지\n- 기타사항을 활용하여 추가적 경영진 대응방향, 후속 조치 가능성 평가\n\n【연계 분석 도구】\n- get_business_suspension: 영업정지 공시와 연계하여 사업중단 리스크 확인\n- get_rehabilitation: 회생절차 개시 여부 확인하여 파산 가능성 평가\n- get_dissolution: 해산사유 발생 공시 여부와 연계 분석\n- get_major_holder_changes: 부도 이후 주요주주 지분 변동 여부 모니터링\n- get_executive_trading: 부도 전후 임원 주식 매매 패턴 분석\n- get_single_acc: 부도 발생 기업의 전체 재무상태표 심층 분석\n\n【활용 시나리오】\n- 부도 발생 즉시 해당 기업에 대한 신용등급 하향 리스크 사전 탐지\n- 채권자 정보 분석을 통한 대손충당금 설정 필요성 평가\n- 연쇄부도 가능성 판단을 위한 관련 채권자 및 주요 계열사 위험 모니터링\n- 부도 금액 및 부도 사유에 따른 회생 가능성, 청산 가능성 분기점 평가\n- 부도기업 인수/합병 검토 시 기초 데이터로 활용\n\n【효과적 활용 방법】\n- failure_amt(부도금액) 규모에 따라 그룹 전체 리스크 여부 판단\n- failure_rsn(부도사유) 분석을 통해 구조적 부실(예: 유동성 부족, 사업 실패) 여부 확인\n- creditor_nm(채권자명) 정보로 거래 은행, 대출기관 리스트 확보\n- get_rehabilitation, get_business_suspension와 연계하여 후속조치 진행 여부 점검",
    tags={"주요사항보고서", "부도발생", "주요정보", "부도"}
)
def get_bankruptcy(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    부도발생 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020019
    """
    result = with_context(ctx, "get_bankruptcy", lambda context: context.ds005.get_bankruptcy(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_business_suspension",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 영업정지 사실을 공시한 내역을 조회하는 도구입니다. 사업의 일시적 또는 영구적 정지 여부를 신속하게 파악할 수 있으며, 기업의 존속 가능성, 수익성 감소 리스크, 부도 및 구조조정 가능성을 조기에 진단하는 데 활용됩니다.\n\n【핵심 제공 데이터】\n- 영업정지사유(bsnsp_stop_rsn): 영업정지 발생 원인\n- 영업정지기간(bsnsp_stop_pd): 영업정지 적용 기간\n- 영업정지대상부문(bsnsp_stop_part): 정지된 사업 부문\n- 정지영향 및 향후대책(rspn_matter): 영업정지가 기업 재무에 미치는 영향 및 대응방안\n\n【분석 활용 특징】\n- 정지사유를 통해 일시적 문제인지, 구조적 사업 부진인지 구분\n- 영업정지기간과 사업부문을 통해 매출 타격 규모 추정\n- 정지영향 및 대응계획을 분석하여 경영진 대응 역량 평가\n- 영업정지 공시 후 연쇄 리스크(부도, 해산, 회생절차) 가능성 조기 탐지\n\n【연계 분석 도구】\n- get_bankruptcy: 영업정지 이후 부도발생 가능성 추적\n- get_rehabilitation: 영업정지 후 회생절차 개시 여부 분석\n- get_dissolution: 영업정지 장기화 시 해산 절차 진행 여부 검토\n- get_single_acc: 영업정지 사업부문 관련 자산/부채 세부 내역 분석\n- get_disclosure_list: 영업정지 관련 추가 공시자료 확인\n\n【활용 시나리오】\n- 영업정지된 주요 사업부문 분석을 통한 전체 기업 존속성 평가\n- 정지사유가 산업 전체 문제인지, 기업 특수 사유인지 식별\n- 매출 비중이 높은 사업부문 정지 시, 전체 수익성 급감 리스크 평가\n- 영업정지 후 경영진 대응방안을 확인하여 향후 회생 가능성 판단\n- 영업정지 이후 부도, 회생절차, 해산공시 여부를 체계적으로 모니터링\n\n【효과적 활용 방법】\n- bsnsp_stop_part(정지대상 부문)과 bsnsp_stop_pd(정지기간) 분석으로 실질적 매출 타격 규모 추정\n- 정지영향(rspn_matter) 검토를 통해 후속 재무제표 변동 가능성 사전 예측\n- get_single_acc로 해당 부문 관련 자산, 부채 항목을 심층 확인\n- get_bankruptcy, get_rehabilitation와 연계하여 추가 위험 신호 조기 포착",
    tags={"주요사항보고서", "영업정지", "주요정보", "정지"}
)
def get_business_suspension(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    영업정지 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020020
    """
    result = with_context(ctx, "get_business_suspension", lambda context: context.ds005.get_business_suspension(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_rehabilitation",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 회생절차 개시신청 사실을 공시한 내역을 조회하는 도구입니다. 회생신청 시점, 사유, 진행상황을 종합적으로 파악하여 기업 존속 가능성과 투자 위험도를 조기에 평가할 수 있습니다.\n\n【핵심 제공 데이터】\n- 신청일자(receipt_de): 회생신청 시점으로 재무위기 발생 시기와 대응 속도 분석\n- 신청사유(rsn): 유동성 위기, 구조적 부실 등 위기의 근본 원인 파악\n- 법원명(court_nm): 관할 법원 특성에 따른 회생절차 속도와 처리 가능성 참고\n- 신청기업명(applicant_nm): 회생신청 주체 확인 및 그룹 연관성 분석\n- 진행현황(process_sttus): 회생계획 승인, 폐지 여부 등 리스크 실시간 모니터링\n\n【연계 분석 도구】\n- get_bankruptcy: 부도 발생과 연계하여 회생신청 여부 추적\n- get_business_suspension: 영업정지와 병행 발생 여부 확인\n- get_dissolution: 회생 실패 시 해산 공시로 전이 여부 탐색\n- get_single_acc: 회생 전후 재무제표의 자산, 부채 구조 심층 분석\n- get_major_holder_changes: 회생신청 전후 대주주 지분 변동 모니터링\n\n【활용 시나리오】\n- 회생신청 기업을 조기에 선별하여 대손충당금 설정 또는 투자회수 전략 수립\n- 신청사유를 분석하여 기업 존속 가능성(구조조정 통한 회생 vs 청산)을 평가\n- 회생계획 진행 상황 모니터링을 통해 신용등급 변동 사전 대응\n- 부채규모와 자산규모 비교를 통한 실질적 회생 가능성 판단\n- 투자자산 중 회생절차 기업 존재 여부를 사전 모니터링하여 위험 최소화\n\n【효과적 활용 방법】\n- 신청사유(rsn)를 분류하여 재무구조 악화 원인 구체적으로 분석\n- 진행현황(process_sttus) 변동을 주기적으로 체크하여 청산리스크 사전 감지\n- 회생신청 기업에 대한 get_single_acc 기반 자산/부채 구조 세부 분석\n- get_bankruptcy, get_dissolution와 연계하여 파산·청산 가능성 예측",
    tags={"주요사항보고서", "회생절차", "주요정보", "회생"}
)
def get_rehabilitation(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회생절차 개시신청 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020021
    """
    result = with_context(ctx, "get_rehabilitation", lambda context: context.ds005.get_rehabilitation(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_dissolution",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 해산사유 발생 사실을 공시한 내역을 조회하는 도구입니다. 기업의 법적 해산 절차 진행 여부를 조기에 파악할 수 있으며, 해산 원인과 시점을 기반으로 기업 존속성 상실 위험을 평가하고, 투자자산의 회수 전략을 수립하는 데 활용됩니다.\n\n【핵심 제공 데이터】\n- 해산사유 발생일자(dissolution_occur_de): 해산사유가 최초로 발생한 시점\n- 해산사유(dissolution_rsn): 자발적 해산, 법정 해산 등 해산 발생의 근본 원인\n- 해산결정일자(dissolution_de): 이사회 또는 주주총회에서 공식 해산 결정이 내려진 날짜\n- 해산유형(dissolution_type): 합병, 청산, 기타 해산 유형 구분\n- 기타사항(etc): 해산 이후 청산절차, 남은 채권·채무 처리 방향 등 추가정보\n\n【연계 분석 도구】\n- get_bankruptcy: 부도 이후 해산 절차로 연결되는 경우 연계 분석\n- get_rehabilitation: 회생절차 실패 후 해산으로 전이되는 흐름 모니터링\n- get_single_acc: 해산 전후 자산/부채 구조 및 청산 가능 자산 규모 심층 분석\n- get_major_holder_changes: 해산 과정 중 주요주주 지분 변동 탐지\n\n【활용 시나리오】\n- 해산사유를 분석하여 자발적 청산(구조조정)인지, 강제 청산(부도/파산)인지 식별\n- 해산결정일자 기준으로 투자금 회수 전략 시점 결정\n- 해산유형별로 향후 청산절차 소요기간 및 회수 가능성 평가\n- 해산 이후 잔여 자산 분배 가능성에 따른 투자자 손실율 사전 추정\n\n【효과적 활용 방법】\n- 해산사유(dissolution_rsn)를 분류하여 위험 발생 원인을 구체적으로 분석\n- 해산결정일자(dissolution_de) 기준으로 대손충당금 설정 시점 조정\n- 해산유형(dissolution_type)을 파악하여 잔여가치 평가 방식(합병 vs 청산) 설정\n- get_single_acc를 통해 해산 직전 자산 규모 및 채무 구조를 상세 분석",
    tags={"주요사항보고서", "해산사유", "주요정보", "해산"}
)
def get_dissolution(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    해산사유 발생 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020022
    """
    result = with_context(ctx, "get_dissolution", lambda context: context.ds005.get_dissolution(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_paid_in_capital_increase",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 유상증자 결정을 공시한 내역을 조회하는 도구입니다. 신규 자금 조달 계획, 기존 주주의 지분 희석 가능성, 기업 성장전략 방향성을 조기에 파악할 수 있으며, 투자자산 평가 및 주가 변동성 예측에 활용됩니다.\n\n【핵심 제공 데이터】\n- 결정일자(decision_de): 유상증자 결정을 공식 발표한 일자\n- 증자방식(capital_increase_mthd): 주주배정, 제3자 배정, 일반공모 등 자금조달 방식 확인\n- 신주발행수량(new_stock_co): 유상증자로 발행 예정인 신주의 총 수량\n- 1주당 발행가액(issue_prc): 신주 한 주당 발행가로 기존 주주 가치 희석 여부 판단\n- 증자금액(capital_increase_amt): 총 조달 예정 금액으로 자금 활용 규모 추정\n- 신주배정 기준일(stock_allotment_base_de): 신주 배정 대상 주주 확정일\n- 신주상장 예정일(new_stock_listg_estm_de): 신주가 실제 시장에 상장될 예정일\n- 기타사항(etc): 추가 조건, 락업 여부 등 세부사항\n\n【연계 분석 도구】\n- get_stock_total: 신주발행 이후 총 주식수 변화 확인\n- get_major_holder_changes: 증자 이후 주요 주주 지분율 변동 추적\n- get_single_acc: 유상증자 대금 반영 후 재무제표 상 자본 변동 분석\n- get_disclosure_list: 추가 유상증자, 전환사채 발행 공시와 연계 분석\n\n【활용 시나리오】\n- 유상증자 방식 및 발행가를 분석하여 기존 주주 가치 희석 여부 평가\n- 신주발행수량 및 증자금액을 통해 기업 성장 계획과 자금 활용 방향성 분석\n- 신주배정 기준일을 기준으로 권리락 일정 및 주가 변동성 예측\n- 주요 주주가 참여하지 않는 경우(3자배정 등) 지배구조 변화 리스크 분석\n- 증자 이후 get_stock_total, get_single_acc를 통해 실제 자본구조 변동 모니터링\n\n【효과적 활용 방법】\n- 증자방식(capital_increase_mthd) 확인 후 투자자 관점(공모/사모)에서 리스크 분석\n- 신주배정 기준일(stock_allotment_base_de) 전후로 투자 타이밍 조정\n- get_major_holder_changes를 통해 지분구조 변화 여부를 사전 파악\n- 자본금 증가에 따른 부채비율 개선 또는 추가 차입 가능성 분석",
    tags={"주요사항보고서", "유상증자", "주요정보", "증자"}
)
def get_paid_in_capital_increase(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유상증자 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020023
    """
    result = with_context(ctx, "get_paid_in_capital_increase", lambda context: context.ds005.get_paid_in_capital_increase(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_free_capital_increase",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 무상증자 결정을 공시한 내역을 조회하는 도구입니다. 기존 주주에 대한 무상 신주 배정 계획을 신속히 파악할 수 있으며, 주가 희석 가능성, 주주가치 제고 전략 여부, 주식 유통물량 변동성을 평가하는 데 활용됩니다.\n\n【핵심 제공 데이터】\n- 결정일자(decision_de): 무상증자 결정을 공식 발표한 일자\n- 신주배정 기준일(stock_allotment_base_de): 신주를 배정받을 기존 주주를 확정하는 기준일\n- 신주상장 예정일(new_stock_listg_estm_de): 신주가 실제 상장되어 거래 가능한 예정일\n- 신주발행수량(new_stock_co): 무상증자로 발행 예정인 신주의 총 수량\n- 1주당 배정주식수(per_stk_stock): 기존 1주당 무상배정 받을 신주 수량 (예: 1주당 0.5주)\n- 배정대상(target): 신주를 배정받는 대상 (예: 기존 주주, 전환사채권자 등)\n- 기타사항(etc): 락업 조건, 상장일 변동 가능성 등 추가 조건\n\n【연계 분석 도구】\n- get_stock_total: 무상증자 이후 총 주식수 변동 확인\n- get_major_holder_changes: 무상증자 이후 주요 주주 지분율 변동 추적\n- get_single_acc: 무상증자에 따른 자본금 변동 여부 분석\n- get_disclosure_list: 추가 무상증자 또는 유상증자 계획 여부 확인\n\n【활용 시나리오】\n- 무상증자 규모 및 배정비율을 통해 기존 주주가치 희석 여부 평가\n- 신주배정 기준일 기준 권리락 발생 가능성 분석\n- 무상증자 이후 주식 수 급증에 따른 유통물량 변화 예측\n- get_stock_total, get_single_acc를 통해 자본구조 변동 추적\n- get_major_holder_changes를 통해 지배구조 변동성 사전 탐지\n\n【효과적 활용 방법】\n- 신주발행수량(new_stock_co)와 기존 총발행주식수를 비교하여 희석율 계산\n- 1주당 배정주식수(per_stk_stock)를 활용하여 주가 조정 예상\n- 배정대상(target)을 검토하여 향후 지분변동 리스크 사전 점검\n- 무상증자 결정 이후 추가 공시(get_disclosure_list) 병행 모니터링",
    tags={"주요사항보고서", "무상증자", "주요정보", "증자"}
)
def get_free_capital_increase(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    무상증자 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020024
    """
    result = with_context(ctx, "get_free_capital_increase", lambda context: context.ds005.get_free_capital_increase(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_paid_free_capital_increase",
    description="주요사항보고서(유무상증자 결정) 내에 주요 정보를 제공합니다. 반환값에는 유상/무상 발행주식수, 발행가액, 배정비율, 상장예정일 등이 포함됩니다.",
    tags={"주요사항보고서", "유무상증자", "주요정보", "증자"}
)
def get_paid_free_capital_increase(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유무상증자 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020025
    """
    result = with_context(ctx, "get_paid_free_capital_increase", lambda context: context.ds005.get_paid_free_capital_increase(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_capital_reduction",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 감자 결정을 공시한 내역을 조회하는 도구입니다. 기업 구조조정의 핵심 신호, 재무적 곤경 정도, 주주가치 희생 정도, 또는 세금 최적화 전략 등을 심층 분석할 수 있습니다.\n\n【핵심 제공 데이터】\n- 감자방식(cpr_mth): 유상감자/무상감자 구분을 통해 재무위기 심각도 및 주주 피해 정도 판단\n- 감자비율(cpr_rat): 감자 규모를 통한 기업 재무구조 개선 의지 또는 위기 수준 평가\n- 감자사유(cpr_rs): 재무구조 개선, 자본 조정, 적자 누적, 분식회계 처리 등 다양한 사유 분석\n- 감자일정(안건예정/결정/효력발생일자): 감자 결정부터 실행까지 소요시간으로 위기 긴급도 평가\n- 1주당 감자가액(cpr_prc_per_sh): 기업 내부가치 평가와 시장가치 괴리 분석\n- 감자총액(cpr_tamt): 실질적 자본금 감소 규모를 통한 재무위기 깊이 분석\n- 기타사항(etc): 감자 이후 추가 구조조정 계획, 채권단 개입 여부, 향후 자본확충 계획 등\n\n【연계 분석 도구】\n- get_business_suspension: 감자 전후 영업정지 발생 여부 확인 → 전면적 구조조정 신호 포착\n- get_bankruptcy, get_rehabilitation: 감자 이후 추가적 부도/회생절차 진행 여부 → 기업 생존가능성 평가\n- get_major_holder_changes: 감자 전후 대주주 지분 변동 패턴 → 대주주의 책임회피 또는 경영권 방어 전략 분석\n- get_executive_trading: 감자 결정 직전 임원진의 지분 매도 여부 → 내부자 사전 회피 행위 감지\n- get_single_acc: 감자 전후 재무제표 변화 → 부채비율 개선 효과 및 실질 가치 변화 검증\n- get_stock_total: 감자 이후 총 발행주식수 및 자본금 변동 추적 → 주당가치 및 유통구조 변화 분석\n\n【활용 시나리오】\n- 부실기업 식별: 무상감자 규모가 큰 기업 중 감자사유가 '누적적자'인 경우 → 심각한 재무위기 신호로 투자 리스크 극대화\n- 분식회계 후폭풍 탐지: 감자사유가 '과거 회계처리 오류' 언급 시 → 추가적 감사 지적 및 상장폐지 리스크 평가\n- 경영권 분쟁 포착: 특정 주주 지분만 선택적으로 소각하는 감자방식 → 경영권 분쟁 또는 적대적 인수 방어 의도 분석\n- 세금 최적화 전략: 합병/분할 전후 감자 실시 → 과세이연 또는 세금 최적화 의도 파악\n- 구조조정 수순 예측: 감자 공시 후 get_paid_in_capital_increase 결과 연계 → '선 감자, 후 증자' 방식의 자본재편 전략 사전 파악\n\n【효과적 활용 방법】\n- 감자방식과 감자비율 교차분석: 무상감자+고비율(50%이상) 조합은 심각한 재무위기 신호, 유상감자+저비율은 운영상 자본조정 신호로 구분\n- 일정 분석을 통한 긴급도 평가: 안건예정일→결정일→효력발생일 간격이 매우 짧은 경우 긴급 구조조정 신호로 해석\n- 감자 전후 공시 연계분석: get_disclosure_list로 감자 직전 '상장적격성 실질심사' 또는 직후 '유상증자' 공시 여부 확인으로 기업 생존 시나리오 도출\n- 경영진/대주주 행동패턴 추적: get_executive_trading과 get_major_holder_changes로 내부자들의 감자 전후 주식거래 패턴 비교로 신뢰성 판단",
    tags={"주요사항보고서", "감자", "주요정보", "감자"}
)
def get_capital_reduction(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    감자 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020026
    """
    result = with_context(ctx, "get_capital_reduction", lambda context: context.ds005.get_capital_reduction(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_creditor_management",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 채권은행 등의 관리절차 개시를 공시한 내역을 조회하는 도구입니다. 기업의 심각한 재무위기 상태와 채권단 개입 단계를 파악할 수 있는 중요 지표로, 상장폐지 전 위험신호를 조기에 포착하는 데 활용됩니다.\n\n【핵심 제공 데이터】\n- 개시일자(mngm_prc_bgn_dt): 채권은행 관리절차 시작 시점으로 공식적 재무위기 개시일\n- 관리은행명(mngm_bnk_nm): 주채권은행 또는 채권금융기관 등 구조조정 주도기관 정보\n- 관리내용(mngm_ctn): 자율협약, 워크아웃, 기업개선작업 등 구체적 관리유형 및 구조조정 수준\n- 후속일정(ft_shdl): 경영정상화계획 제출, 채권단 협의, 자구계획 이행 등 향후 진행 로드맵\n- 비고(rmk): 관리사유, 추가 구조조정 계획, 지원 내용 등 세부 정보\n\n【연계 분석 도구】\n- get_creditor_management_termination: 채권단 관리절차 중단 여부 확인 → 정상화 또는 추가 위기 판단\n- get_rehabilitation, get_bankruptcy: 채권단 관리 실패 후 회생절차 또는 부도 상태로 진행 여부\n- get_major_holder_changes: 채무 출자전환 등 채권단 개입에 따른 지배구조 변화 분석\n- get_single_acc: 관리절차 개시 전후 부채구조, 유동성, 자본 변동 상세 분석\n- get_disclosure_list: 채권단 관리 이후 자산매각, 사업재편, 유상증자 등 후속조치 파악\n\n【활용 시나리오】\n- 디폴트 위험 사전탐지: 자율협약(초기단계)→워크아웃(중간단계)→법정관리(심각단계) 진행 패턴 포착\n- 구조조정 강도 분석: 관리내용에 따른 구조조정 침투력 평가와 기존 주주가치 희석 가능성 판단\n- 부실예측 정확도 제고: 채권단 개입 시점으로부터 1년 내 실질적 디폴트 가능성 80%+ 고위험군 선별\n- 생태계 연쇄 리스크 파악: 대기업 채권단 관리 공시 → 관련 계열사 및 협력사 연쇄 부실 가능성 예측\n- 주가 변동 패턴 예측: 채권단 관리 개시 공시 후 단기 반등→장기 하락 전환점 식별 및 투자전략 수립\n\n【효과적 활용 방법】\n- 관리은행-관리내용 교차분석: 산업은행/기업은행 주도의 워크아웃은 정부 주도 구조조정으로 회복 가능성 평가\n- 주기적 모니터링 체계 구축: get_creditor_management_termination과 get_disclosure_list를 3개월 주기로 연계 조회하여 정상화 진행 추적\n- 산업군별 비교분석: 동일 업종 내 과거 채권단 관리 사례의 생존율, 회복기간, 주주가치 변동 패턴 비교\n- 연계 위험신호 탐지: get_executive_trading으로 채권단 관리 직전 경영진의 지분 매도 여부 확인 → 사전 위험인지 시점 역추적",
    tags={"주요사항보고서", "채권은행", "주요정보", "채권"}
)
def get_creditor_management(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    채권은행 등의 관리절차 개시 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020027
    """
    result = with_context(ctx, "get_creditor_management", lambda context: context.ds005.get_creditor_management(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_lawsuit",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 소송 등의 제기를 공시한 내역을 조회하는 도구입니다. 기업의 법적 위험, 잠재적 재무 영향, 평판 리스크를 파악할 수 있으며, 소송 패턴 분석을 통해 기업 지배구조와 내부통제의 취약점을 식별하는 데 활용됩니다.\n\n【핵심 제공 데이터】\n- 소송제기일(lawsuit_date): 소송이 시작된 일자로, 기업 리스크 노출 시점 파악 및 주가 영향 분석의 기준점\n- 소송당사자(lawsuit_party): 원고/피고 구성을 통해 기업 간 분쟁, 내부 고발, 집단소송 등 소송 성격 식별\n- 소송의 내용(lawsuit_content): 특허침해, 계약위반, 불공정거래, 환경오염 등 소송 유형과 기업 위험 영역 파악\n- 소송가액(lawsuit_amount): 소송으로 인한 잠재적 재무 손실 규모와 전체 자산 대비 심각성 평가\n- 소송사유(lawsuit_cause): 소송 발생 원인과 기업의 경영판단 오류 또는 법규 위반 가능성 파악\n- 진행상황(progress_status): 소송 진행 단계와 향후 전개 예측에 활용(1심 진행중, 항소 등)\n- 향후대책(future_plan): 기업이 제시한 소송 대응 전략과 리스크 관리 역량 평가\n\n【연계 분석 도구】\n- get_disclosure_list: 소송 관련 추가 공시자료 확인 → 시간 경과에 따른 소송 진행 경과 추적\n- get_single_acc: 재무제표 상 소송충당부채, 우발부채 설정 여부 확인 → 기업의 소송 리스크 자체 평가 파악\n- get_accounting_auditor_opinion: 감사의견에 소송 관련 강조사항 포함 여부 확인 → 회계적 중요성 판단\n- get_executive_trading: 소송 공시 전후 임원 주식거래 패턴 분석 → 내부자 정보 활용 여부 점검\n- get_individual_compensation: 소송 책임 임원에 대한 보상 변화 분석 → 내부 책임 소재 파악\n\n【활용 시나리오】\n- 소송 금액 중요성 평가: 소송가액과 get_single_acc를 연계하여 총자산 대비 소송금액 비율 산출 → 20% 이상 시 재무적 중대 위험 신호\n- 소송 패턴 분석: get_disclosure_list로 과거 유사 소송 이력 확인 → 반복적 소송은 구조적 내부통제 취약성 지표\n- 이해관계자 영향 평가: 소송당사자 유형과 get_major_shareholder 정보 연계 → 주주 간 분쟁 또는 지배구조 문제 식별\n- 회계 리스크 연계성: 소송내용과 get_accounting_auditor_opinion 연계 → 회계처리 적정성 문제와 소송 연관성 파악\n- 내부자 행동 모니터링: 소송제기일 전후 get_executive_trading 패턴 분석 → 소송 예상 시 비정상적 매도는 내부 위험인지 신호\n\n【효과적 활용 방법】\n- 소송가액 임계치 설정: 시가총액 대비 소송가액 비율 10% 이상 건은 중대 재무리스크로 우선 모니터링\n- 소송 유형 분류: 소송내용을 특허, 계약, 노동, 환경 등으로 분류하여 기업의 취약 영역 식별\n- 진행상황-향후대책 교차분석: 진행상황이 불리함에도 향후대책이 구체적이지 않은 경우 심각한 리스크 신호\n- 소송 타임라인 구축: 유사 소송의 제기일부터 종결까지 소요기간 데이터 수집 → 현재 소송의 잠재 영향 기간 예측\n- 산업군별 소송 패턴 비교: 동종업계 기업들의 소송 유형과 빈도 비교 → 산업 고유 리스크 vs 기업 특수 리스크 구분",
    tags={"주요사항보고서", "소송", "주요정보", "소송"}
)
def get_lawsuit(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    소송 등의 제기 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020028
    """
    result = with_context(ctx, "get_lawsuit", lambda context: context.ds005.get_lawsuit(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_foreign_listing_decision",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 해외 증권시장 주권등 상장 결정을 공시한 내역을 조회하는 도구입니다. 국내 시장을 넘어 해외 자본시장 진출 전략, 글로벌 투자자 유치 의도, 기업가치 재평가 목적, 국내 규제 우회 가능성 등 다양한 숨은 전략적 의도를 분석할 수 있습니다.\n\n【핵심 제공 데이터】\n- 상장예정시장(lst_plan_mkt): 상장 대상 해외 거래소(NYSE, NASDAQ, 홍콩, 런던 등)를 통해 목표 투자자층과 지역 다변화 전략 파악\n- 상장예정일(lst_plan_dt): 국내외 정치경제 이벤트, 산업 주기와의 연관성 분석으로 최적 타이밍 선택 의도 분석\n- 증권종류(sec_tp): ADR/GDR 등 해외상장 방식 선택을 통한 경영권 방어 및 지배구조 유지 의도 파악\n- 상장예정주식수(lst_plan_stk_cnt): 전체 발행주식 대비 비율을 통해 자금조달 규모 및 지배구조 영향도 예측\n- 상장주선인(lst_undwrt): 선정된 글로벌 투자은행의 위상을 통해 상장 성공 가능성 및 국제 네트워크 역량 평가\n- 외화표시여부(forexc_exprs_yn): 글로벌 브랜드 구축, 국제 회계기준 준수, 환율 리스크 회피 전략 식별\n- 상장결정사유(lst_dcrs_rsn): 공식 발표된 상장 목적 뒤에 숨은 실질적 의도(지배구조 변화, 규제 회피, 사업다각화) 분석\n\n【연계 분석 도구】\n- get_disclosure_list: 해외상장 결정 전후 관련 공시 패턴 분석 → 실제 의도와 공식 발표의 일관성 검증\n- get_foreign_listing: 실제 상장 완료 여부와 계획 대비 변동사항 추적 → 상장 추진력과 실행력 평가\n- get_major_holder_changes: 해외상장 결정 전후 대주주 지분 변동 확인 → 지배구조 변화 의도 포착\n- get_single_acc: 재무제표 상 해외사업 비중 및 외화자산 비율 분석 → 글로벌 확장 전략의 실체성 검증\n- get_executive_trading: 해외상장 공시 전후 임원 주식거래 패턴 분석 → 내부자 기대감 및 신뢰도 평가\n\n【활용 시나리오】\n- 규제 회피 의도 탐지: 국내 규제 강화 시기와 해외상장 결정 시점 비교 + 상장예정시장의 규제 특성 분석 → 국내 금융/지배구조 규제 우회 가능성 평가\n- 자본조달 전략 분석: 상장예정주식수 + get_single_acc 통한 부채비율 검토 → 국내 자본시장 한계 돌파 목적 또는 대규모 해외 투자 준비 신호 포착\n- 글로벌 M&A 준비 감지: 상장예정시장의 산업 특성 + get_disclosure_list를 통한 해외기업 인수 관련 공시 검색 → 주식교환 방식 글로벌 M&A 준비 가능성 평가\n- 대주주 지배력 강화 의도 파악: 증권종류(ADR 수준) + get_major_holder_changes 연계 분석 → 의결권 제한 있는 해외상장으로 지배력 유지 의도 식별\n- 기업가치 재평가 목적 검증: 동종업계 글로벌 기업 대비 저평가 여부 + 상장예정시장의 산업별 밸류에이션 멀티플 비교 → 국내 저평가 탈피 의도 분석\n\n【효과적 활용 방법】\n- 시장 선택 의도 분석: 상장예정시장(lst_plan_mkt)별 특성과 기업 사업영역 매칭도 평가 → 기술기업의 나스닥, 소비재기업의 홍콩 등 전략적 적합성 판단\n- 지배구조 영향 평가: 증권종류와 상장예정주식수 조합으로 의결권 희석 가능성 계산 → ADR Level별 의결권 제한 정도 고려한 지배구조 변동 예측\n- 글로벌 확장 진정성 검증: 상장결정사유와 get_single_acc 통한 해외사업 비중 연계 분석 → 해외사업 비중 낮은데 글로벌 확장 명분은 의심 신호\n- 자금조달 규모의 적정성: 상장예정주식수와 get_single_acc 통한 재무상태 연계분석 → 과대/과소 규모 판단으로 숨은 의도 추론\n- 산업 특수 요인 식별: 동종업계 해외상장 사례와 성과 패턴 분석 → 산업별 해외상장 성공/실패 요인과 현 기업 특성 비교",
    tags={"주요사항보고서", "해외 증권시장", "주권등", "상장", "결정"}
)
def get_foreign_listing_decision(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    해외 증권시장 주권등 상장 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020029
    """
    result = with_context(ctx, "get_foreign_listing_decision", lambda context: context.ds005.get_foreign_listing_decision(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_foreign_delisting_decision",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 해외 증권시장 주권등 상장폐지 결정을 공시한 내역을 조회하는 도구입니다. 해외 자본시장에서의 철수 전략, 지배구조 강화 의도, 비용 절감 목적, 경영 투명성 감소 시도, 유동성 문제 은폐 등 다양한 숨은 의도와 잠재적 리스크를 분석할 수 있습니다.\n\n【핵심 제공 데이터】\n- 상장폐지시장(delst_mkt): 철수 대상 해외 거래소를 통해 지역별 경영 전략 변화와 사업 축소 방향성 식별\n- 상장폐지사유(delst_rs): 공식 발표된 폐지 사유와 실제 경영/재무 상황 간 불일치 파악으로 숨은 의도 추론\n- 상장폐지예정일(delst_pln_dt): 폐지 일정의 급박성을 통해 위기 대응 성격인지 계획적 철수인지 판단\n- 주요주주현황(maj_shldr_stt): 대주주와 외국인 투자자 비중 등을 통해 지배구조 강화 의도 파악\n- 관련 이사회결의일(board_mngt_dt): 의사결정 과정의 신속성과 독립성 평가로 거버넌스 건전성 판단\n- 투자자보호조치(invst_prtc_msr): 보호조치의 실질적 효과성 분석으로 소액주주 권익 침해 가능성 평가\n- 영향분석(impact_anlys): 상장폐지의 재무적/비재무적 영향에 대한 기업 자체 평가의 객관성 검증\n\n【연계 분석 도구】\n- get_foreign_listing: 최초 해외상장 시점과 폐지 결정까지의 기간 분석 → 해외시장 활용 전략의 변화 패턴 파악\n- get_major_holder_changes: 폐지 결정 전후 대주주 지분 변동 확인 → 지배구조 강화 의도 검증\n- get_single_acc: 최근 재무상태 변화와 해외사업 실적 추이 분석 → 실적 부진 은폐 또는 비용 절감 목적 확인\n- get_disclosure_list: 폐지 결정 전후 주요 공시 패턴 분석 → 비우호적 정보 공개 회피 의도 탐지\n- get_executive_trading: 폐지 결정 전 임원 주식거래 패턴 분석 → 내부자 정보 활용 여부 확인\n\n【활용 시나리오】\n- 재무적 위기 은폐 탐지: 상장폐지사유 + get_single_acc 통한 해외 실적 및 부채 추이 분석 → 해외 투자자 대상 재무 정보 공개 회피 의도 식별\n- 경영권 방어 전략 분석: 주요주주현황 + get_major_holder_changes 연계 분석 → 외국인 투자자 영향력 차단 및 지배주주 통제력 강화 의도 포착\n- 규제 회피 의도 파악: 폐지 대상 시장의 최근 규제 변화 + 해당 국가 감독당국 조사 정보 수집 → 강화된 공시의무나 지배구조 규제 회피 목적 평가\n- 비용 합리화 검증: 상장폐지사유 중 '비용 절감' 주장 + get_single_acc 통한 해외상장 유지비용 대비 자산규모 분석 → 비용 대비 효익 논리의 합리성 검증\n- M&A 준비 징후 포착: 폐지 결정 타이밍 + get_disclosure_list 통한 지분구조 변화 관련 공시 검토 → 경영권 변동 또는 주요 인수합병 준비 과정 식별\n\n【효과적 활용 방법】\n- 폐지사유-재무상태 정합성 분석: 상장폐지사유(delst_rs)와 get_single_acc 통한 재무지표 추이 교차검증 → 공식 사유와 재무 실적 간 불일치는 숨은 의도 신호\n- 지배구조 영향 평가: 주요주주현황과 get_major_holder_changes 비교 → 폐지 결정 전후 지분구조 변화로 지배력 강화 의도 확인\n- 시장 반응 예측 모델: 유사 사례의 국내 주가 반응 패턴 분석 → 해외상장 폐지 후 국내 주가 영향 및 변동성 예측\n- 투자자보호조치 실효성 평가: 제시된 보호조치와 실제 주주가치 보전 가능성 비교 → 형식적 조치 vs 실질적 보호 구분\n- 국내-해외 공시 내용 비교: 국내 공시와 해당 해외시장 공시 내용의 일관성 점검 → 정보 비대칭 전략 포착",
    tags={"주요사항보고서", "해외 증권시장", "주권등", "상장", "결정"}
)
def get_foreign_delisting_decision(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    해외 증권시장 주권등 상장폐지 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020030
    """
    result = with_context(ctx, "get_foreign_delisting_decision", lambda context: context.ds005.get_foreign_delisting_decision(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_foreign_listing",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중 해외 증권시장 주권등 상장에 관한 공시 내역을 조회하는 도구입니다. 기업의 글로벌 자본시장 진출 현황, 해외 투자자 유치 전략, 자금조달 규모, 국내 자본시장 규제 회피 가능성 등을 파악할 수 있으며, 기업의 글로벌 확장 전략과 잠재적 리스크를 평가하는 데 활용됩니다.\n\n【핵심 제공 데이터】\n- 상장시장명(mkt_nm): 기업이 선택한 해외 거래소(뉴욕, 나스닥, 런던, 홍콩 등)를 통해 목표 투자자층과 자본시장 특성 분석\n- 상장일자(lst_dt): 실제 상장 완료 시점으로 결정부터 실행까지의 추진력 및 효율성 평가\n- 상장주식수(lst_stk_cnt): 해외 상장 규모와 전체 발행주식 대비 비율로 자금조달 목적과 경영권 희석 여부 판단\n- 발행시장 구분(pb_pvt_cls_nm): 공모/사모 방식을 통해 투자자 타겟팅 전략 및 정보공개 회피 의도 식별\n- 상장목적(lst_pps): 공식적으로 발표된 상장 목적과 실제 재무/사업 전략 간 정합성 판단\n- 자금용도(fund_prps): 조달 자금의 사용 계획을 통해 해외 사업 확장, 부채 상환, M&A 등 실질적 전략 방향 평가\n- 증권의 종류(sec_knd): ADR, GDR 등 증권 형태를 통한 의결권 구조 변화 의도와 지배구조 영향 파악\n\n【연계 분석 도구】\n- get_foreign_listing_decision: 최초 결정 시점과 실제 상장까지의 기간 및 변경사항 비교 → 계획 실행력과 목표 일관성 검증\n- get_foreign_delisting_decision: 향후 상장폐지 결정 여부 모니터링 → 해외 자본시장 활용의 지속성과 성공 여부 평가\n- get_major_holder_changes: 해외상장 전후 대주주 지분 변동 분석 → 지배구조 변화 및 내부자 거래 패턴 식별\n- get_single_acc: 해외사업 비중과 외화자산/부채 구조 분석 → 글로벌 확장 전략의 실질적 기반 검증\n- get_disclosure_list: 해외상장 관련 후속 공시 모니터링 → 계획 변경, 추가 자금조달, 규제대응 등 연속적 전략 파악\n\n【활용 시나리오】\n- 지배구조 영향 평가: 상장주식수 + get_major_holder_changes 연계 분석 → 의결권 희석 효과와 지배주주의 통제력 변화 예측\n- 글로벌 M&A 준비 감지: 자금용도 + get_disclosure_list의 인수합병 관련 공시 연계 → 해외 인수 대상 탐색 및 글로벌 사업 재편 가능성 평가\n- 규제 회피 의도 분석: 상장시장명과 상장시점 + 국내 규제환경 변화 타이밍 비교 → 국내 규제/감독 회피 목적의 해외 이전 가능성 식별\n- 재무적 위기 은폐 탐지: 상장목적과 get_single_acc 통한 부채구조/수익성 추이 연계 → 국내 신용등급 하락 회피 또는 유동성 위기 극복 의도 파악\n- 회계투명성 변화 예측: 상장시장명의 회계/공시 규제 특성 + get_accounting_auditor_opinion 연계 → 국제 회계기준 적용에 따른 재무구조 변화 전망\n\n【효과적 활용 방법】\n- 시장 선택의 전략적 의미 분석: 상장시장명(mkt_nm)별 규제/투자자 특성과 기업 사업영역 매칭도 평가 → 기술기업의 나스닥, 소비재기업의 홍콩 등 전략적 적합성 판단\n- 자금조달 규모의 목적 검증: 상장주식수(lst_stk_cnt)와 자금용도(fund_prps) 연계 분석 → 실제 필요 자금 규모 대비 과대/과소 조달 여부로 숨은 의도 추론\n- 상장 타이밍의 기회주의적 활용 식별: 상장일자(lst_dt)와 국내외 시장 상황/규제 변화 비교 → 일시적 기회 포착 또는 장기 전략적 접근 구분\n- 지역별 사업 전략 변화 감지: 상장시장명(mkt_nm)과 get_single_acc의 지역별 매출/자산 비중 연계 → 특정 지역 사업 확장 또는 축소 전략 변화 조기 파악\n- 증권종류별 지배구조 영향 평가: 증권의 종류(sec_knd)와 get_major_holder_changes 연계 → ADR 레벨별 의결권 제한 정도를 고려한 지배구조 영향 심층 분석",
    tags={"주요사항보고서", "해외 증권시장", "주권등", "상장"}
)
def get_foreign_listing(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    해외 증권시장 주권등 상장 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020031
    """
    result = with_context(ctx, "get_foreign_listing", lambda context: context.ds005.get_foreign_listing(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_foreign_delisting",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중 해외 증권시장 주권등 상장폐지에 관한 공시 내역을 조회하는 도구입니다. 기업의 해외 자본시장 철수 전략, 지배구조 강화 의도, 비용 절감 목적, 경영 투명성 감소 시도, 실적 부진 은폐 등의 숨은 의도와 잠재적 리스크를 분석할 수 있습니다.\n\n【핵심 제공 데이터】\n- 상장폐지시장(delst_mkt): 철수 대상 해외 거래소를 통해 지역별 경영 전략 변화와 시장환경 대응 방향성 파악\n- 폐지일자(delst_dt): 상장폐지 실행 시점으로 철수 결정의 긴급성과 시장 상황 활용 의도 분석\n- 폐지사유(delst_rs): 공식 발표된 폐지 이유와 실제 경영/재무 상황 간 불일치를 통한 숨은 의도 추론\n- 상장일자(lst_dt): 최초 상장부터 폐지까지의 기간 분석으로 해외 자본시장 활용 전략의 성공/실패 평가\n- 폐지방법(delst_mth): 자발적 폐지, 강제 퇴출 등 폐지 유형을 통한 기업 신뢰도와 국제 규제 준수 수준 판단\n- 후속조치(fllw_msr): 상장폐지 이후 투자자 보호 대책과 자본구조 변화 계획을 통한 소액주주 가치 보존 의지 평가\n- 기타사항(etc): 추가 정보를 통한 폐지 관련 복잡한 상황이나 특이사항 파악\n\n【연계 분석 도구】\n- get_foreign_listing: 최초 해외상장 내역과 비교 분석 → 상장-폐지 간 일관성 및 전략 변화 파악\n- get_foreign_listing_decision: 최초 상장 결정 시 목표와 폐지 사유 비교 → 전략 실패 또는 의도적 단기 활용 여부 판단\n- get_major_holder_changes: 폐지 전후 대주주 지분 변동 추적 → 경영권 강화 또는 외국인 투자자 배제 의도 확인\n- get_single_acc: 재무상태 변화와 해외사업 실적 추이 분석 → 실적 부진 은폐 또는 비용 합리화 목적 검증\n- get_disclosure_list: 폐지 전후 주요 공시 패턴 분석 → 시장에 불리한 정보 공개 회피 의도 탐지\n\n【활용 시나리오】\n- 비용 합리화 검증: 폐지사유 중 '비용 절감' 주장 + get_single_acc 통한 유지비용 대비 시가총액 분석 → 비용 대비 효익 논리의 합리성 검증\n- 지배구조 변화 의도 탐지: 폐지시장 특성 + get_major_holder_changes 연계 분석 → 외국인 투자자 영향력 차단 및 지배주주 통제력 강화 목적 식별\n- 재무 실적 은폐 평가: 폐지사유 + get_single_acc 통한 해외 실적 및 부채 추이 분석 → 해외 투자자 대상 부진한 실적 공개 회피 의도 파악\n- 규제 회피 징후 포착: 폐지시장의 규제 강화 추세 + 감독당국 조사 정보 수집 → 강화된 공시의무나 지배구조 규제 회피 목적 추론\n- M&A 준비 신호 감지: 폐지 타이밍 + get_disclosure_list 통한 지분구조 변화 관련 공시 검토 → 경영권 변동 또는 인수합병 준비 과정 식별\n\n【효과적 활용 방법】\n- 폐지사유-재무상태 정합성 분석: 폐지사유(delst_rs)와 get_single_acc 통한 재무지표 추이 교차검증 → 공식 사유와 재무 실적 간 불일치 시 숨은 의도 포착\n- 폐지 결정의 적시성 판단: 폐지일자(delst_dt)와 해당 해외시장 상황/규제 변화 비교 → 시장 악화 전 선제적 철수 또는 규제 회피성 철수 구분\n- 후속조치 실효성 평가: 후속조치(fllw_msr) 내용과 실제 주주가치 보전 가능성 비교 → 형식적 조치 vs 실질적 보호 구분\n- 국내-해외 공시 내용 비교: 국내 폐지 공시와 해당 해외시장 공시 내용의 일관성 점검 → 시장별 정보 비대칭 전략 포착\n- 지배구조 영향 추적: 폐지시장(delst_mkt) 특성과 get_major_holder_changes 연계 → 폐지 전후 지분구조 및 의결권 변화 패턴 심층 분석",
    tags={"주요사항보고서", "해외 증권시장", "주권등", "상장", "폐지"}
)
def get_foreign_delisting(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    해외 증권시장 주권등 상장폐지 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020032
    """
    result = with_context(ctx, "get_foreign_delisting", lambda context: context.ds005.get_foreign_delisting(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_convertible_bond",
    description="주요사항보고서(전환사채권 발행결정) 내에 주요 정보를 제공합니다. 반환값에는 발행총액, 전환비율, 전환가액, 전환청구기간 등이 포함됩니다.",
    tags={"주요사항보고서", "전환사채권", "발행결정", "전환"}
)
def get_convertible_bond(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    전환사채권 발행결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020033
    """
    result = with_context(ctx, "get_convertible_bond", lambda context: context.ds005.get_convertible_bond(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_bond_with_warrant",
    description="주요사항보고서(신주인수권부사채권 발행결정) 내에 주요 정보를 제공합니다. 반환값에는 발행총액, 행사비율, 행사기간, 발행조건 등이 포함됩니다.",
    tags={"주요사항보고서", "신주인수권부사채권", "발행결정", "신주"}
)
def get_bond_with_warrant(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    신주인수권부사채권 발행결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020034
    """
    result = with_context(ctx, "get_bond_with_warrant", lambda context: context.ds005.get_bond_with_warrant(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_exchangeable_bond",
    description="주요사항보고서(교환사채권 발행결정) 내에 주요 정보를 제공합니다. 반환값에는 발행총액, 교환대상종목, 교환가액, 교환청구기간 등이 포함됩니다.",
    tags={"주요사항보고서", "교환사채권", "발행결정", "교환"}
)
def get_exchangeable_bond(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    교환사채권 발행결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020035
    """
    result = with_context(ctx, "get_exchangeable_bond", lambda context: context.ds005.get_exchangeable_bond(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_creditor_management_termination",
    description="주요사항보고서(채권은행 등의 관리절차 중단) 내에 주요 정보를 제공합니다. 반환값에는 중단일자, 중단사유, 채권은행명, 향후계획 등이 포함됩니다.",
    tags={"주요사항보고서", "채권은행", "관리절차", "중단"}
)
def get_creditor_management_termination(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    채권은행 등의 관리절차 중단 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020036
    """
    result = with_context(ctx, "get_creditor_management_termination", lambda context: context.ds005.get_creditor_management_termination(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_write_down_bond",
    description="주요사항보고서(상각형 조건부자본증권 발행결정) 내에 주요 정보를 제공합니다. 반환값에는 발행조건, 상각요건, 발행총액, 발행일자 등이 포함됩니다.",
    tags={"주요사항보고서", "상각형 조건부자본증권", "발행결정", "상각"}
)
def get_write_down_bond(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    상각형 조건부자본증권 발행결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020037
    """
    result = with_context(ctx, "get_write_down_bond", lambda context: context.ds005.get_write_down_bond(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_treasury_stock_acquisition",
    description="주요사항보고서(자기주식 취득 결정) 내에 주요 정보를 제공합니다. 반환값에는 취득예정주식수, 취득금액, 취득기간, 목적 등이 포함됩니다.",
    tags={"주요사항보고서", "자기주식", "취득", "결정"}
)
def get_treasury_stock_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자기주식 취득 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020038
    """
    result = with_context(ctx, "get_treasury_stock_acquisition", lambda context: context.ds005.get_treasury_stock_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_treasury_stock_disposal",
    description="주요사항보고서(자기주식 처분 결정) 내에 주요 정보를 제공합니다. 반환값에는 처분예정주식수, 처분금액, 처분방법, 처분기간 등이 포함됩니다.",
    tags={"주요사항보고서", "자기주식", "처분", "결정"}
)
def get_treasury_stock_disposal(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자기주식 처분 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020039
    """
    result = with_context(ctx, "get_treasury_stock_disposal", lambda context: context.ds005.get_treasury_stock_disposal(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_treasury_stock_trust_contract",
    description="주요사항보고서(자기주식취득 신탁계약 체결 결정) 내에 주요 정보를 제공합니다. 반환값에는 계약체결일, 계약기간, 계약금액, 위탁기관 등이 포함됩니다.",
    tags={"주요사항보고서", "자기주식", "신탁계약", "체결", "결정"}
)
def get_treasury_stock_trust_contract(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자기주식취득 신탁계약 체결 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020040
    """
    result = with_context(ctx, "get_treasury_stock_trust_contract", lambda context: context.ds005.get_treasury_stock_trust_contract(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_treasury_stock_trust_termination",
    description="주요사항보고서(자기주식취득 신탁계약 해지 결정) 내에 주요 정보를 제공합니다. 반환값에는 해지일자, 해지사유, 계약금액, 이사회결의일 등이 포함됩니다.",
    tags={"주요사항보고서", "자기주식", "신탁계약", "해지", "결정"}
)
def get_treasury_stock_trust_termination(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    자기주식취득 신탁계약 해지 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020041
    """
    result = with_context(ctx, "get_treasury_stock_trust_termination", lambda context: context.ds005.get_treasury_stock_trust_termination(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_business_acquisition",
    description="주요사항보고서(영업양도 결정) 내에 주요 정보를 제공합니다. 반환값에는 양도일자, 양도대상사업, 양도금액, 계약상대방 등이 포함됩니다.",
    tags={"주요사항보고서", "영업양도", "결정"}
)
def get_business_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    영업양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020043
    """
    result = with_context(ctx, "get_business_acquisition", lambda context: context.ds005.get_business_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_tangible_asset_transfer",
    description="주요사항보고서(유형자산 양수 결정) 내에 주요 정보를 제공합니다. 반환값에는 자산종류, 양수금액, 양수일자, 계약상대방 등이 포함됩니다.",
    tags={"주요사항보고서", "유형자산", "양수", "결정"}
)
def get_tangible_asset_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유형자산 양수 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020044
    """
    result = with_context(ctx, "get_tangible_asset_transfer", lambda context: context.ds005.get_tangible_asset_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_tangible_asset_acquisition",
    description="주요사항보고서(유형자산 양도 결정) 내에 주요 정보를 제공합니다. 반환값에는 자산종류, 양도금액, 양도일자, 계약상대방 등이 포함됩니다.",
    tags={"주요사항보고서", "유형자산", "양도", "결정"}
)
def get_tangible_asset_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유형자산 양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020045
    """
    result = with_context(ctx, "get_tangible_asset_acquisition", lambda context: context.ds005.get_tangible_asset_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_other_corp_stock_transfer",
    description="주요사항보고서(타법인 주식 및 출자증권 양수결정) 내에 주요 정보를 제공합니다. 반환값에는 양수대상 법인명, 양수주식수, 양수금액, 계약일자 등이 포함됩니다.",
    tags={"주요사항보고서", "타법인", "주식", "출자증권", "양수", "결정"}
)
def get_other_corp_stock_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    타법인 주식 및 출자증권 양수결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020046
    """
    result = with_context(ctx, "get_other_corp_stock_transfer", lambda context: context.ds005.get_other_corp_stock_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_other_corp_stock_acquisition",
    description="주요사항보고서(타법인 주식 및 출자증권 양도결정) 내에 주요 정보를 제공합니다. 반환값에는 양도대상 법인명, 양도주식수, 양도금액, 계약일자 등이 포함됩니다.",
    tags={"주요사항보고서", "타법인", "주식", "출자증권", "양도", "결정"}
)
def get_other_corp_stock_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    타법인 주식 및 출자증권 양도결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020047
    """
    result = with_context(ctx, "get_other_corp_stock_acquisition", lambda context: context.ds005.get_other_corp_stock_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_related_bond_transfer",
    description="주요사항보고서(주권 관련 사채권 양수 결정) 내에 주요 정보를 제공합니다. 반환값에는 사채종류, 양수금액, 양수일자, 대상회사명 등이 포함됩니다.",
    tags={"주요사항보고서", "주권", "사채권", "양수", "결정"}
)
def get_stock_related_bond_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주권 관련 사채권 양수 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020048
    """
    result = with_context(ctx, "get_stock_related_bond_transfer", lambda context: context.ds005.get_stock_related_bond_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_related_bond_acquisition",
    description="주요사항보고서(주권 관련 사채권 양도 결정) 내에 주요 정보를 제공합니다. 반환값에는 사채종류, 양도금액, 양도일자, 대상회사명 등이 포함됩니다.",
    tags={"주요사항보고서", "주권", "사채권", "양도", "결정"}
)
def get_stock_related_bond_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주권 관련 사채권 양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020049
    """
    result = with_context(ctx, "get_stock_related_bond_acquisition", lambda context: context.ds005.get_stock_related_bond_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_merger",
    description="주요사항보고서(회사합병 결정) 내에 주요 정보를 제공합니다. 반환값에는 합병상대회사, 합병비율, 합병기일, 합병방법 등이 포함됩니다.",
    tags={"주요사항보고서", "회사합병", "결정"}
)
def get_merger(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회사합병 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020050
    """
    result = with_context(ctx, "get_merger", lambda context: context.ds005.get_merger(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_division",
    description="주요사항보고서(회사분할 결정) 내에 주요 정보를 제공합니다. 반환값에는 분할방식, 분할기일, 분할회사명, 분할비율 등이 포함됩니다.",
    tags={"주요사항보고서", "회사분할", "결정"}
)
def get_division(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회사분할 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020051
    """
    result = with_context(ctx, "get_division", lambda context: context.ds005.get_division(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_division_merger",
    description="주요사항보고서(회사분할합병 결정) 내에 주요 정보를 제공합니다. 반환값에는 분할합병 상대회사, 분할합병 방식, 합병비율, 합병기일 등이 포함됩니다.",
    tags={"주요사항보고서", "회사분할합병", "결정"}
)
def get_division_merger(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    회사분할합병 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020052
    """
    result = with_context(ctx, "get_division_merger", lambda context: context.ds005.get_division_merger(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_exchange",
    description="주요사항보고서(주식교환·이전 결정) 내에 주요 정보를 제공합니다. 반환값에는 교환상대회사, 교환비율, 교환기일, 교환방법 등이 포함됩니다.",
    tags={"주요사항보고서", "주식교환", "이전", "결정"}
)
def get_stock_exchange(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주식교환·이전 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20220101)
        end_de (str): 검색종료 접수일자 (예: 20221231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020053
    """
    result = with_context(ctx, "get_stock_exchange", lambda context: context.ds005.get_stock_exchange(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

