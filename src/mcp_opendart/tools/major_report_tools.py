import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")
@mcp.tool(
    name="get_asset_transfer",
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 자산양수도(기타) 및 풋백옵션 계약 사실을 조회하는 도구입니다. 기업이 대규모 자산을 양도하거나 양수하면서 숨은 재무 리스크나 경영 전략 변경 가능성을 조기에 파악하는 데 활용됩니다. 특히 풋백옵션 존재 여부를 통해 거래 이후 발생할 수 있는 추가 부채 리스크를 사전 감지할 수 있습니다.\n\n【핵심 제공 데이터】\n- 계약일자(ctrct_de): 자산 양수도 계약 체결 시점 파악\n- 회사명(corp_name), 고유번호(corp_code), 법인구분(corp_cls): 거래 주체의 기본 정보 확인\n- 보고사유(rp_rsn): 거래 목적 및 배경 분석 (예: 구조조정, 신규사업 진출 등)\n- 자산양수·도 가액(ast_inhtrf_prc): 거래 규모를 통한 경영전략 변화 여부 평가\n- 접수번호(rcept_no): 공시 상세내역 추적용 식별자\n\n【연계 분석 도구】\n- get_disclosure_list: 동일 시기 다른 주요 공시 병행 분석\n- get_single_acc: 자산 양수·도 이후 재무제표 변동 사항 심층 분석\n- get_major_holder_changes: 대규모 자산 이동 이후 주요 주주 지분 변동 여부 모니터링\n- get_executive_trading: 임원 및 대주주의 주식 거래 패턴 변화 분석\n\n【활용 시나리오】\n- 대규모 자산 매각 → 단기 부채 상환 목적일 경우 유동성 위기 가능성 평가\n- 자산 취득 → 신규 성장 전략 진입 여부(예: 신규 공장, 신사업 부지 취득 등) 파악\n- 풋백옵션 설정 → 향후 재무 부담 발생 가능성(회수 위험) 사전 경고\n- 보고사유(rp_rsn) 분석 → 정상적인 사업확장 vs 비정상적 구조조정 구분\n- 계약 체결 이후 get_disclosure_list를 통해 추가 조건부 계약 공시 탐색\n\n【효과적 활용 방법】\n- ast_inhtrf_prc(거래 금액)과 get_single_acc(자산총계) 비교하여 재무구조 변동 규모 파악\n- 계약일자(ctrct_de) 직후 get_major_holder_changes를 통해 대주주 리스크 변화 모니터링\n- 풋백옵션 관련 조건은 반드시 세부 공시 내용(추가 get_disclosure_list 검색)으로 검토\n- 거래 금액이 총자산 대비 일정 비율(예: 10% 이상) 초과 시 경영진의 전략 방향성 재검토 필요\n\n【주의사항 및 팁】\n- 풋백옵션이 설정된 경우, 실제 행사 가능성과 시기까지 구체적으로 분석해야 리스크를 정확히 평가할 수 있습니다.\n- 단순 자산매각/취득 외에도 '보고사유'를 통해 이면의 숨은 의도를 읽어내는 것이 핵심입니다.\n- 계약 상대방의 신용도 및 관련 기업 공시를 추가적으로 분석하면 거래 안정성 평가가 가능합니다.",
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 부도 발생 사실을 조회하는 도구입니다. 기업의 유동성 리스크와 구조적 재무위기를 조기에 탐지할 수 있으며, 부도 발생 시점과 경위를 기반으로 향후 신용등급 하락, 회생절차 돌입 가능성 등을 평가하는 데 활용됩니다.\n\n【핵심 제공 데이터】\n- 회사명(corp_name), 고유번호(corp_code), 법인구분(corp_cls): 부도 발생 주체 식별\n- 부도내용(df_cn): 부도 사안의 요약 설명 (예: 만기어음 부도 등)\n- 부도금액(df_amt): 부도 금액 규모를 통한 재무 충격 평가\n- 부도발생은행(df_bnk): 부도 처리 은행 정보로 금융거래 리스크 파악\n- 최종부도일자(dfd): 부도 확정일로 유동성 위기 발생 시점 추적\n- 부도사유 및 경위(df_rs): 부도 발생의 구체적 원인 및 상황 분석\n- 접수번호(rcept_no): 추가 상세 공시문 조회를 위한 식별자 제공\n\n【연계 분석 도구】\n- get_disclosure_list: 부도 전후 다른 공시(회생절차 신청 등) 동시 분석\n- get_rehabilitation: 부도 이후 회생절차 개시 여부 확인\n- get_business_suspension: 부도와 병행된 영업정지 발생 여부 점검\n- get_dissolution: 부도 이후 해산사유 발생 여부 추적\n- get_major_holder_changes: 부도 이후 주요 주주 지분 변동 여부 모니터링\n- get_single_acc: 부도 발생 전후 재무제표 변동 분석\n\n【활용 시나리오】\n- df_amt(부도금액) 규모를 통해 그룹 전체 리스크 확산 가능성 평가\n- df_rs(부도사유 및 경위) 분석을 통해 일회성 부도(예: 일시적 유동성 부족) vs 구조적 부실 구분\n- 부도발생은행(df_bnk)을 통해 은행 연쇄 리스크 및 추가 금융위험 탐지\n- 부도 직후 get_rehabilitation, get_business_suspension 호출하여 후속 구조조정 신호 탐색\n- get_disclosure_list로 부도 관련 추가 공시(자구계획 제출, 회생신청 등) 모니터링\n\n【효과적 활용 방법】\n- df_amt(부도금액) 대비 자산총계(get_single_acc) 비율을 계산해 실질 피해규모 평가\n- dfd(최종부도일자)를 중심으로 부도 전후 30일 이내 공시를 집중 분석해 연쇄 리스크 조기 포착\n- df_rs(부도사유 및 경위) 상세 분석을 통해 경영진의 대응 의지 및 회생 가능성 평가\n- get_major_holder_changes를 통해 부도 직후 주요 주주의 이탈 가능성 모니터링\n\n【주의사항 및 팁】\n- 부도내용(df_cn)만으로는 부도 원인 분석이 불충분할 수 있으므로 반드시 부도사유(df_rs)까지 함께 검토해야 합니다.\n- 부도발생은행(df_bnk) 다수 존재 시 연쇄적 금융기관 리스크 확산 여부를 고려해야 합니다.\n- 단일 부도 공시만으로 판단하지 말고, 반드시 연계 도구(get_rehabilitation, get_dissolution 등)로 후속 절차까지 추적해야 합니다.",
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 영업정지 사실을 조회하는 도구입니다. 사업 부문 단위의 영업 중단 여부를 조기에 탐지하고, 매출 손실 규모와 향후 경영 전략 변화를 분석하는 데 활용할 수 있습니다. 기업의 존속 가능성, 수익성 악화 리스크, 구조조정 가능성까지 종합적으로 평가할 수 있습니다.\n\n【핵심 제공 데이터】\n- 회사명(corp_name), 고유번호(corp_code), 법인구분(corp_cls): 영업정지 주체 식별\n- 영업정지 분야(bsnsp_rm): 영업정지 대상 사업 부문 명칭\n- 영업정지 금액(bsnsp_amt): 해당 사업부문의 정지로 발생하는 매출 손실 규모\n- 최근 매출총액(rsl): 비교 기준이 되는 전체 매출\n- 매출 대비 비율(sl_vs): 영업정지 부문 매출이 전체 매출에서 차지하는 비율\n- 영업정지 내용(bsnsp_cn): 구체적인 영업정지 대상 설명\n- 영업정지 사유(bsnsp_rs): 영업정지 발생 원인 (예: 계약종료, 사업부문 철수 등)\n- 향후 대책(ft_ctp): 경영진의 대응 계획 (예: 신규 사업 진출, 기존 사업 강화 등)\n- 영업정지 영향(bsnsp_af): 영업정지가 재무제표에 미치는 영향 분석\n- 영업정지일자(bsnspd): 실제 영업정지 시행 일자\n- 이사회 결의일자(bddd): 영업정지 결정을 내린 이사회 결의 일자\n- 사외이사 참석여부(od_a_at_t, od_a_at_b), 감사 참석여부(adt_a_atn): 의사결정 절차의 투명성 및 합법성 판단 지표\n\n【연계 분석 도구】\n- get_disclosure_list: 영업정지 직전/직후 다른 공시 병행 분석\n- get_bankruptcy: 영업정지 이후 부도 발생 가능성 확인\n- get_rehabilitation: 영업정지 이후 회생절차 개시 여부 모니터링\n- get_dissolution: 영업정지 장기화 시 해산 절차 발생 여부 추적\n- get_single_acc: 영업정지 부문 관련 자산/부채 변동 심층 분석\n\n【활용 시나리오】\n- bsnsp_amt(영업정지 금액)과 rsl(최근 매출총액) 대비 sl_vs(비율)를 통해 전체 수익성 타격 규모 평가\n- 영업정지 사유(bsnsp_rs)를 분석하여 사업철수 위험성과 구조적 부진 여부 구분\n- ft_ctp(향후 대책) 분석을 통해 경영진의 대응력 및 회복 가능성 사전 평가\n- get_bankruptcy, get_rehabilitation 연계하여 부도/회생 리스크 모니터링\n- get_disclosure_list로 영업정지 외 추가 공시(자산처분, 구조조정 등) 병행 검토\n\n【효과적 활용 방법】\n- sl_vs(매출대비 비율)가 20% 이상이면 기업 존속성 리스크로 심각히 평가해야 함\n- bsnspd(영업정지일자)를 기준으로 30일 이내 공시를 집중 모니터링하여 연쇄 리스크 조기 탐지\n- 이사회결의(bddd)와 사외이사 참석(od_a_at_t, od_a_at_b) 정보를 통해 의사결정의 합법성과 충실성 검토\n- get_single_acc로 해당 사업부문의 자산·부채 변동 상황까지 심층 추적 필요",
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""
        상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 회생절차 개시신청 사실을 조회하는 도구입니다.
        기업의 심각한 재무위기, 유동성 고갈 문제를 조기에 파악하고,
        향후 존속 가능성 및 회생 가능성 여부를 분석하는 데 필수적인 정보를 제공합니다.

        【핵심 제공 데이터】
        - 회사명(corp_name), 고유번호(corp_code), 법인구분(corp_cls): 회생신청 주체 식별
        - 신청인(apcnt): 신청자와 회사의 관계 (예: 회사 본인, 채권자 등)
        - 관할법원(cpct): 회생신청이 접수된 법원명
        - 신청사유(rq_rs): 유동성 위기, 구조적 부실 등 신청 배경 설명
        - 신청일자(rqd): 회생절차 신청일자
        - 향후대책 및 일정(ft_ctp_sc): 경영진의 대응 계획 및 이후 법원 심리 일정

        【연계 분석 도구】
        - get_bankruptcy: 부도 발생과 회생신청 병행 여부 모니터링
        - get_business_suspension: 영업정지 이력과 회생 신청의 연관성 분석
        - get_dissolution: 회생 실패 시 해산 절차로 전이 여부 추적
        - get_major_holder_changes: 회생신청 전후 주요 주주 지분 변동 모니터링
        - get_single_acc: 회생신청 전후 재무제표 변동 심층 분석

        【활용 시나리오】
        - 신청사유(rq_rs) 분석을 통해 구조적 부실(예: 반복적 적자, 대규모 채무) 여부 구분
        - 신청일자(rqd)를 기준으로 신청 직전 3개월간 재무 및 경영 이벤트 집중 분석
        - 향후대책(ft_ctp_sc)을 통해 경영진의 회생 가능성 판단 (예: 신규 투자 유치 계획 등)
        - get_bankruptcy, get_business_suspension 호출하여 추가 리스크 여부 동시 검토
        - get_disclosure_list로 회생 진행 중 추가 공시(법원 승인 여부 등) 실시간 모니터링

        【효과적 활용 방법】
        - 신청사유(rq_rs) 구체 분석을 통해 유동성 일시 위기와 구조적 회생불능 상황 구별
        - 향후대책(ft_ctp_sc) 내용을 통해 경영진의 실질적 회생 의지 및 실행 가능성 평가
        - get_single_acc로 자산-부채 구조를 심층 분석하여 실질 회생 가능성 판단
        - get_major_holder_changes로 회생신청 직후 주요 주주 이탈 여부를 조기 포착

        【주의사항 및 팁】
        - 단순 회생신청 사실만으로 회생 가능성을 단정하지 말고, 향후대책(ft_ctp_sc)과 재무제표(get_single_acc)를 반드시 병행 분석해야 합니다.
        - 법원의 보전처분 결정 여부를 get_disclosure_list로 지속 추적하여 최종 회생절차 개시 여부를 확인해야 합니다.
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""
        상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 해산사유 발생 사실을 조회하는 도구입니다.
        기업의 법적 존속성 상실 여부를 조기에 탐지하고, 청산 절차 돌입 가능성 및 투자금 회수 리스크를 평가하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 회사명(corp_name), 고유번호(corp_code), 법인구분(corp_cls): 해산 발생 기업 식별
        - 해산사유(ds_rs): 해산 결정의 직접적인 사유 (예: 자산 전부 상환 완료, 자발적 해산 등)
        - 해산사유 발생일(결정일)(ds_rsd): 해산사유가 공식 발생한 날짜
        - 사외이사 참석여부(od_a_at_t, od_a_at_b): 해산 결정 시 사외이사 출석 여부로 의사결정 절차 합법성 평가
        - 감사 참석여부(adt_a_atn): 감사 또는 감사위원 참석 여부 확인

        【연계 분석 도구】
        - get_bankruptcy: 부도 이후 해산 절차로 전이된 경우 추가 분석
        - get_rehabilitation: 회생절차 실패 후 해산으로 넘어간 흐름 모니터링
        - get_major_holder_changes: 해산 전후 주요 주주 지분 변동 여부 파악
        - get_single_acc: 해산 직전 자산, 부채 상태를 정밀 분석하여 청산 가능 자산 규모 평가
        - get_disclosure_list: 해산 관련 추가 공시(청산절차, 잔여재산 분배 등) 병행 추적

        【활용 시나리오】
        - ds_rs(해산사유) 분석을 통해 자발적 해산(구조조정)과 비자발적 해산(파산) 구분
        - 해산사유 발생일자(ds_rsd)를 기준으로 해산 결의 이후 발생하는 추가 재무공시 집중 모니터링
        - 사외이사/감사 출석 여부를 통해 해산 결정 과정의 법적 안정성 평가
        - get_single_acc로 해산 직전 자산, 부채 구조를 심층 분석하여 회수 가능한 투자자산 규모 추정
        - 해산 이후 get_disclosure_list를 통해 잔여재산 분배, 청산완료 여부 실시간 추적

        【효과적 활용 방법】
        - 해산사유(ds_rs)가 구조적 부실(예: 영업손실 지속)인지, 단순 목적완료(예: SPC 청산)인지 구체적으로 분리하여 리스크 평가
        - 해산결정일(ds_rsd) 전후 1개월 이내 공시를 집중 모니터링하여 청산 관련 추가 이벤트를 조기 탐지
        - get_major_holder_changes를 통해 해산결정 이후 대주주 지분 변동을 파악하여 잔여재산 분배 리스크 관리
        - 해산공시가 나온 경우에도 get_disclosure_list를 통해 잔여 의무사항(부채, 미지급금 등) 여부를 끝까지 확인해야 함

        【주의사항 및 팁】
        - 해산사유가 '자발적'인 경우에도 부채나 잠재적 소송 리스크가 남아있을 수 있으므로 추가 공시(get_disclosure_list) 병행 확인 필수
        - SPC 등 특수목적회사(Special Purpose Company)의 해산은 일반 기업 해산과 해석이 다를 수 있으니 맥락을 구분하여 분석
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""
        상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 유상증자 결정을 조회하는 도구입니다.
        기업의 자금 조달 전략, 기존 주주의 지분 희석 가능성, 성장 투자 또는 재무구조 개선 의도를 조기에 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 회사명(corp_name), 고유번호(corp_code), 법인구분(corp_cls): 유상증자 주체 식별
        - 신주의 종류와 수(nstk_ostk_cnt, nstk_estk_cnt): 발행 예정 신주의 수량 (보통주, 기타주식 구분)
        - 1주당 액면가액(fv_ps): 기본 주식 가치 평가 기준
        - 증자 전 발행주식총수(bfic_tisstk_ostk, bfic_tisstk_estk): 기존 주식수와 비교하여 희석율 분석
        - 증자방식(ic_mthn): 주주배정, 제3자배정, 일반공모 등 방식 확인
        - 자금조달 목적별 금액(fdpp_fclt, fdpp_bsninh, fdpp_op, fdpp_dtrp, fdpp_ocsa, fdpp_etc): 시설자금, 운영자금, 채무상환 등 자금 사용 계획 파악
        - 공매도 해당여부(ssl_at), 시작일(ssl_bgd), 종료일(ssl_edd): 증자 관련 공매도 리스크 여부 확인

        【연계 분석 도구】
        - get_stock_total: 유상증자 후 총 주식수 변동 확인
        - get_major_holder_changes: 유상증자 이후 주요 주주 지분 변동 모니터링
        - get_single_acc: 자본금 및 부채비율 변동 여부 심층 분석
        - get_disclosure_list: 유상증자 관련 후속 공시 병행 추적

        【활용 시나리오】
        - 신주 발행수(nstk_ostk_cnt)와 기존 주식수(bfic_tisstk_ostk) 비교하여 기존 주주 지분 희석률 계산
        - 자금조달 목적별 항목 분석으로 성장 투자 목적(시설투자 중심) vs 부채 상환 목적(채무상환 중심) 구분
        - 제3자배정(ic_mthn) 여부를 통해 지배구조 변동 가능성 평가
        - get_major_holder_changes 호출하여 대주주 지분 희석 및 신규 주주 진입 여부 탐지
        - 공매도 허용 여부(ssl_at)가 O일 경우, 증자 직후 주가 급락 리스크 추가 점검

        【효과적 활용 방법】
        - 유상증자 발행수 대비 기존 발행주식수를 기반으로 희석율을 수치화하여 투자 리스크 평가
        - 자금조달 목적 중 운영자금(fdpp_op) 비중이 지나치게 높을 경우 단기 유동성 문제를 의심
        - 제3자배정 방식(ic_mthn) 선택 시, 수혜자(배정 대상자)와의 관계를 분석하여 특혜성 증자 여부 검토
        - 증자 후 get_single_acc 호출로 자본금 변동 및 부채비율 개선 여부 실제 확인

        【주의사항 및 팁】
        - 유상증자 결정만으로 최종 발행이 확정된 것은 아니므로, 추가 공시(get_disclosure_list)로 확정 여부를 지속 추적해야 합니다.
        - 자금조달 목적별 배분 비율이 명확히 제시되지 않은 경우, 향후 자금 사용처 변경 가능성도 고려해야 합니다.
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""
        상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 무상증자 결정을 조회하는 도구입니다.
        기업이 자본구조를 조정하거나, 내부 잉여금을 자본금으로 전환하는 숨은 의도, 주주구성 변화 가능성, 지배구조 강화/변경 시도 여부를 분석하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 회사명(corp_name), 고유번호(corp_code), 법인구분(corp_cls): 무상증자 대상 기업 식별
        - 신주의 종류와 수(nstk_ostk_cnt, nstk_estk_cnt): 보통주 및 기타주식 발행 예정 수량
        - 1주당 액면가액(fv_ps): 신주 발행 기준 단가
        - 증자 전 발행주식총수(bfic_tisstk_ostk, bfic_tisstk_estk): 기존 주식 수량
        - 신주배정기준일(nstk_asstd): 신주배정 기준일 (기준일 직전 주주명부 기준)
        - 1주당 신주배정 주식수(nstk_ascnt_ps_ostk, nstk_ascnt_ps_estk): 무상 배정 비율
        - 신주의 배당기산일(nstk_dividrk): 신주에 대한 배당 권리 발생일
        - 신주권교부예정일(nstk_dlprd): 신주권 교부 예정 시점
        - 신주의 상장 예정일(nstk_lstprd): 발행 신주의 시장 유통 예정 시점
        - 이사회결의일자(bddd): 무상증자 결정일
        - 사외이사 참석여부(od_a_at_t, od_a_at_b), 감사 참석여부(adt_a_atn): 의사결정의 적법성 및 투명성 검토용 데이터

        【연계 분석 도구】
        - get_stock_total: 무상증자 이후 총 발행주식수 변동 분석
        - get_major_holder_changes: 무상증자 이후 주요 주주의 지분율 변동 및 지배구조 변화 모니터링
        - get_single_acc: 자본잉여금 사용 여부, 자본금 증가 구조 분석
        - get_disclosure_list: 무상증자 관련 추가 공시(변경 공시, 수정 공시 등) 병행 모니터링

        【활용 시나리오】
        - 신주배정 비율(nstk_ascnt_ps_ostk)과 기존 발행주식총수(bfic_tisstk_ostk) 비교로 지분 희석 가능성 평가
        - 무상증자 비율이 과도할 경우, 내부 유보금의 자본금 전환을 통한 재무제표 상 착시 개선 시도 가능성 탐지
        - get_major_holder_changes 호출로 무상증자 이후 주요 주주의 지분 희석 방지 또는 신규 세력 진입 여부 분석
        - get_single_acc 분석을 통해 자본잉여금 감소 및 자본금 증가 비율 비교로 재무구조 재편 목적 평가
        - 이사회결의(bddd)와 사외이사, 감사 참석 여부를 통해 의사결정 절차의 적법성과 리스크 사전 감지

        【효과적 활용 방법】
        - 1주당 신주배정수와 기존 주식총수를 비교하여 희석 효과를 정량화하고, 지배구조 변화 가능성 사전 탐지
        - 무상증자 결정 직후 get_disclosure_list로 수정공시 여부를 추적하여 계획 변경 가능성 조기 탐색
        - get_single_acc를 통해 무상증자 이후 자본항목 구조 변동을 정밀 분석하여, 자본건전성 개선 여부 판단
        - 주요 주주 지분율(get_major_holder_changes) 변동을 통해 경영권 방어 또는 지배구조 개편 시도 여부를 분석

        【주의사항 및 팁】
        - 무상증자가 단기 재무구조 개선 착시를 유도하는 수단으로 활용될 수 있으므로, 자본잉여금 출처와 재무제표 변화를 면밀히 분석해야 합니다.
        - 신주배정비율이 비정상적으로 높거나, 사외이사 및 감사 출석률이 낮은 경우, 무상증자 목적의 투명성 문제를 의심해야 합니다.
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""
        상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 유상증자와 무상증자 결정을 동시에 조회하는 도구입니다.
        기업이 자본구조를 대규모로 조정하거나, 내부자금과 외부자금을 복합적으로 활용하는 의도, 지배구조 변동 가능성, 재무 리스크 대응 전략을 분석하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 회사명(corp_name), 고유번호(corp_code), 법인구분(corp_cls): 증자 대상 기업 식별

        【유상증자 관련】
        - 유상 신주 종류와 수(piic_nstk_ostk_cnt, piic_nstk_estk_cnt): 보통주, 기타주식 발행 수량
        - 1주당 액면가(piic_fv_ps): 발행 기준 단가
        - 증자 전 발행주식총수(piic_bfic_tisstk_ostk, piic_bfic_tisstk_estk): 기존 주식 대비 희석률 분석
        - 자금조달 목적별 금액(piic_fdpp_fclt, piic_fdpp_bsninh, piic_fdpp_op, piic_fdpp_dtrp, piic_fdpp_ocsa, piic_fdpp_etc): 시설투자, 영업양수, 채무상환 등 세부 자금 사용 계획
        - 증자방식(piic_ic_mthn): 주주배정, 제3자배정, 일반공모 등 방식 구분

        【무상증자 관련】
        - 무상 신주 종류와 수(fric_nstk_ostk_cnt, fric_nstk_estk_cnt): 보통주, 기타주식 발행 수량
        - 1주당 액면가(fric_fv_ps): 무상 신주의 액면가
        - 증자 전 발행주식총수(fric_bfic_tisstk_ostk, fric_bfic_tisstk_estk): 무상증자 희석 영향 분석
        - 신주배정기준일(fric_nstk_asstd): 무상증자 기준일
        - 1주당 신주배정수(fric_nstk_ascnt_ps_ostk, fric_nstk_ascnt_ps_estk): 배정 비율
        - 신주의 배당기산일(fric_nstk_dividrk): 무상 신주 배당 권리 기준일
        - 신주권교부예정일(fric_nstk_dlprd), 상장 예정일(fric_nstk_lstprd): 유통 시점 확인
        - 이사회결의일자(fric_bddd): 무상증자 결정일
        - 사외이사 참석여부(fric_od_a_at_t, fric_od_a_at_b), 감사 참석여부(fric_adt_a_atn): 결정 절차의 합법성 평가

        【공매도 관련】
        - 공매도 허용 여부(ssl_at) 및 공매도 기간(ssl_bgd, ssl_edd): 증자 전후 시장 통제 여부 확인

        【연계 분석 도구】
        - get_stock_total: 유무상증자 이후 총 발행주식수 변동 분석
        - get_major_holder_changes: 증자 이후 주요 주주 지분율 변화 분석
        - get_single_acc: 자본금 및 자본잉여금 변화 심층 분석
        - get_disclosure_list: 추가 자금조달 계획, 증자 변경 등 후속 공시 실시간 추적

        【활용 시나리오】
        - 유상 및 무상증자 비율 분석을 통해 지배구조 강화 목적(예: 대주주 지분율 방어) 여부 탐지
        - 자금조달 목적별 항목을 통해 재무구조 개선 시도 vs 신규사업 투자 목적 구분
        - 증자방식(piic_ic_mthn)을 분석하여 경영권 변동 위험성 평가
        - 무상증자 배정비율(fric_nstk_ascnt_ps_ostk) 분석을 통해 주식수 급증에 따른 지분희석 리스크 조기 감지
        - 공매도 허용 여부를 통해 증자 직후 시장 리스크 가능성 사전 점검
        - get_major_holder_changes 호출로 주요 주주 구조 재편 및 지배력 강화 시도 여부 분석

        【효과적 활용 방법】
        - 유상 및 무상 신주 발행 총합 대비 기존 주식총수를 비교하여 실제 희석률 정량 분석
        - 유상증자 자금 사용 계획에서 채무상환 목적이 과도할 경우 단기 유동성 문제 가능성 주의
        - 무상증자 기준일과 상장 예정일 분석을 통해 경영진이 유통 주식수를 급격히 확대하려는 의도를 탐지
        - get_single_acc를 통해 자본항목 변동 여부를 상세 검토하여 재무구조 안정성 여부 확인
        - 추가 공시(get_disclosure_list)를 병행 모니터링하여 계획 변경 가능성 실시간 탐지

        【주의사항 및 팁】
        - 유무상증자 동시 진행은 복합적 목적(재무구조 개선, 주주 친화 정책, 지배구조 변경 등)이 얽혀있을 수 있으므로 단일 지표로 판단하지 말고, 여러 데이터 간 상호관계를 종합 분석해야 합니다.
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""
        상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 감자(자본금 감소) 결정을 조회하는 도구입니다.
        기업이 자본구조를 축소하거나, 재무구조를 재편하는 숨은 의도, 잠재적 경영 리스크 대응 전략, 부실 정리 또는 배당가능 재원 확보 목적 여부를 분석하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 회사명(corp_name), 고유번호(corp_code), 법인구분(corp_cls): 감자 대상 기업 식별
        - 감자 주식 종류와 수(crstk_ostk_cnt, crstk_estk_cnt): 보통주 및 기타주식 감자 수량
        - 1주당 액면가액(fv_ps): 감자 전 주식 액면 단가
        - 감자 전후 자본금(bfcr_cpt, atcr_cpt): 감자 전후 자본금 변동 확인
        - 감자 전후 발행주식수(bfcr_tisstk_ostk, atcr_tisstk_ostk, bfcr_tisstk_estk, atcr_tisstk_estk): 발행주식수 변화 분석
        - 감자비율(cr_rt_ostk, cr_rt_estk): 자본금 감축 비율
        - 감자 기준일(cr_std): 감자 기준일 및 기준 주주 식별
        - 감자 방법(cr_mth): 감자 방식(예: 액면감소, 병합, 소각 등)
        - 감자 사유(cr_rs): 경영 전략상 감자 목적 설명
        - 감자 관련 일정(crsc_*): 주주총회 예정일, 구주권 제출기간, 매매거래정지 예정일, 신주권 교부일, 신주 상장일
        - 채권자 이의제출기간(cdobprpd_bgd, cdobprpd_edd): 감자 과정에서 채권자 보호 여부 확인
        - 구주권제출 및 신주권교부장소(ospr_nstkdl_pl): 물리적 감자 절차 진행 정보
        - 이사회결의일자(bddd): 감자 결정일
        - 사외이사 참석여부(od_a_at_t, od_a_at_b), 감사 참석여부(adt_a_atn): 감자 결정의 적법성 및 투명성 평가
        - 공정거래위원회 신고대상 여부(ftc_stt_atn): 감자가 공정거래 규제 대상 여부

        【연계 분석 도구】
        - get_disclosure_list: 감자 이후 추가 경영 이벤트(합병, 해산 등) 모니터링
        - get_single_acc: 감자 전후 자본금, 자본잉여금, 결손금 변동 상세 분석
        - get_major_holder_changes: 감자 이후 주요 주주 지분 변동 여부 추적
        - get_rehabilitation, get_bankruptcy: 감자 이후 회생/부도 가능성 동시 모니터링

        【활용 시나리오】
        - 감자비율(cr_rt_ostk)과 자본금 감소율을 비교하여 구조조정 강도 분석
        - 감자 방법(cr_mth)을 통해 재무구조 단순 조정(액면감소) vs 부실 정리(소각) 여부 구분
        - 감자 사유(cr_rs)를 분석하여 경영진의 자본 재편 의도 및 위험 신호 탐지
        - 이사회결의일자(bddd)와 사외이사, 감사 참석여부를 통해 절차적 합법성 및 리스크 감지
        - get_single_acc 호출로 감자 이후 자본 구조 변화를 정밀 분석하여 회계상 이익 가능성 여부 판단
        - 감자 직후 get_major_holder_changes 호출로 대주주 지분 변동 모니터링하여 경영권 리스크 조기 탐지

        【효과적 활용 방법】
        - 감자 전후 자본금 및 주식수를 수치화하여 재무구조 개선 규모를 정량 분석
        - 감자 사유와 자금 흐름을 연결 분석하여 배당 가능 이익 창출 목적 여부 평가
        - 감자 방법과 감자율, 채권자 이의제출기간 유무를 종합 분석하여 경영진의 리스크 대응 수준 평가
        - 감자 이후 발생하는 모든 공시(get_disclosure_list) 실시간 모니터링을 통해 추가 리스크 조기 포착

        【주의사항 및 팁】
        - 단순 액면감소형 감자라도, 목적이 부실 정리나 부채 상환을 위한 경우, 추가 경영 리스크를 동반할 수 있으므로, 감자사유(cr_rs)와 재무제표(get_single_acc)를 반드시 교차 검토해야 합니다.
        - 주주총회에서 감자 결정이 부결되거나, 채권자 이의가 접수되는 경우 계획이 변경될 수 있으므로, 이후 공시(get_disclosure_list) 모니터링을 지속해야 합니다.
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 채권은행 등 관리절차 개시 사실을 조회하는 도구입니다.
        기업이 재무적 위기를 맞아 채권단 관리 하에 들어간 경우를 신속히 파악할 수 있으며, 경영정상화 가능성, 재무구조 변동 가능성 등을 분석하는 데 활용됩니다.
        
        【핵심 제공 데이터】
        - 관리절차 개시 결정일자(mngt_pcbg_dd): 채권자 관리 절차가 공식적으로 시작된 일자
        - 관리기관(mngt_int): 관리절차를 감독하는 주관 채권은행 또는 채권자협의회 정보
        - 관리기간(mngt_pd): 채권자 관리 하에 있는 기간
        - 관리사유(mngt_rs): 관리절차 개시의 배경 및 사유 (예: 유동성 악화, 경영 정상화 추진 등)
        - 확인일자(cfd): 공시 확인일
        - 회사명(corp_name), 고유번호(corp_code), 법인구분(corp_cls): 관리절차 대상 기업의 기본 정보
        - 접수번호(rcept_no): 공시 상세내역 추적용 식별자

        【연계 분석 도구】
        - get_disclosure_list: 관리절차 개시 전후 주요 공시 변동사항 탐색
        - get_bankruptcy: 관리절차 진행 중 부도 발생 여부 병행 모니터링
        - get_rehabilitation: 관리절차 이후 회생절차 개시 여부 확인
        - get_major_holder_changes: 관리절차 개시 이후 주요 주주 지분 변동 여부 모니터링
        - get_single_acc: 관리기간 내 재무제표 변동 심층 분석

        【활용 시나리오】
        - 관리기관(mngt_int)이 산업은행 등 공적 금융기관인 경우, 기업 지원 가능성 및 구조조정 방향성 예측
        - 관리사유(mngt_rs) 분석을 통해 단순 유동성 위기 vs 구조적 부실 여부 구분
        - 관리기간(mngt_pd) 종료 시점 전후로 추가 공시(get_disclosure_list) 집중 모니터링하여 조기 정상화 가능성 탐색
        - 관리개시 이후 get_single_acc를 통해 유동성, 부채비율 변동 여부 정밀 분석
        - 주요주주(get_major_holder_changes) 변동사항을 통해 경영권 변동 리스크 조기 감지

        【효과적 활용 방법】
        - 관리절차 개시 결정일자(mngt_pcbg_dd) 기준으로 6개월 내 공시 변동 사항 집중 분석
        - 관리기간(mngt_pd)이 짧은 경우 조기 정상화 가능성, 긴 경우 구조조정 가능성 검토
        - 관리기관(mngt_int)이 복수 기관일 경우, 주관 기관의 특성과 구제 방식 차이를 비교 분석
        - 관리사유(mngt_rs)를 통해 자발적 정상화 추진 여부 또는 채권단 주도의 강제 구조조정 여부 판단

        【주의사항 및 팁】
        - 관리절차 개시만으로 경영 정상화를 보장할 수 없으므로, 이후 부도(get_bankruptcy) 및 회생절차(get_rehabilitation) 병행 가능성 주의
        - 관리기간 종료 전후 추가 공시(get_disclosure_list) 및 주요주주 변동(get_major_holder_changes)을 반드시 병행 분석해야 조기 리스크 포착 가능
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 소송 제기 사실을 조회하는 도구입니다. 
        기업이 소송에 휘말린 경우 발생할 수 있는 재무 리스크, 경영 리스크, 지배구조 리스크를 조기에 탐지하고 대응 전략을 수립하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 사건의 명칭(icnm): 소송의 공식 명칭 및 사건번호
        - 원고ㆍ신청인(ac_ap): 소송을 제기한 당사자
        - 청구내용(rq_cn): 소송의 청구취지 및 구체적 요구사항
        - 관할법원(cpct): 사건이 제기된 법원 정보
        - 향후대책(ft_ctp): 기업 측 대응 계획 및 방침
        - 제기일자(lgd): 소송이 제기된 날짜
        - 확인일자(cfd): 공시 확인 기준일
        - 회사명(corp_name), 고유번호(corp_code), 법인구분(corp_cls): 소송 대상 기업 식별 정보
        - 접수번호(rcept_no): 공시 상세내역 조회용 식별자

        【연계 분석 도구】
        - get_disclosure_list: 소송 제기 전후 기업의 주요 공시 변동사항 탐색
        - get_major_holder_changes: 소송 관련 경영권 분쟁 리스크 탐색
        - get_executive_trading: 소송 발생 이후 임원 및 주요주주의 주식 거래 변동 여부 모니터링
        - get_single_acc: 소송 금액 규모에 따른 재무제표 변동성 심층 분석
        - get_business_suspension: 소송 결과에 따른 사업 정지 리스크 병행 점검

        【활용 시나리오】
        - 청구내용(rq_cn) 분석을 통해 소송이 재무적 손실 리스크(예: 손해배상 청구)인지, 경영권 분쟁 리스크(예: 주주총회 결의 무효 등)인지 구분
        - 사건의 명칭(icnm)과 관할법원(cpct)을 통해 소송의 중요도와 심급(1심/항소심 등) 파악
        - 향후대책(ft_ctp) 내용을 분석하여 기업의 방어전략, 합의 가능성, 장기화 리스크 평가
        - 소송 제기일자(lgd) 이후 get_disclosure_list를 통해 후속 소송, 추가 공시 여부 모니터링
        - 대규모 소송인 경우 get_single_acc를 활용하여 충당부채 반영 여부 및 재무건전성 영향 분석

        【효과적 활용 방법】
        - 소송 청구금액이 명시된 경우, 총자산 대비 비율을 계산하여 재무적 충격 가능성 수치화
        - 소송이 경영권 분쟁 성격을 가지는 경우, get_major_holder_changes로 주요주주 지분 변동 탐지
        - 향후대책(ft_ctp)이 단순 대응 예고에 그칠 경우, 실제 방어 가능성이나 리스크를 보수적으로 평가
        - 관할법원이 고등법원, 대법원 등인 경우 사건 심각성을 상향 평가하여 리스크 관리 강화

        【주의사항 및 팁】
        - 청구내용(rq_cn)만으로 소송 결과를 예단하지 말고, 법원의 판결이나 합의 진행 상황을 추가 모니터링해야 함
        - 복수 소송 진행 중일 경우, get_disclosure_list로 관련 사건 모두 추적 필요
        - 향후대책(ft_ctp)이 구체적이지 않은 경우, 기업의 리스크 대응 역량을 추가 검증하는 것이 바람직함
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 해외증권시장 주권 등 상장 결정을 공시한 내역을 조회하는 도구입니다. 
        기업의 글로벌 자금 조달 전략, 성장성 확보 의지, 해외 투자자 기반 확대 여부를 평가하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 상장예정주식 종류 및 수량(lstprstk_ostk_cnt, lstprstk_estk_cnt): 해외 상장 예정 주식 수량을 통해 조달 규모 및 주식구조 변동 가능성 파악
        - 발행주식 총수(tisstk_ostk, tisstk_estk): 상장 후 전체 주식 수 대비 희석율 분석
        - 공모방법(psmth_nstk_sl, psmth_ostk_sl): 신주발행 및 구주매출 비율을 통해 자금조달 목적 구분
        - 자금조달 목적(fdpp): 신사업 투자, 연구개발 등 구체적 사용 계획 확인
        - 상장거래소 및 소재국(lstex_nt): 상장국가 및 거래소를 통한 투자자 기반 다변화 여부 평가
        - 해외상장 목적(lstpp): 상장 전략 및 숨은 의도 파악(예: 글로벌 브랜드 강화, 외화조달 등)
        - 상장예정일자(lstprd): 예상 상장 시점을 통한 시장 영향 시기 예측
        - 이사회결의일자(bddd), 사외이사 참석여부(od_a_at_t, od_a_at_b), 감사 참석여부(adt_a_atn): 의사결정 절차의 투명성 및 합법성 점검

        【연계 분석 도구】
        - get_disclosure_list: 상장 결의 전후 관련 주요 공시 동시 모니터링
        - get_major_holder_changes: 해외상장 이후 주요 주주의 지분율 변동 여부 추적
        - get_single_acc: 해외상장 전후 자본구조, 재무상태 변동 분석
        - get_executive_trading: 상장 결의 직후 경영진 및 주요주주의 주식거래 패턴 변화 분석

        【활용 시나리오】
        - lstprstk_ostk_cnt와 tisstk_ostk를 비교하여 기존 주주 희석율 및 추가 자금유입 규모 분석
        - psmth_nstk_sl, psmth_ostk_sl 비율을 통해 신주발행 중심인지 기존주주 구주매출 중심인지 구분
        - fdpp(자금조달목적) 검토를 통해 자금 사용처가 성장 투자 중심인지 단순 차입 상환 중심인지 판단
        - lstex_nt(상장거래소 소재국) 분석을 통해 해당 시장 특성(규제환경, 투자자 성향 등) 파악
        - bddd(이사회결의일자) 이후 get_disclosure_list로 추가 해외진출 전략, 제휴 등 후속 공시 추적

        【효과적 활용 방법】
        - lstpp(해외상장 목적)와 fdpp(자금조달 목적)를 교차 분석하여 단순 자금조달 목적 상장인지, 전략적 글로벌 진출인지 구분
        - 사외이사 참석률(od_a_at_t, od_a_at_b) 및 감사 참석여부(adt_a_atn)를 통해 이사회 결의의 투명성 및 합법성 점검
        - 상장거래소(lstex_nt)가 글로벌 주요 거래소인지, 신흥시장인지에 따라 투자 리스크 구분
        - lstprd(상장예정일자) 기준으로 상장 전후 공시와 주가 변동 모니터링

        【주의사항 및 팁】
        - lstprd(상장예정일자)가 임박해도 연기되거나 철회되는 경우가 있으므로 이후 공시를 지속 모니터링해야 합니다.
        - psmth_ostk_sl(구주매출)이 지나치게 높은 경우, 기존 대주주의 지분 매각 의도가 있는지 추가 점검 필요
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 해외 증권시장 주권 등 상장폐지 결정을 공시한 내역을 조회하는 도구입니다. 
        기업의 글로벌 시장 철수 전략, 투자자 신뢰도 변화, 지배구조 재편 가능성 등을 조기에 파악하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 상장폐지주식 종류 및 수량(dlststk_ostk_cnt, dlststk_estk_cnt): 해외 시장에서 철수하는 주식 수량을 통해 전체 자본구조에 미치는 영향 분석
        - 상장거래소 및 소재국(lstex_nt): 상장폐지 대상 거래소 및 국가 확인을 통한 시장별 철수 전략 분석
        - 폐지신청예정일자(dlstrq_prd) 및 폐지(예정)일자(dlst_prd): 폐지 절차 진행 일정 파악 및 시장 반응 예측
        - 폐지사유(dlst_rs): 해외 상장 철회 배경(사업 전략 변경, 거래량 부족, 규제 변화 등) 구체적 분석
        - 이사회결의일자(bddd), 사외이사 참석여부(od_a_at_t, od_a_at_b), 감사 참석여부(adt_a_atn): 상장폐지 결정 과정의 투명성과 합법성 검토

        【연계 분석 도구】
        - get_disclosure_list: 상장폐지 전후 관련 주요 공시 동시 모니터링
        - get_major_holder_changes: 해외상장 폐지 이후 주요 주주 지분율 변동 여부 추적
        - get_single_acc: 해외사업 관련 자산, 부채 항목 변동 심층 분석
        - get_executive_trading: 상장폐지 직후 경영진 및 주요주주 주식 거래 패턴 변화 분석

        【활용 시나리오】
        - 폐지사유(dlst_rs)를 통해 사업 철수(예: 해외사업 포기)와 단순 구조조정(예: 원주전환) 여부 구분
        - dlstrq_prd와 dlst_prd를 활용하여 폐지 절차 진행 속도 및 예상 충격 시점 예측
        - lstex_nt(상장거래소 소재국)를 기준으로 철수 지역 및 해당 지역 사업 영향도 분석
        - bddd(이사회결의일자) 이후 get_disclosure_list로 추가 철수 관련 공시(사업종료, 인력감축 등) 연계 추적
        - 사외이사/감사 참석여부를 통해 의사결정 투명성 및 주주보호 여부 점검

        【효과적 활용 방법】
        - dlststk_ostk_cnt 대비 전체 발행주식수 분석을 통해 철수에 따른 자본구조 변동성 평가
        - 폐지사유(dlst_rs)와 get_single_acc의 해외매출 비중 교차 분석 → 실제 사업 철수 리스크 평가
        - get_major_holder_changes와 연계하여 대주주 이탈 리스크 사전 탐지
        - get_executive_trading으로 폐지 결의 이후 내부자 매매 패턴 변화 모니터링
        - dlstrq_prd, dlst_prd 기준으로 공시 빈도 및 이슈 확산 경로 분석

        【주의사항 및 팁】
        - 폐지사유가 단순 원주전환인 경우(예: GDR 전환)와 사업 철수 목적의 폐지는 구분해서 해석해야 합니다.
        - 폐지 이후에도 해당 지역에서 사업을 지속할 수 있으므로 사업 철수 여부는 추가 공시(get_disclosure_list)로 최종 확인해야 합니다.
        - 이사회 결의에서 사외이사 불참 비율이 높거나 감사 불참 시, 절차상 리스크를 주의 깊게 검토해야 합니다.
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 해외 증권시장 주권 등 상장 사실을 공시한 내역을 조회하는 도구입니다. 
        기업의 글로벌 시장 진출 현황, 해외 투자자 기반 확보, 글로벌 사업 전략 이행 여부를 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 상장주식 종류 및 수(lststk_ostk_cnt, lststk_estk_cnt): 해외 상장 대상 보통주 및 기타주식 수량을 통해 자금조달 규모 및 지배구조 변화 가능성 평가
        - 상장거래소(소재국가)(lstex_nt): 상장 거래소 및 국가를 통해 목표 시장 특성 및 규제 환경 분석
        - 종목명(stk_cd): 해외 상장 종목 코드 확인으로 거래 가능성 및 투자 접근성 평가
        - 상장일자(lstd): 실제 상장 완료 시점을 기준으로 글로벌 시장 진입 시기 분석
        - 확인일자(cfd): 상장 관련 최종 확인 시점을 통한 공시 이행 여부 점검
        - 접수번호(rcept_no): 상세 공시문 접근 및 추가 정보 조회를 위한 식별자 제공

        【연계 분석 도구】
        - get_foreign_listing_decision: 최초 상장 결정 공시와 실제 상장 완료 간 일관성 분석
        - get_foreign_delisting_decision: 상장 이후 폐지 위험 여부 모니터링
        - get_major_holder_changes: 해외상장 전후 주요 주주 지분율 변동 분석
        - get_single_acc: 해외사업 관련 매출/자산 비중 및 외화 부채 구조 분석
        - get_disclosure_list: 상장 전후 관련 전략 변화 및 자금조달 계획 후속 공시 추적

        【활용 시나리오】
        - lststk_ostk_cnt, lststk_estk_cnt를 통해 해외 조달 규모 및 기존 주주 희석 가능성 예측
        - lstex_nt(상장거래소)별 규제 강도 및 투자자 유형 분석을 통해 향후 공시 부담 및 리스크 평가
        - stk_cd(종목명)을 활용하여 해당 증권의 실제 거래 활성화 여부 및 인지도 파악
        - lstd(상장일자)와 cfd(확인일자)를 비교하여 상장 프로세스 지연 여부 분석
        - get_major_holder_changes로 상장 이후 주요 주주의 지분 변동 가능성 사전 탐지

        【효과적 활용 방법】
        - 상장주식 수량(lststk_ostk_cnt, lststk_estk_cnt) 정보가 비어 있을 경우, 발행 방식(ADR, GDR 등)과 발행비율을 별도로 확인하여 해석해야 합니다.
        - 상장거래소(lstex_nt)가 글로벌 주요 시장(예: NYSE, NASDAQ)인지 여부에 따라 시장 신뢰도와 기업 인지도 평가
        - stk_cd(종목명)을 기준으로 실제 거래 개시 여부 및 상장 성공 여부를 사후 점검
        - get_disclosure_list를 통해 상장 이후 자금조달 확대나 추가 상장 계획 공시 여부를 지속 모니터링해야 합니다.

        【주의사항 및 팁】
        - lstex_nt(상장거래소 소재국가)와 lstd(상장일자)만으로 글로벌 사업 확장 성공 여부를 단정하지 말고, get_single_acc를 통해 해외 매출/자산 비중 변화를 병행 분석해야 합니다.
        - 상장 직후에도 get_major_holder_changes를 통해 내부자 지분 이동 여부를 지속 모니터링하여 경영권 리스크를 조기에 탐지해야 합니다.
        - 종목명(stk_cd) 부여만으로 거래가 활성화되었는지 알 수 없으므로, 실제 거래량과 시장 반응은 별도로 점검해야 합니다.
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 해외 증권시장 주권 등 상장폐지 사실을 공시한 내역을 조회하는 도구입니다. 
        기업의 글로벌 전략 수정 여부, 투자자 신뢰도 변화, 해외 자본시장 의존도 감소 가능성 등을 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 상장거래소 및 소재국가(lstex_nt): 상장폐지 대상 거래소 및 국가를 통해 해외시장 철수 지역 분석
        - 상장폐지주식 종류 및 수량(dlststk_ostk_cnt, dlststk_estk_cnt): 폐지되는 주식 종류와 수량을 통해 자본구조 변동성 평가
        - 매매거래종료일(tredd): 실제 거래 종료 시점을 통해 시장 영향 시점 분석
        - 폐지사유(dlst_rs): 상장폐지 결정의 구체적 원인(예: 원주전환, 거래부진, 자발적 철수 등) 분석
        - 확인일자(cfd): 상장폐지 사실 최종 확정 시점 확인
        - 접수번호(rcept_no): 상세 공시문 접근 및 추가 분석을 위한 식별자 제공

        【연계 분석 도구】
        - get_foreign_delisting_decision: 상장폐지 결정 공시와 실제 폐지 완료 여부 비교 분석
        - get_disclosure_list: 상장폐지 전후 추가 전략 변화 및 사업구조 조정 공시 모니터링
        - get_major_holder_changes: 상장폐지 전후 주요 주주 지분 변동 여부 추적
        - get_single_acc: 해외 자산 및 매출 비중 변화 여부 분석
        - get_executive_trading: 상장폐지 직후 주요 경영진 및 대주주 주식거래 패턴 변화 모니터링

        【활용 시나리오】
        - dlst_rs(폐지사유)를 통해 단순 구조조정(GDR 전환 등)과 사업 철수 목적의 상장폐지 구분
        - tredd(매매거래종료일) 기준으로 폐지 영향 시점과 시장 충격 타이밍 분석
        - lstex_nt(상장거래소 소재국가) 기준으로 해외시장 포기 지역과 남은 글로벌 거점 비교 분석
        - get_major_holder_changes를 활용하여 상장폐지 이후 대주주 지분 매각 또는 이탈 리스크 조기 탐지
        - get_single_acc를 통해 폐지 지역 관련 매출/자산 비중 축소 여부 심층 분석

        【효과적 활용 방법】
        - dlststk_ostk_cnt, dlststk_estk_cnt가 "-"로 표시된 경우, 실제 폐지 영향 규모를 별도로 확인해야 정확한 분석이 가능합니다.
        - 폐지사유(dlst_rs)가 "GDR 전량 원주전환"일 경우, 실질적 사업 철수가 아니라 단순 상장구조 변경 가능성으로 구분해야 합니다.
        - 매매거래종료일(tredd) 직전 30일 내 get_disclosure_list를 통해 추가 구조조정, 사업철수 계획 공시를 병행 모니터링해야 합니다.
        - 상장폐지 이후 get_single_acc를 활용하여 해외자산 비중 변화, 외화부채 구조 변동을 추가 분석해야 합니다.

        【주의사항 및 팁】
        - 폐지사유가 단순 구조적 변경(GDR 전환)인지, 본격적인 해외시장 철수인지 구체적으로 구분하여 리스크 평가해야 합니다.
        - tredd(매매거래종료일)과 실제 상장폐지일 간 차이가 발생할 수 있으므로 확인일자(cfd) 기준으로 이행 완료 여부를 최종 확인해야 합니다.
        - 폐지 이후에도 해외사업 자체가 지속되는 경우가 있으므로, 단순 상장폐지와 사업 철수는 구분하여 해석해야 합니다.
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 전환사채권 발행 결정을 공시한 내역을 조회하는 도구입니다. 
        기업의 자금조달 전략, 부채 리스크, 향후 주식수 변동 가능성 및 지배구조 영향 여부를 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 사채 종류 및 회차(bd_tm, bd_knd): 발행 사채의 종류와 특성(무보증, 후순위 등) 파악
        - 사채 총액(bd_fta): 조달 규모를 통한 재무 레버리지 영향 평가
        - 자금조달 목적(fdpp_fclt, fdpp_bsninh, fdpp_op, fdpp_dtrp, fdpp_ocsa, fdpp_etc): 시설자금, 영업양수자금, 운영자금, 부채상환 등 구체적 사용 계획 분석
        - 이율(bd_intr_ex, bd_intr_sf) 및 만기일(bd_mtd): 사채의 금리 부담과 만기구조 평가
        - 발행방법(bdis_mthn): 공모/사모 여부를 통한 투자자층 분석
        - 전환비율(cv_rt), 전환가액(cv_prc), 전환발행주식 종류 및 수량(cvisstk_knd, cvisstk_cnt): 주식 전환 가능성에 따른 주주가치 희석 리스크 분석
        - 전환청구기간(cvrqpd_bgd, cvrqpd_edd): 주식 전환 가능 시점과 기간 확인
        - 시가하락에 따른 전환가액 조정조건(act_mktprcfl_cvprc_lwtrsprc, act_mktprcfl_cvprc_lwtrsprc_bs): 주가 하락 시 추가 희석 위험 여부 분석
        - 이사회결의일자(bddd), 사외이사 참석여부(od_a_at_t, od_a_at_b), 감사 참석여부(adt_a_atn): 발행결정의 투명성과 합법성 점검
        - 대표주관회사(rpmcmp), 보증기관(grint): 발행 안정성 평가
        - 증권신고서 제출여부(rs_sm_atn), 공정거래위원회 신고여부(ftc_stt_atn): 법적 절차 준수 여부 확인

        【연계 분석 도구】
        - get_stock_increase_decrease: 전환 후 주식총수 변동 여부 분석
        - get_major_holder_changes: 전환사채 발행 및 전환 완료 후 주요 주주 지분율 변화 추적
        - get_single_acc: 전환사채 발행 이후 재무구조 변화(부채비율, 자본금) 분석
        - get_disclosure_list: 전환 조건 변경, 추가 발행 등 후속 공시 병행 모니터링

        【활용 시나리오】
        - bd_fta(사채총액) 대비 회사 자본 규모(get_single_acc)를 비교하여 레버리지 위험 평가
        - cv_rt(전환비율)와 cvisstk_cnt(전환주식 수)를 통해 희석율 추정
        - fdpp_op, fdpp_dtrp 분석을 통해 유동성 보완 목적 발행인지 성장 투자 목적 발행인지 구분
        - act_mktprcfl_cvprc_lwtrsprc(최저 전환가 조정 조건)이 존재하는 경우, 주가 급락 시 추가 희석 리스크 평가
        - cvrqpd_bgd부터 전환 가능성이 열리므로 해당 시점을 전후하여 get_major_holder_changes로 주요 주주 변동성 모니터링

        【효과적 활용 방법】
        - 전환가액(cv_prc)이 현재 주가 대비 얼마나 차이가 나는지 분석하여 전환 가능성 및 투자자 행동 예측
        - 만기구조(bd_mtd)와 상환 조건을 함께 고려하여 부채 리스크 평가
        - 공모(bdis_mthn) 발행인 경우 다수 투자자 참여로 리스크 분산, 사모 발행 시 특수관계인 집중 가능성 평가
        - 전환사채 발행 후 추가 증자나 전환조건 변경(get_disclosure_list) 가능성도 항상 함께 모니터링

        【주의사항 및 팁】
        - 시가하락 조정조건(act_mktprcfl_cvprc_lwtrsprc)이 있는 경우, 추가 희석 위험을 별도로 계산해야 합니다.
        - 운영자금(fdpp_op) 목적이 전체 조달액의 대부분을 차지할 경우, 단기 유동성 압박을 반영한 발행 가능성도 고려해야 합니다.
        - 전환청구기간(cvrqpd_bgd~cvrqpd_edd) 내 주가 급등락에 따라 주식 수 대량 변동 리스크가 존재할 수 있으므로 연계 공시 모니터링이 필수입니다.
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""신주인수권부사채(BW, Bond with Warrant) 발행 내역을 조회하는 도구입니다. 
        기업의 미래 지분 희석 가능성, 자금조달 목적, 부채 리스크 등을 종합적으로 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 사채 기본정보: 종류(bd_tm, bd_knd), 총액(bd_fta), 만기일(bd_mtd), 이율(bd_intr_ex, bd_intr_sf), 발행방법(bdis_mthn)
        - 자금조달 목적: 시설자금(fdpp_fclt), 영업양수자금(fdpp_bsninh), 운영자금(fdpp_op), 채무상환자금(fdpp_dtrp), 기타자금(fdpp_etc) 항목별 세부금액
        - 신주인수권 세부정보: 행사비율(ex_rt), 행사가격(ex_prc), 행사기간(expd_bgd~expd_edd), 발행주식수(nstk_isstk_cnt), 발행총수 대비 비율(nstk_isstk_tisstk_vs), 분리 여부(bdwt_div_atn)
        - 추가 리스크 요인: 시가하락에 따른 최저가액 조정 가능성(act_mktprcfl_cvprc_lwtrsprc, rmislmt_lt70p) 여부
        - 주요 의사결정 절차: 이사회 결의일(bddd), 사외이사/감사 참석 여부(od_a_at_t, od_a_at_b, adt_a_atn)

        【연계 분석 도구】
        - get_major_holder_changes: BW 발행 이후 주요 주주 지분율 변동 분석
        - get_single_acc: 자본구조 및 부채비율 변동 분석
        - get_disclosure_list: BW 관련 추가 조건 변경 공시 모니터링

        【활용 시나리오】
        - 신주인수권 행사로 인한 지분 희석 리스크 사전 파악
        - 자금조달 목적 분석을 통해 성장 투자용인지, 단기 부채 상환용인지 구분
        - 발행조건(이율, 만기, 분리 여부 등)을 종합적으로 검토해 재무 리스크 진단
        - 행사기간과 행사가격 비교를 통해 투자자 권리행사 가능성 평가
        - 이사회 및 사외이사 출석 정보를 통해 발행의 투명성 및 합법성 점검
        - 시가하락 조정 조항 존재 시, 최악의 경우 투자자 손실 가능성 평가

        【효과적 활용 방법】
        - 신주발행 예상수량(nstk_isstk_cnt)과 기존 주식총수 대비 비율(nstk_isstk_tisstk_vs)을 비교하여 희석율 수치화
        - 행사비율(ex_rt)과 행사가격(ex_prc)을 통해 발행주가 대비 유리성 분석
        - 분리형(bdwt_div_atn=‘분리’) 여부 확인으로 신주인수권 자체 거래 가능성 고려
        - 시가하락 조정 조항이 있을 경우, 최소 행사가격(act_mktprcfl_cvprc_lwtrsprc)와 기준 근거(act_mktprcfl_cvprc_lwtrsprc_bs)를 반드시 검토

        【주의사항 및 팁】
        - 신주인수권부사채는 사채이면서도 주식 전환 리스크를 내포하므로, 부채와 자본 양방향 모두에 영향 분석 필요
        - 행사기간(expd_bgd~expd_edd) 내 주가 급락 시 투자자 보호 장치(최저 행사가격 조정) 유무에 따라 리스크 차이가 크므로 세밀한 확인 필요
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""교환사채(EB, Exchangeable Bond) 발행 내역을 조회하는 도구입니다. 
        기업의 미래 지분 희석 가능성, 자금조달 목적, 부채 리스크, 특정 종목에 대한 전략적 연계 여부 등을 종합적으로 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 사채 기본정보: 종류(bd_tm, bd_knd), 총액(bd_fta), 만기일(bd_mtd), 이율(bd_intr_ex, bd_intr_sf), 발행방법(bdis_mthn)
        - 자금조달 목적: 시설자금(fdpp_fclt), 영업양수자금(fdpp_bsninh), 운영자금(fdpp_op), 채무상환자금(fdpp_dtrp), 기타자금(fdpp_etc) 항목별 세부금액
        - 교환권 세부정보: 교환대상종목(extg), 교환주식수(extg_stkcnt), 교환총수 대비 비율(extg_tisstk_vs), 교환비율(ex_rt), 교환가액(ex_prc), 교환청구기간(exrqpd_bgd~exrqpd_edd)
        - 추가 리스크 요인: 이사회 결의일(bddd), 사외이사 및 감사 참석 여부(od_a_at_t, od_a_at_b, adt_a_atn)
        - 신고 여부: 증권신고서 제출 여부(rs_sm_atn) 및 제출면제 사유(ex_sm_r)

        【연계 분석 도구】
        - get_major_holder_changes: EB 발행 이후 주요 주주 지분율 변동 분석
        - get_single_acc: 교환사채 발행 전후 재무구조 및 부채비율 변동 분석
        - get_disclosure_list: 교환사채 관련 추가 변경 공시 모니터링

        【활용 시나리오】
        - 교환대상종목(extg) 분석을 통해 특정 기업 주가와 연동된 리스크 평가
        - 교환비율(ex_rt) 및 교환가액(ex_prc)을 통해 실제 행사 시 희석 가능성 수치화
        - 자금조달 목적별 항목 분석을 통해 성장 투자 목적과 부채 상환 목적 구분
        - 행사기간(exrqpd_bgd~exrqpd_edd) 동안 주가 추이 모니터링하여 교환 가능성 예측
        - 이사회 결의(bddd) 및 사외이사/감사 출석 여부를 통해 발행 투명성 및 합법성 점검

        【효과적 활용 방법】
        - 교환주식수(extg_stkcnt)와 기존 발행주식 대비 비율(extg_tisstk_vs)을 기반으로 예상 희석율 계산
        - 교환가액(ex_prc)과 발행 당시 주가 비교하여 투자자 손실 가능성 및 프리미엄 여부 평가
        - 교환기간 종료일(exrqpd_edd) 직전 교환권 행사 집중 여부에 따른 주가 변동성 예측
        - get_single_acc를 통한 부채 및 자본 항목 변화 심층 분석

        【주의사항 및 팁】
        - 교환대상 종목이 비상장 또는 변동성이 큰 경우, 실질 리스크가 예상보다 클 수 있으므로 별도 검토 필요
        - 행사비율(ex_rt)이 100% 이상인 경우, 추가 발행 주식수 증가 가능성 고려 필수
        - 교환사채는 단순 부채 외에도 주가 변동성, 교환 행사 타이밍 리스크를 함께 평가해야 함
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""채권은행 또는 채권금융기관협의회 등의 관리절차(공동관리, 워크아웃 등) 중단 사실을 조회하는 도구입니다. 
        기업의 구조조정 종료 여부, 재무 정상화 진행 상황, 향후 경영 리스크를 종합적으로 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 관리절차 중단일자(mngt_pcsp_dd): 공식적인 관리종료 결정 시점
        - 관리기관(mngt_int): 관리 및 지원을 담당했던 주채권은행 또는 금융기관 협의체 명칭
        - 중단사유(sp_rs): 관리절차 종료의 구체적 사유(예: 채권 매각, 재무개선 완료 등)
        - 향후대책(ft_ctp): 관리 종료 이후의 기업 경영 방향성 및 전략
        - 확인일자(cfd): 공시 확인일자 (※ 관리종료의 법적 효력 발생 시점과 다를 수 있음)

        【연계 분석 도구】
        - get_single_acc: 관리절차 종료 전후 재무구조(자산, 부채, 자본) 변화 분석
        - get_disclosure_list: 관리 종료 이후 추가 공시(증자, 인수합병, 사업확장 등) 모니터링
        - get_major_holder_changes: 관리종료 이후 주요 주주 지분 변동 여부 추적

        【활용 시나리오】
        - 관리절차 종료 기업의 재무 정상화 여부 검토
        - 중단사유(sp_rs) 분석을 통해 정상적 회복(예: 채권 전액 상환)과 비정상적 종료(예: 부실채권 매각) 구분
        - 향후대책(ft_ctp)을 통해 기업의 자율경영 가능성 및 재도약 전략 여부 평가
        - 관리종료 직후 get_single_acc를 호출하여 부채비율, 유동성 지표 개선 여부 확인
        - get_disclosure_list를 통해 관리 종료 이후의 자금조달, 투자 유치, 사업 확대 움직임 모니터링

        【효과적 활용 방법】
        - 관리기관(mngt_int) 분석을 통해 관리 과정에서 주도권을 가졌던 기관(예: 산업은행, 수출입은행 등) 파악
        - 중단사유(sp_rs)와 향후대책(ft_ctp)을 교차 분석하여 정상적 구조조정 완료 여부 평가
        - 관리종료 이후 get_major_holder_changes를 통해 대주주 교체나 경영권 변동 신호 조기 포착
        - 확인일자(cfd)를 기준으로 후속 공시(get_disclosure_list) 집중 모니터링

        【주의사항 및 팁】
        - 관리절차 종료가 재무구조 정상화를 의미하지 않을 수 있으므로, get_single_acc로 실제 개선 여부를 반드시 검증해야 함
        - 향후대책(ft_ctp) 항목이 추상적일 경우, 추가 공시(get_disclosure_list)를 통해 실제 실행 여부를 지속 추적 필요
        - 부실채권 매각 등으로 관리가 종료된 경우, 외형상 정상화와 실질 리스크가 불일치할 수 있으므로 심층 분석 필요
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""상각형 조건부자본증권(Write-down Bond) 발행 내역을 조회하는 도구입니다. 
        기업의 자본 건전성 보완 목적, 부채 관리 전략, 잠재적 재무 리스크(상각 발생 가능성)를 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 사채 기본정보: 종류(bd_tm, bd_knd), 총액(bd_fta), 만기일(bd_mtd), 이율(bd_intr_ex, bd_intr_sf), 발행방법(bdis_mthn)
        - 해외발행 세부정보: 해외발행금액(ovis_fta), 통화단위(ovis_fta_crn), 기준환율(ovis_ster), 발행지역(ovis_isar), 상장시장(ovis_mktnm)
        - 자금조달 목적: 시설자금(fdpp_fclt), 영업양수자금(fdpp_bsninh), 운영자금(fdpp_op), 채무상환자금(fdpp_dtrp), 기타자금(fdpp_etc)
        - 상각 관련 정보: 채무재조정 범위(dbtrs_sc) (예: 사채 원리금 전액 상각 등)
        - 주요 의사결정 이력: 이사회결의일(bddd), 사외이사/감사 참석 여부(od_a_at_t, od_a_at_b, adt_a_atn)
        - 증권신고서 제출 여부(rs_sm_atn) 및 제출 면제 사유(ex_sm_r)

        【연계 분석 도구】
        - get_single_acc: 상각형 채권 발행 전후 재무구조 변동 분석
        - get_major_holder_changes: 발행 이후 주요 주주 지분 변동 여부 모니터링
        - get_disclosure_list: 상각형 채권 발행 이후 추가 공시 모니터링

        【활용 시나리오】
        - 상각형 조건부자본증권 발행 여부를 통해 자본확충 필요성 및 재무구조 개선 의지 평가
        - 상각조건(dbtrs_sc)을 분석하여, 비상 상황 발생 시 재무구조 악화 리스크 파악
        - 해외발행(ovis_fta) 및 통화정보(ovis_fta_crn, ovis_ster)를 통해 외화 리스크 노출 여부 진단
        - 발행 직후 get_single_acc를 통해 자기자본비율, 부채비율 변동 여부 확인
        - 이사회결의일자(bddd) 및 사외이사/감사 출석여부 검토를 통해 의사결정 투명성 평가
        - get_disclosure_list로 상각 조건 변경, 추가 발행 여부 등 후속 리스크 요인 모니터링

        【효과적 활용 방법】
        - 채무재조정 범위(dbtrs_sc)가 '원리금 전액'으로 설정된 경우, 재무제표상 부채 감소와 동시에 자본 훼손 가능성 분석
        - 해외발행비율(ovis_fta) 및 환율정보(ovis_ster)를 기반으로 외화부채 리스크 사전 파악
        - 상각 조건 충족 가능성 평가를 위해 get_single_acc로 자본비율 변동추이 사전 분석
        - get_major_holder_changes를 통해 상각형 조건부자본증권 발행 전후 지배구조 변동 위험 감시

        【주의사항 및 팁】
        - 조건부자본증권은 특정 조건 충족 시 원리금 상각이 발생하므로, 단순 발행 사실 외에도 구체적 상각 조건과 발동 기준을 추가 분석해야 함
        - 해외발행 증권의 경우, 환율 변동에 따른 채무 상환 리스크를 별도로 관리해야 함
        - 발행 이후 자본구조 안정성 확보 여부는 반드시 get_single_acc와 병행 분석 필요
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""자기주식 취득 계획 공시 내역을 조회하는 도구입니다. 
        기업의 주가 방어 전략, 주주환원 정책, 지배구조 변화 가능성 등을 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 취득 예정 내역: 취득예정주식수(aqpln_stk_ostk, aqpln_stk_estk), 취득예정금액(aqpln_prc_ostk, aqpln_prc_estk)
        - 취득 및 보유 기간: 취득예상기간(aqexpd_bgd, aqexpd_edd), 보유예상기간(hdexpd_bgd, hdexpd_edd)
        - 취득 목적 및 방법: 취득목적(aq_pp), 취득방법(aq_mth), 위탁투자중개업자(cs_iv_bk)
        - 취득 전 자기주식 보유 현황: 배당가능이익 범위 내 보유주식(aq_wtn_div_ostk, aq_wtn_div_estk) 및 비율(aq_wtn_div_ostk_rt, aq_wtn_div_estk_rt), 기타취득분(eaq_ostk, eaq_estk)
        - 주요 의사결정 이력: 취득결정일(aq_dd), 이사회결의 사외이사 참석 여부(od_a_at_t, od_a_at_b), 감사위원 참석 여부(adt_a_atn)
        - 1일 매수 주문수량 한도: 보통주식(d1_prodlm_ostk), 기타주식(d1_prodlm_estk)

        【연계 분석 도구】
        - get_single_acc: 자기주식 취득 전후 자본 및 부채구조 변동 분석
        - get_major_holder_changes: 자기주식 취득 이후 주요 주주 지분율 변동 여부 모니터링
        - get_disclosure_list: 자기주식 취득 관련 추가 공시 모니터링

        【활용 시나리오】
        - 취득예정수량 대비 현재 자기주식 보유비율을 비교하여, 지배구조 강화/방어 의도 파악
        - aq_pp(취득목적)이 "주주가치 제고" 외에 있는 경우, 단순 방어목적 외 추가 의도 분석
        - aq_mth(취득방법)이 장내매수인 경우, 직접적인 주가 부양 효과를 예상
        - get_single_acc로 자기주식 취득 전후 자본총계 변동 분석을 통해 재무건전성 영향 평가
        - 이사회결의일자(aq_dd) 및 사외이사/감사 출석 정보 검토로 의사결정 투명성 검증
        - get_major_holder_changes를 통해 주요주주 지분 변동 및 경영권 방어 여부 모니터링

        【효과적 활용 방법】
        - 자기주식 취득비율(aqpln_stk_ostk 대비 aq_wtn_div_ostk_rt)을 통해 경영권 안정성 강화 여부 평가
        - aqexpd_bgd~aqexpd_edd 기간 동안 주가 변동성 모니터링하여 실제 주가 부양 효과 검증
        - 1일 매수 주문수량 한도(d1_prodlm_ostk, d1_prodlm_estk)를 기준으로 취득속도 및 기간 예상
        - cs_iv_bk(위탁중개업자)를 통해 시장 내 매수집행 신뢰성 평가

        【주의사항 및 팁】
        - aq_mth(취득방법)이 장내매수 외 방식일 경우, 취득 영향이 시장에 미치는 정도가 다를 수 있음
        - 배당가능이익 한도 내 보유주식과 기타취득 주식 구분을 명확히 파악하여 법적 문제 가능성 검토 필요
        - 취득계획 발표 후 실제 취득 이행 여부는 별도 공시(get_disclosure_list)로 사후 모니터링 필요
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""자기주식 처분 계획 공시 내역을 조회하는 도구입니다. 
        기업의 주주환원 정책, 자본구조 조정 전략, 또는 경영권 방어 해제 가능성 등을 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 처분 예정 내역: 처분예정주식수(dppln_stk_ostk, dppln_stk_estk), 처분 예정금액(dppln_prc_ostk, dppln_prc_estk), 단위 주당 가격(dpstk_prc_ostk, dpstk_prc_estk)
        - 처분 기간: 처분예정기간 시작일(dpprpd_bgd), 종료일(dpprpd_edd)
        - 처분 목적 및 방법: 처분목적(dp_pp), 시장매도(dp_m_mkt), 시간외대량매매(dp_m_ovtm), 장외처분(dp_m_otc), 기타(dp_m_etc)
        - 위탁투자중개업자: cs_iv_bk
        - 처분 전 자기주식 보유 현황: 배당가능이익 내 취득 주식(aq_wtn_div_ostk, aq_wtn_div_estk) 및 비율(aq_wtn_div_ostk_rt, aq_wtn_div_estk_rt), 기타취득 주식(eaq_ostk, eaq_estk)
        - 주요 의사결정 이력: 처분결정일(dp_dd), 사외이사 참석 여부(od_a_at_t, od_a_at_b), 감사위원 참석 여부(adt_a_atn)
        - 1일 매도 주문수량 한도: 보통주식(d1_slodlm_ostk), 기타주식(d1_slodlm_estk)

        【연계 분석 도구】
        - get_single_acc: 자기주식 처분 전후 자본 및 부채구조 변동 분석
        - get_major_holder_changes: 자기주식 처분 이후 주요 주주 지분율 변동 여부 모니터링
        - get_disclosure_list: 자기주식 처분 관련 추가 공시 모니터링

        【활용 시나리오】
        - 처분 목적(dp_pp)이 "주주환원" 목적이 아닌 경우, 구조적 경영변화 가능성 분석
        - 처분 방식(dp_m_mkt, dp_m_ovtm, dp_m_otc) 구분을 통해 시장 유통 영향력 및 매각 의도 구분
        - get_single_acc를 통해 처분 전후 자본금, 이익잉여금 변동 분석하여 재무구조 개선 여부 평가
        - 처분결정일(dp_dd) 및 이사회결의의 사외이사, 감사 참석 여부 검토로 절차 투명성 평가
        - get_major_holder_changes 호출하여 처분 이후 지배구조 변동 리스크 모니터링

        【효과적 활용 방법】
        - 처분예정주식수 대비 기존 자기주식 비율 비교로, 지분구조 변화 가능성 사전 점검
        - 처분 방법이 시간외대량매매(dp_m_ovtm)일 경우, 특정 투자자에 대한 지분 이동 가능성 검토
        - 처분예정기간(dpprpd_bgd~dpprpd_edd) 동안 주가 변동성 모니터링하여 시장 반응 분석
        - 1일 매도 주문수량 한도(d1_slodlm_ostk, d1_slodlm_estk)를 활용하여 처분 속도 및 시장 영향도 예측

        【주의사항 및 팁】
        - 처분 목적이 모호하거나 기타처분(dp_m_etc) 비중이 높은 경우, 거래 상대방 및 내부자 거래 여부를 주의 깊게 검토
        - 자기주식 처분은 경영권 방어 포기 또는 유동성 확보 전략과 직결될 수 있으므로, 의도 분석이 핵심
        - 처분 완료 후 추가 공시(get_disclosure_list)로 최종 처분 수량 및 금액 확인 필수
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""자기주식 신탁계약 체결 공시 내역을 조회하는 도구입니다. 
        기업의 주가 안정화 정책, 주주환원 전략, 경영권 방어 수단 마련 여부를 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 계약 주요정보: 계약금액(ctr_prc), 계약기간 시작일/종료일(ctr_pd_bgd, ctr_pd_edd), 계약목적(ctr_pp)
        - 계약 체결기관 및 예정일: 계약체결기관(ctr_cns_int), 계약체결 예정일자(ctr_cns_prd)
        - 계약 전 자기주식 보유현황: 배당가능이익 범위 내 보유주식(aq_wtn_div_ostk, aq_wtn_div_estk) 및 비율(aq_wtn_div_ostk_rt, aq_wtn_div_estk_rt), 기타취득 주식(eaq_ostk, eaq_estk)
        - 주요 의사결정 이력: 이사회결의일자(bddd), 사외이사 참석 여부(od_a_at_t, od_a_at_b), 감사위원 참석 여부(adt_a_atn)
        - 위탁투자중개업자: cs_iv_bk

        【연계 분석 도구】
        - get_single_acc: 신탁계약 체결 전후 자본구조 및 부채비율 변동 분석
        - get_major_holder_changes: 신탁계약 체결 이후 주요 주주 지분율 변동 여부 모니터링
        - get_disclosure_list: 신탁계약 관련 후속 공시 모니터링

        【활용 시나리오】
        - 계약목적(ctr_pp)이 "주가 안정화"인지, "스톡옵션 대비"인지에 따라 신탁계약의 전략적 의미 분석
        - 계약금액(ctr_prc)이 기업 자기자본 대비 차지하는 비중을 계산하여 시장 영향력 평가
        - 계약체결기관(ctr_cns_int)의 신뢰성 여부를 확인하여 주가 방어 실효성 검토
        - get_single_acc로 신탁계약 체결 전후 자본총계, 유동성 비율 변화를 추적하여 재무구조 개선 여부 분석
        - 계약기간(ctr_pd_bgd~ctr_pd_edd) 동안 get_disclosure_list를 통해 추가 계약 변경 여부 모니터링

        【효과적 활용 방법】
        - 계약금액 대비 전체 시가총액 비율을 분석하여 실질적 주가 방어 효과 예상
        - 신탁계약 기간 동안 자기주식 처분 가능성 여부를 get_major_holder_changes를 통해 병행 모니터링
        - 계약목적과 실제 주가 흐름 비교를 통해 주주가치 제고 전략의 이행 수준 점검
        - 계약 체결기관(cs_iv_bk)과 계약체결기관(ctr_cns_int)이 불일치할 경우 계약 리스크 재검토

        【주의사항 및 팁】
        - 계약 종료 후 자기주식 처분 계획 여부는 별도 공시(get_disclosure_list)로 확인해야 함
        - 신탁계약이 경영권 방어 수단으로 활용될 수 있으므로, 취득 및 처분 조건을 면밀히 분석할 필요 있음
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""자기주식 신탁계약 해지 내역을 조회하는 도구입니다. 
        신탁계약 종료에 따른 주가 방어 정책 변경, 주주환원 전략 수정, 또는 경영권 리스크 노출 가능성 등을 분석하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 계약금액 변동: 해지 전 계약금액(ctr_prc_bfcc), 해지 후 계약금액(ctr_prc_atcc)
        - 계약기간: 해지 전 계약기간 시작일/종료일(ctr_pd_bfcc_bgd, ctr_pd_bfcc_edd)
        - 해지정보: 해지목적(cc_pp), 해지기관(cc_int), 해지예정일자(cc_prd)
        - 해지 후 재산처리 방법: 해지 후 신탁재산 반환방법(tp_rm_atcc)
        - 계약 전 자기주식 보유현황: 배당가능이익 범위 내 보유주식(aq_wtn_div_ostk, aq_wtn_div_estk) 및 비율(aq_wtn_div_ostk_rt, aq_wtn_div_estk_rt), 기타취득 주식(eaq_ostk, eaq_estk)
        - 주요 의사결정 이력: 이사회결의일자(bddd), 사외이사 참석 여부(od_a_at_t, od_a_at_b), 감사위원 참석 여부(adt_a_atn)

        【연계 분석 도구】
        - get_single_acc: 신탁계약 해지 전후 자본구조 및 부채비율 변동 분석
        - get_major_holder_changes: 해지 이후 주요 주주 지분율 변동 여부 모니터링
        - get_disclosure_list: 신탁 해지 이후 추가 자기주식 처분 또는 재신탁 여부 모니터링

        【활용 시나리오】
        - 해지목적(cc_pp)이 단순 만료인지, 전략 변경에 따른 조기 해지인지 구분하여 향후 주가 방어 정책 변화 예상
        - 해지 후 반환방법(tp_rm_atcc)이 현금 또는 실물(자사주)인지 분석하여 재무구조 또는 유동성에 미치는 영향 평가
        - 해지기관(cc_int)이 기존 계약체결기관과 동일한지 여부를 검토하여 계약 해지의 신뢰성 점검
        - 해지 이후 get_single_acc를 호출하여 자본총계, 부채비율 변동 여부 추적
        - 해지 이후 get_major_holder_changes를 통해 주요주주 지분 변동 리스크 모니터링

        【효과적 활용 방법】
        - 해지 전 계약금액(ctr_prc_bfcc)과 전체 자기자본 대비 비율 분석으로 해지의 재무적 영향성 예측
        - 해지예정일(cc_prd) 전후 주가 변동성 모니터링을 통해 시장 반응 조기 포착
        - 신탁재산 반환 방식(tp_rm_atcc)이 현금일 경우, 대규모 자금 유출 가능성 분석
        - 계약 종료 이후에도 get_disclosure_list를 통해 후속 자기주식 처분 계획 여부 지속 모니터링

        【주의사항 및 팁】
        - 단순 만기 해지라 하더라도 해지 이후 주주가치 제고 전략이 변경될 수 있으므로, 해지 목적(cc_pp) 및 반환방식(tp_rm_atcc) 세부 내용까지 면밀히 분석해야 함
        - 신탁재산 반환이 실물(자사주)로 이뤄질 경우, 이후 대규모 처분 리스크에 대비할 필요 있음
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""기업의 영업 양수 결정 공시 내역을 조회하는 도구입니다. 
        영업 양수는 기업 구조의 중대한 변화, 경영 전략의 전환, 또는 특수관계자와의 내부 거래 위험 등 
        다양한 기업 리스크를 내포할 수 있어 주요 리스크 탐지에 활용됩니다.

        【핵심 제공 데이터】
        - 양수 대상: 양수 영업(inh_bsn), 주요내용(inh_bsn_mc), 전부 양수 여부(absn_inh_atn)
        - 재무적 규모: 자산/매출/부채 기준 양수 부문의 규모 및 비중(ast_rt, sl_rt, dbt_rt)
        - 금전 정보: 양수가액(inh_prc), 양수대금 지급조건(inh_pym)
        - 일정 정보: 계약일(inh_prd_ctr_cnsd), 기준일(inh_prd_inh_std)
        - 거래상대방: 회사명(dlptn_cmpnm), 자본금(dlptn_cpt), 사업내용(dlptn_mbsn), 관계(dlptn_rl_cmpn)
        - 외부평가: 평가 여부(exevl_atn), 평가의견(exevl_op), 평가기관, 평가기간 등
        - 주주권리 영향: 주주총회 특별결의 여부(gmtsck_spd_atn), 주식매수청구권 관련 내용(aprskh_*)
        - 기타 이사회 의사결정 정보: 이사회결의일(bddd), 사외이사/감사 참석 여부(od_a_at_t, od_a_at_b, adt_a_atn)
        - 규제 정보: 우회상장 해당 여부(bdlst_atn), 공정위 신고 여부(ftc_stt_atn), 향후 제3자배정 증자 계획(n6m_tpai_plann)

        【연계 분석 도구】
        - get_single_acc: 양수 전후 자산, 매출, 부채 변화 정밀 분석
        - get_major_holder_changes: 거래 이후 주요 주주 지분 변동 여부 모니터링
        - get_disclosure_list: 연계 계약, 추가 이슈 등 병행 공시 추적

        【활용 시나리오】
        - 자산/매출/부채 비중(ast_rt, sl_rt, dbt_rt)을 통해 양수 부문의 기업 전체 기여도 및 리스크 집중 여부 분석
        - absn_inh_atn이 ‘예’인 경우, 영업 전체를 인수한 구조인지 확인하고, 기존 사업 포기 가능성까지 검토
        - 양수목적(inh_pp)과 양수영향(inh_af)을 통해 사업 전략의 전환 목적 여부 해석
        - 거래상대방이 계열사(dlptn_rl_cmpn)인 경우 내부자 거래 또는 자산 이전 의도 탐지
        - exevl_op이 '적정'이 아닌 경우, 거래가 객관적 가치와 괴리 가능성 여부 분석
        - 주식매수청구권 존재 시, 소액주주 권리보호 조치 여부 확인 및 주주갈등 리스크 탐지

        【효과적 활용 방법】
        - ast_rt, sl_rt, dbt_rt의 수치를 정량적으로 비교하여, 양수 대상이 핵심 사업인지, 부실 사업 인수인지 평가
        - 계약일 ~ 기준일 간의 일정 격차를 통해 거래 성사 리스크 및 이행 지연 가능성 분석
        - get_disclosure_list 병행 활용으로 해당 거래와 연계된 증자, 분할, 소송 등 추가 공시 동시 모니터링
        - 외부평가 기관(exevl_intn)의 신뢰도 및 평가근거(exevl_bs_rs) 확인으로 거래 공정성 재검토

        【주의사항 및 팁】
        - 양수 대상이 특정 자산군이 아니라 영업 전반일 경우, 조직 재편 또는 역합병 시도 가능성 검토 필요
        - 주식매수청구권 관련 조건(aprskh_lmt, aprskh_plnprc 등)은 실질 행사 가능성까지 분석
        - '향후 6월 이내 제3자배정 증자 계획'(n6m_tpai_plann)이 있는 경우, 이번 거래가 지배구조 개편 수단인지 교차검토 필요
        """,
    tags={"주요사항보고서", "영업양수", "결정"}
)
def get_business_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    영업양수 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020042
    """
    result = with_context(ctx, "get_business_acquisition", lambda context: context.ds005.get_business_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_business_transfer",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 영업양도 결정을 조회하는 도구입니다. 
        영업양도는 기업 전략의 급격한 전환, 특정 사업 부문의 철수, 또는 특수관계자와의 자산 이전 가능성을 내포할 수 있으므로, 
        경영 안정성과 지배구조 측면에서 주요 리스크 분석 대상으로 활용됩니다.

        【핵심 제공 데이터】
        - 양도 대상 사업: trf_bsn(양도영업), trf_bsn_mc(주요내용), 양도 목적(trf_pp)
        - 재무적 영향: ast_rt(자산 비중), sl_rt(매출 비중), trf_prc(양도가액)
        - 양도 영향 및 전략: trf_af(양도 이후 영향), 계약일 및 기준일(trf_prd_ctr_cnsd, trf_prd_trf_std)
        - 거래상대방 정보: dlptn_cmpnm, dlptn_cpt, dlptn_rl_cmpn(회사와의 관계 등)
        - 외부평가 내역: exevl_op(의견), exevl_intn(기관명), exevl_pd(기간)
        - 주주 영향 요소: gmtsck_spd_atn(주총 특별결의), aprskh_* (주식매수청구권 관련 항목)
        - 계약 구조 정보: trf_pym(대금 지급 방식), popt_ctr_cn(풋옵션 유무 및 계약내용)
        - 내부 의사결정: 이사회결의일(bddd), 사외이사/감사 참석여부(od_a_at_t, adt_a_atn)
        - 법적 신고 여부: 공정거래위원회 신고 대상 여부(ftc_stt_atn)

        【연계 분석 도구】
        - get_single_acc: 자산/매출 등 재무구조 변화 정밀 비교
        - get_major_holder_changes: 지분율 변화 여부를 통한 내부자 거래 리스크 탐지
        - get_disclosure_list: 병행 공시 여부 모니터링 (ex. 유상증자, 분할, 분쟁 등)

        【활용 시나리오】
        - sl_rt 또는 ast_rt 수치가 높은 경우, 핵심사업부 양도 여부 검토 필요
        - trf_pp, trf_af를 통해 매각 목적이 ‘사업철수’인지 ‘재무개선’인지 판별
        - 거래상대방(dlptn_rl_cmpn)이 계열사일 경우 내부자산이전 가능성 점검
        - 주주총회 특별결의 여부(gmtsck_spd_atn) 및 주식매수청구권 존재 시, 소액주주 보호 여부 확인
        - 외부평가 결과가 '적정'이 아닐 경우, 자산 저가매각 또는 사전합의 의혹 분석

        【효과적 활용 방법】
        - ast_rt, sl_rt 수치 분석으로 매각 사업이 전체 기업 재무에 미치는 영향 정량화
        - 계약일(trf_prd_ctr_cnsd)과 기준일(trf_prd_trf_std)의 간격을 확인해 거래이행 신뢰성 평가
        - trf_pym, popt_ctr_cn을 통해 대금지급의 실질성과 부채위험 여부 판단
        - exevl_op, exevl_bs_rs, exevl_pd를 통해 외부평가의 객관성 및 평가시점과의 괴리 분석

        【주의사항 및 팁】
        - 전체 영업양도(absn_inh_atn 값 '예')인 경우, 사실상 합병 또는 법인 청산 전단계 가능성 검토
        - 거래상대방이 외부기업이 아닌 경우, get_major_holder_changes 및 get_disclosure_list를 통해 후속 지분 변동 및 연계 공시 병행 확인 필요
        - 주식매수청구권 조건이 지나치게 제한적인 경우, 소액주주 보호제도의 실효성 의심 필요
        """,
    tags={"주요사항보고서", "영업양도", "결정"}
)
def get_business_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    영업양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020043
    """
    result = with_context(ctx, "get_business_transfer", lambda context: context.ds005.get_business_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_tangible_asset_acquisition",
    description="""기업의 유형자산 양수 결정 공시 내역을 조회하는 도구입니다. 
        대규모 유형자산의 양수는 자산 구조 변화, 재무 레버리지 확대, 특수관계자 거래 가능성 등
        기업의 재무 건전성과 지배구조에 직·간접 영향을 미치는 요소로, 해당 공시는 리스크 조기 탐지에 유효합니다.

        【핵심 제공 데이터】
        - 자산 정보: 자산구분(ast_sen), 자산명(ast_nm), 양수금액(inhdtl_inhprc), 자산총액(inhdtl_tast), 자산총액 대비 비중(inhdtl_tast_vs)
        - 양수 목적 및 영향: 양수 목적(inh_pp), 기대 효과(inh_af)
        - 일정 정보: 계약일(inh_prd_ctr_cnsd), 기준일(inh_prd_inh_std), 등기예정일(inh_prd_rgs_prd)
        - 거래상대방 정보: 회사명(dlptn_cmpnm), 자본금(dlptn_cpt), 주요사업(dlptn_mbsn), 주소(dlptn_hoadd), 관계(dlptn_rl_cmpn)
        - 계약조건: 거래대금 지급 방식(dl_pym), 풋옵션 여부(popt_ctr_atn), 계약내용(popt_ctr_cn)
        - 외부평가: 평가 여부(exevl_atn), 평가기관(exevl_intn), 평가기간(exevl_pd), 평가 의견(exevl_op)
        - 의사결정 이력: 이사회결의일(bddd), 사외이사 참석 여부(od_a_at_t, od_a_at_b), 감사 참석 여부(adt_a_atn)
        - 주주총회 및 매수청구권: 특별결의 여부(gmtsck_spd_atn), 매수청구권 조건 및 지급정보(aprskh_*)
        - 공정위 신고 대상 여부(ftc_stt_atn)

        【연계 분석 도구】
        - get_single_acc: 자산 양수 전후 자산 및 부채 구조 변화 추적
        - get_major_holder_changes: 지배구조 변동 탐지
        - get_disclosure_list: 동시기 계약/공시와의 연계 확인

        【활용 시나리오】
        - 자산총액 대비 비중(inhdtl_tast_vs)이 과도한 경우, 재무 구조 악화 또는 자금 조달 압박 가능성 검토
        - 양수 목적(inh_pp)과 기대효과(inh_af)를 통해 실질적 필요성 및 전략성과의 연계성 평가
        - 거래상대방과의 관계(dlptn_rl_cmpn)가 존재하면 특수관계자 리스크 또는 내부자 이익 가능성 확인
        - 외부평가 의견(exevl_op)이 '적정'이 아닐 경우, 평가 근거(exevl_bs_rs)를 통해 객관성 검증
        - 풋옵션 존재 시, 추후 손실 발생 가능성 및 계약 구조상 의도 파악
        - 주주총회 필요 여부(gmtsck_spd_atn) 및 매수청구권 조항(aprskh_*) 포함 시, 소액주주 권리와 갈등 요소 확인

        【효과적 활용 방법】
        - inhdtl_inhprc 금액과 get_single_acc의 총자산 대비 비율 계산을 통해 재무 레버리지 영향 추정
        - inh_prd_ctr_cnsd ~ inh_prd_rgs_prd 구간의 이행 지연 여부 판단으로 실행 리스크 분석
        - 거래상대방의 자본금(dlptn_cpt)과 사업내용(dlptn_mbsn) 분석으로 실질 거래처 적격성 검토
        - 외부평가 기관(exevl_intn)의 신뢰도와 과거 평가 이력 병행 분석
        - 추가 get_disclosure_list 호출로 계약 변경, 소송, 자산처분 등 연계 이슈 병행 모니터링

        【주의사항 및 팁】
        - 자산 양수가 '생산성 제고' 등 포괄적 표현일 경우, 실질 효과는 향후 공시 또는 실적(get_single_acc)과 연동 분석 필요
        - 풋옵션이 ‘아니오’라 하더라도 유사한 계약 조항이 있는지 계약내용(popt_ctr_cn) 상세 검토 필수
        - 양수 대상이 건물/토지인 경우, 이전 거래 이력 및 담보 제공 여부는 외부 자료와 병행 확인 필요
        """,
    tags={"주요사항보고서", "유형자산", "양수", "결정"}
)
def get_tangible_asset_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유형자산 양수 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020044
    """
    result = with_context(ctx, "get_tangible_asset_acquisition", lambda context: context.ds005.get_tangible_asset_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_tangible_asset_transfer",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 유형자산 양도 결정을 조회하는 도구입니다. 
        유형자산의 매각은 단순 자산 처분뿐 아니라 유동성 확보, 구조조정, 사업 철수 등 중대한 경영 판단의 신호일 수 있으므로, 
        기업의 재무안정성 및 장기 지속가능성 평가에 중요한 분석 지표로 활용됩니다.

        【핵심 제공 데이터】
        - 자산 내역: ast_sen(자산구분), ast_nm(자산명), trfdtl_trfprc(양도금액), trfdtl_tast_vs(총자산 대비 비중)
        - 전략 및 재무 목적: trf_pp(양도목적), trf_af(양도영향), sl_rt 또는 ast_rt 기반 비중
        - 거래 일정: 계약일(trf_prd_ctr_cnsd), 기준일(trf_prd_trf_std), 등기 예정일(trf_prd_rgs_prd)
        - 거래상대방: dlptn_cmpnm, dlptn_rl_cmpn(관계), dlptn_cpt(자본금), dlptn_mbsn(주요사업)
        - 거래 구조: dl_pym(대금지급 방식), popt_ctr_atn/popt_ctr_cn(풋옵션 여부 및 내용)
        - 외부평가 정보: exevl_op(평가의견), exevl_intn(기관명), exevl_pd(기간), exevl_bs_rs(평가 근거 및 사유)
        - 주주 영향: gmtsck_spd_atn(주주총회 특별결의 여부), aprskh_*(주식매수청구권 관련 항목)
        - 내부의사결정 정보: 이사회결의일(bddd), 사외이사/감사 참석 여부(od_a_at_t, adt_a_atn)
        - 규제 및 법적 정보: 공정거래위원회 신고대상 여부(ftc_stt_atn)

        【연계 분석 도구】
        - get_single_acc: 자산/부채 구조에서 해당 자산 비중 및 매각 이후 구조변화 추적
        - get_disclosure_list: 양도 이후 구조조정, 증자, 분할 등 연계 공시 추적
        - get_major_holder_changes: 대규모 자산 변동 이후 대주주 지분율 변화 모니터링

        【활용 시나리오】
        - 자산총액 대비 비중(trfdtl_tast_vs)이 20% 이상일 경우, 주요 사업부처의 매각 가능성 분석
        - trf_pp(양도 목적)에 '재무구조 개선', '현금 유동성 확보' 등이 명시된 경우, 단기 유동성 압박 의심
        - 거래상대방이 계열사인 경우(dlptn_rl_cmpn), 내부 자산이전 또는 지배구조 조정 가능성 점검
        - 외부평가 결과가 '적정'이 아닌 경우(exevl_op), 거래 공정성 및 자산 저가매각 의혹 확인
        - 주식매수청구권이 존재하거나 제한이 있는 경우, 소액주주 보호 여부 및 분쟁 가능성 검토

        【효과적 활용 방법】
        - trfdtl_tast_vs, trfdtl_trfprc 등 수치를 기반으로 자산총액 대비 영향 분석
        - 계약일~양도 기준일 간 차이 분석으로 거래 실행 지연/위험 가능성 평가
        - 외부평가 근거(exevl_bs_rs) 및 기관 신뢰도 검토로 평가 타당성 확보
        - get_disclosure_list 병행 활용으로 해당 자산 양도와 관련된 후속 공시 실시간 추적

        【주의사항 및 팁】
        - 자산명이 공장, 사옥 등일 경우, 해당 자산의 활용도 및 사업 영향까지 교차 분석 필요
        - 주주총회 특별결의 여부와 사외이사 출석률은 거래의 투명성과 합법성 판단에 중요한 지표
        - '풋옵션' 관련 계약이 포함된 경우, 장기적으로 추가 부채 리스크로 이어질 수 있으므로 병행 검토 필수
        """,
    tags={"주요사항보고서", "유형자산", "양도", "결정"}
)
def get_tangible_asset_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    유형자산 양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020045
    """
    result = with_context(ctx, "get_tangible_asset_transfer", lambda context: context.ds005.get_tangible_asset_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_other_corp_stock_acquisition",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 타법인 주식 양수 결정을 조회하는 도구입니다. 
        타법인 주식 취득은 단순 투자 외에도 지배구조 강화, 신사업 진출, 계열 재편, 우회상장 등 기업의 중대한 전략적 의사결정과 밀접히 연결되어 있으며, 
        자금 운용 리스크, 내부거래 의혹, 장기 부실화 가능성 등 다양한 리스크 신호를 탐지하는 데 활용됩니다.

        【핵심 제공 데이터】
        - 발행회사 정보: iscmp_cmpnm(회사명), iscmp_nt(국적), iscmp_rl_cmpn(회사와의 관계), iscmp_mbsn(주요사업)
        - 양수 내역: inhdtl_stkcnt(취득 주식 수), inhdtl_inhprc(양수금액), inhdtl_tast_vs(총자산 대비 비중), inhdtl_ecpt_vs(자기자본 대비 비중)
        - 양수 목적/일정: inh_pp(양수 목적), inh_prd(예정일자)
        - 거래상대방: dlptn_cmpnm, dlptn_rl_cmpn, dl_pym(지급 조건 및 방식)
        - 거래 영향: atinh_owstkcnt(양수 후 소유주식수), atinh_eqrt(지분율)
        - 외부평가 정보: exevl_op(평가 의견), exevl_intn(기관), exevl_pd(기간), exevl_bs_rs(근거 및 사유)
        - 지배구조 및 상장 관련 여부: bdlst_atn(우회상장 해당), iscmp_bdlst_sf_atn(발행회사의 우회상장 요건 충족 여부), n6m_tpai_plann(향후 제3자배정 증자 계획)
        - 옵션 계약 존재 여부: popt_ctr_atn(풋옵션 계약 체결 여부), popt_ctr_cn(계약내용)
        - 내부 의사결정 정보: bddd(이사회결의일), od_a_at_t/od_a_at_b(사외이사 참석), adt_a_atn(감사 참석)
        - 기타 규제 정보: ftc_stt_atn(공정위 신고 대상 여부)

        【연계 분석 도구】
        - get_major_holder_changes: 대주주 지분율 변화 여부 모니터링
        - get_disclosure_list: 유사 시점 타 공시와 병행 분석 (분할, 유상증자 등)
        - get_single_acc: 양수 전후 자기자본, 총자산 구조 분석

        【활용 시나리오】
        - inhdtl_tast_vs 또는 inhdtl_ecpt_vs가 10% 이상인 경우, 기업 자금 집행 리스크와 경영판단 정당성 여부 검토
        - iscmp_rl_cmpn이 '계열회사'로 명시된 경우, 내부거래 혹은 부실자산 전이 가능성 탐지
        - inh_pp에 ‘지배력 강화’, ‘글로벌 확장’ 등이 반복적으로 언급될 경우, 실질적 성과 없이 외형만 확대하는 전략인지 점검
        - popt_ctr_atn이 ‘예’인 경우, 향후 자금 유출 또는 상환 리스크(풋옵션 행사 조건 등) 발생 가능성 사전 탐지
        - 외부평가 의견이 부적정이거나, 기준금액과 괴리가 있는 경우(exevl_op), 자산 과대평가/거래 부당성 우려 분석

        【효과적 활용 방법】
        - 양수금액(A), 총자산(B), 자기자본(C)을 통해 비중계산: A/B, A/C 수치로 리스크 정량화
        - popt_ctr_cn 내용 분석으로 향후 추가 지분 취득/매각 조건 존재 여부 파악
        - get_disclosure_list로 동일 시점 타 공시(예: 증자, 분할, 사업확장 등)와의 연계 여부 확인
        - 이사회 및 사외이사 참석 여부를 통해 의사결정의 투명성과 절차적 정당성 확보

        【주의사항 및 팁】
        - 해당 도구는 '우회상장' 시도 가능성 분석에 특히 유용함: iscmp_bdlst_sf_atn, bdlst_atn 항목 병행 분석 필수
        - 외부평가가 ‘있음’이라도 평가기관의 신뢰도와 평가기간(exevl_pd)이 적절한지 검토 필요
        - 제3자배정 계획(n6m_tpai_plann)이 존재하는 경우, 지배주주 변경 혹은 내부 세력 유입 여부 주의 깊게 판단
        """,
    tags={"주요사항보고서", "타법인", "주식", "출자증권", "양수", "결정"}
)
def get_other_corp_stock_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    타법인 주식 및 출자증권 양수결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020046
    """
    result = with_context(ctx, "get_other_corp_stock_acquisition", lambda context: context.ds005.get_other_corp_stock_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_other_corp_stock_transfer",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 타법인 주식 양도 결정을 조회하는 도구입니다.  
        타법인 주식의 매각은 단순 자산 정리 외에도 지배력 포기, 자금 유동화, 사업 철수, 혹은 계열 정리와 같은 전략적 판단의 결과일 수 있으며,  
        기업의 장기 수익성, 내부거래 리스크, 또는 재무 건전성 측면에서 중요한 리스크 신호로 분석됩니다.

        【핵심 제공 데이터】
        - 발행회사 정보: iscmp_cmpnm(회사명), iscmp_nt(국적), iscmp_rl_cmpn(관계), iscmp_mbsn(주요사업)
        - 양도 내역: trfdtl_stkcnt(양도주식수), trfdtl_trfprc(양도금액), trfdtl_tast_vs(총자산 대비), trfdtl_ecpt_vs(자기자본 대비)
        - 양도 후 변화: attrf_owstkcnt(잔여 보유주식), attrf_eqrt(잔여 지분율)
        - 거래 상대방 정보: dlptn_cmpnm(회사명), dlptn_rl_cmpn(관계), dl_pym(지급 조건 및 방식)
        - 거래 목적 및 일정: trf_pp(양도 목적), trf_prd(예정일자)
        - 외부 평가: exevl_op(의견), exevl_intn(기관명), exevl_pd(기간), exevl_bs_rs(사유)
        - 이사회 결정: bddd(결정일), 사외이사/감사 참석 여부(od_a_at_t, adt_a_atn)
        - 규제 관련 정보: ftc_stt_atn(공정위 신고대상 여부), popt_ctr_atn/popt_ctr_cn(풋옵션 유무 및 계약내용)

        【연계 분석 도구】
        - get_major_holder_changes: 양도 이후 주요 주주 지분율 변화 추적
        - get_disclosure_list: 연계된 분할/증자/사업 철수 공시 병행 확인
        - get_single_acc: 양도금액이 기업 재무 구조에 미치는 영향 정량 분석

        【활용 시나리오】
        - trfdtl_tast_vs, trfdtl_ecpt_vs가 30% 이상일 경우, 기업 핵심 자산 정리 가능성 검토
        - 양도 목적(trf_pp)이 '재무구조 개선', '현금 확보' 등일 경우, 유동성 위기 징후 판단
        - iscmp_rl_cmpn이 '계열사'인 경우, 내부거래나 지배구조 조정 여부 분석
        - 외부평가 결과가 부적정(exevl_op) 또는 평가 방식이 비표준적일 경우, 거래 정당성 재검토
        - 잔여 지분(attrf_eqrt)이 0%에 수렴하는 경우, 경영권 포기 또는 사업 철수로 이어질 수 있음

        【효과적 활용 방법】
        - 양도금액(A), 총자산(B), 자기자본(C) 기준 비중 계산: A/B, A/C로 리스크 계량화
        - 외부평가 근거 및 기관 신뢰도 확인: exevl_bs_rs, exevl_intn 항목 분석
        - get_disclosure_list로 연계된 공시(분할, 증자 등)를 병행 확인하여 배경 분석
        - popt_ctr_cn이 존재할 경우, 향후 옵션 계약으로 인한 자산 또는 지분 재이동 가능성 검토

        【주의사항 및 팁】
        - 공시된 양도 목적이 포괄적일 경우(trf_pp), 실제 사유 파악을 위해 유사 시기 공시 병행 분석 필요
        - 계열사 간 거래는 외형상 정상 거래처럼 보이더라도 get_major_holder_changes와 교차 분석하여 통제구조 이상 여부 점검
        - 양도 후 보유 주식 수(attrf_owstkcnt)가 남아 있는 경우, 향후 풋옵션 행사 리스크 등 유보 전략인지 확인 필요
        """,
    tags={"주요사항보고서", "타법인", "주식", "출자증권", "양도", "결정"}
)
def get_other_corp_stock_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    타법인 주식 및 출자증권 양도결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020047
    """
    result = with_context(ctx, "get_other_corp_stock_transfer", lambda context: context.ds005.get_other_corp_stock_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_related_bond_acquisition",
    description="""
        상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 주식관련사채(전환사채·신주인수권부사채 등)의 양수 결정을 조회하는 도구입니다.  
        이러한 사채의 양수는 단순 채권 투자 외에도 향후 주식 전환을 통한 지분확보, 경영권 참여, 지배구조 변화 등을 초래할 수 있어  
        자금 집행의 건전성, 내부자와의 이해관계, 변동성 리스크 등 다각적 리스크 분석에 활용됩니다.

        【핵심 제공 데이터】
        - 사채 기본정보: stkrtbd_kndn(사채 종류), tm(회차), knd(구체적 조건)
        - 발행회사 정보: bdiscmp_cmpnm(회사명), bdiscmp_rl_cmpn(관계), bdiscmp_mbsn(주요사업), bdiscmp_cpt(자본금)
        - 양수 내역: inhdtl_bd_fta(사채 총액), inhdtl_inhprc(양수금액), inhdtl_tast_vs(총자산 대비), inhdtl_ecpt_vs(자기자본 대비)
        - 거래 조건 및 자금: dlptn_cmpnm(거래상대방), dlptn_rl_cmpn(관계), dl_pym(지급 조건 및 자금조달 방식)
        - 목적 및 일정: inh_pp(양수 목적), inh_prd(예정일자)
        - 외부평가 정보: exevl_op(의견), exevl_intn(기관), exevl_pd(기간), exevl_bs_rs(평가 사유)
        - 내부의사결정 정보: bddd(이사회 결의일), od_a_at_t/od_a_at_b(사외이사 출석), adt_a_atn(감사 참석 여부)
        - 기타 규제 사항: ftc_stt_atn(공정위 신고 여부), popt_ctr_atn/popt_ctr_cn(풋옵션 등 계약 체결 여부)

        【연계 분석 도구】
        - get_major_holder_changes: 향후 전환권 행사로 인한 지분율 변화 감지
        - get_disclosure_list: 동일 시점 전후로의 연계 공시 병행 추적 (예: 유상증자, 경영권 변경)
        - get_single_acc: 양수 이전/이후 자기자본, 자산 구조 비교

        【활용 시나리오】
        - inhdtl_tast_vs, inhdtl_ecpt_vs 수치가 높을 경우, 대규모 자금 투입에 따른 유동성 위기 가능성 검토
        - stkrtbd_kndn이 '전환사채'인 경우, 향후 주식 전환을 통한 지분율 변화 및 경영권 참여 가능성 분석
        - bdiscmp_rl_cmpn이 '계열사'일 경우, 내부거래 또는 부실 자산 구제 의심 가능성
        - exevl_op이 ‘적정’이 아닐 경우, 사채 평가액 대비 실제 양수가액 왜곡 가능성 존재
        - popt_ctr_cn에 풋옵션 조건이 포함될 경우, 향후 유동성 또는 손실 발생 가능성 사전 탐지

        【효과적 활용 방법】
        - 총자산/자기자본 대비 양수 비중(A/B, A/C) 수치를 통해 재무 영향 정량 평가
        - 사채권 종류(knd) 분석을 통해 전환권·상환권 여부, 만기 조건 등 리스크 평가
        - exevl_bs_rs와 평가기관 신뢰도를 기준으로 평가 타당성 검토
        - get_disclosure_list를 병행 활용해 동일 사채와 관련된 경영 전략 공시(인수, 합병 등) 여부 확인

        【주의사항 및 팁】
        - 전환사채나 신주인수권부사채의 경우, 행사 가능 기간과 전환가액 조건 등을 추가로 분석 필요
        - 동일 시점에 복수 사채 취득 또는 계열사 간 사채 교환이 발생하는 경우, 구조적 이해관계 확인 필수
        - 사채가 상환되지 않고 주식으로 전환될 경우, 실제 희석 효과나 경영권 분쟁 여부까지 고려해야 함
        """,
    tags={"주요사항보고서", "주권", "사채권", "양수", "결정"}
)
def get_stock_related_bond_acquisition(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주권 관련 사채권 양수 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020048
    """
    result = with_context(ctx, "get_stock_related_bond_acquisition", lambda context: context.ds005.get_stock_related_bond_acquisition(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_related_bond_transfer",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 주식 관련 사채(전환사채·신주인수권부사채 등)의 양도 결정을 조회하는 도구입니다.  
        해당 사채는 향후 주식 전환을 통해 지분율 및 지배구조에 직접적인 영향을 미칠 수 있는 유가증권으로, 이를 제3자에게 양도하는 경우  
        기업의 자금 전략, 내부자산 정리, 유동성 확보 목적 외에도 잠재적 리스크 신호로 해석될 수 있습니다.

        【핵심 제공 데이터】
        - 사채 정보: stkrtbd_kndn(사채권 종류), tm(회차), knd(세부 종류), aqd(기존 취득일)
        - 발행회사 정보: bdiscmp_cmpnm(회사명), bdiscmp_rl_cmpn(관계), bdiscmp_mbsn(주요사업), bdiscmp_cpt(자본금)
        - 양도 내역: trfdtl_bd_fta(권면 총액), trfdtl_trfprc(양도금액), trfdtl_tast_vs(총자산 대비), trfdtl_ecpt_vs(자기자본 대비)
        - 양도 목적 및 일정: trf_pp(양도 목적), trf_prd(양도 예정일자)
        - 거래상대방: dlptn_cmpnm(회사명), dlptn_rl_cmpn(관계), dl_pym(지급조건)
        - 외부평가: exevl_op(의견), exevl_intn(기관명), exevl_pd(평가기간), exevl_bs_rs(사유)
        - 내부 의사결정 정보: bddd(이사회결의일), od_a_at_t/od_a_at_b(사외이사 참석), adt_a_atn(감사 참석)
        - 기타 법적 항목: ftc_stt_atn(공정위 신고 대상), popt_ctr_atn/popt_ctr_cn(풋옵션 유무 및 조건)

        【연계 분석 도구】
        - get_single_acc: 사채 양도 이전/이후 자기자본 변화 분석
        - get_disclosure_list: 동시기 공시(예: 유상증자, 사업 양도)와의 연계 여부 점검
        - get_major_holder_changes: 양도 이후 대주주 지분율 변동 여부 추적

        【활용 시나리오】
        - trfdtl_ecpt_vs 또는 trfdtl_tast_vs가 10% 이상인 경우, 대규모 자금 유동화 목적 확인
        - trf_pp에 '신규 투자 재원 마련', '재무구조 개선' 등 명시 시, 자금 경색 가능성 진단
        - bdiscmp_rl_cmpn이 계열사인 경우, 내부거래 가능성 및 정상성 여부 검토
        - aqd와 trf_prd 간 간격이 짧은 경우, 단기 매매 또는 우회적 자금 조달 가능성 분석
        - 외부평가 의견이 부적정이거나 평가금액과 거래금액 간 괴리가 큰 경우, 자산가치 왜곡 리스크 탐지

        【효과적 활용 방법】
        - trfdtl_trfprc 대비 trfdtl_ecpt, trfdtl_tast 수치를 활용하여 재무 영향 정량 분석
        - exevl_pd(평가기간)과 거래일자 간 간극이 짧을 경우, 평가의 객관성 검토 필요
        - popt_ctr_cn 항목 분석을 통해 향후 지분 재취득 리스크 또는 유사 계약의 존재 확인
        - get_disclosure_list 병행 조회로 양도와 동시 발표된 전략 변화, 신규 사업 추진 여부 확인

        【주의사항 및 팁】
        - 전환권 행사 가능성이 남아있는 채권일 경우, 제3자가 이를 행사함으로써 주가·지분율에 영향 미칠 수 있음
        - 양도목적이 불분명하거나 외부평가 의견이 부실한 경우, 자산 매각 명분의 타당성을 의심할 필요 있음
        - 풋옵션 계약(popt_ctr_atn)이 '예'인 경우, 거래 이후 되사기 계약으로 유사 내부거래일 수 있음
        """,
    tags={"주요사항보고서", "주권", "사채권", "양도", "결정"}
)
def get_stock_related_bond_transfer(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주권 관련 사채권 양도 결정 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020049
    """
    result = with_context(ctx, "get_stock_related_bond_transfer", lambda context: context.ds005.get_stock_related_bond_transfer(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_merger",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 합병 결정에 대한 상세 내용을 조회하는 도구입니다. 
        합병 형태(흡수합병/신설합병), 합병비율, 외부평가 여부, 합병상대회사의 재무상태 등 다양한 정량적·정성적 정보를 바탕으로 기업의 지배구조 변화 가능성 및 재무 리스크를 평가할 수 있습니다.

        【핵심 제공 데이터】
        - 합병방식/형태/목적(mg_mth, mg_stn, mg_pp): 단순 구조조정인지, 경영권 확보 등 전략적 판단 요소 확인
        - 합병비율 및 산출근거(mg_rt, mg_rt_bs): 평가기관 기준시가 vs 자산가치 비교로 희석율/공정성 검토
        - 외부평가 정보(exevl_atn ~ exevl_op): 회계법인의 적정성 의견으로 합병 비율의 객관성 확인
        - 합병신주 발행 정보(mgnstk_ostk_cnt, mgnstk_cstk_cnt): 기존 주주 희석율 정량화 가능
        - 합병상대회사 정보(mgptncmp_cmpnm ~ rbsnfdtl_nic): 재무건전성 및 수익성 파악
        - 합병일정(mgsc_...): 주주확정일, 반대의사통지 기간, 합병기일 등 주요 절차 일정 파악
        - 우회상장 여부(bdlst_atn, otcpr_bdlst_sf_atn): 비상장회사와의 합병을 통한 상장 우회 가능성 탐지

        【연계 분석 도구】
        - get_single_acc: 합병 전후 자산, 부채, 자본 변동 분석
        - get_major_holder_changes: 합병 이후 주요 주주 지분율 변동 추적
        - get_disclosure_list: 합병 전후의 주요 공시 흐름 확인
        - get_executive_trading: 합병 직전 임원 주식거래 변화 감시

        【활용 시나리오】
        - 소규모 합병이라 하더라도 합병비율이 불공정할 경우 소액주주 피해 가능성 존재
        - 합병 상대회사의 당기순이익(rbsnfdtl_nic)이 마이너스일 경우 역합병이나 알박기 우려 판단
        - 외부평가 의견(exevl_op) 및 평가근거 분석을 통해 합병 가액 왜곡 가능성 점검
        - 신설합병 시 자산 및 부채 규모(ffdtl_*)를 기준으로 신설법인의 실질가치 추정
        - 일정 중 주주총회/반대의사 통지/주식매수청구권 행사가 누락될 경우, 절차상 하자 여부 검토

        【효과적 활용 방법】
        - 합병비율 산출기준이 기준시가인지 자산가치인지 구분하여 적정성 검토
        - 합병상대회사의 재무정보(rbsnfdtl_*)와 get_single_acc로 합병법인의 재무지표 비교
        - mgnstk_ostk_cnt를 기존 주식수와 비교하여 합병으로 인한 희석율 추산
        - 주주총회 및 주식매수청구권 행사기간 확인을 통해 주주보호 절차의 적절성 검증

        【주의사항 및 팁】
        - 분할합병인 경우 분할회사와의 관계 및 자산 이동 구조를 반드시 주석으로 확인
        - 외부평가의견이 '적정'이라 하더라도, 기준시가 vs 자산가치의 괴리를 수치로 비교하는 것이 중요
        - 우회상장 판정 여부가 '해당사항없음'이라도 거래소 심사에서 반려될 가능성은 별도로 판단 필요
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 분할 결정에 대한 상세 정보를 조회하는 도구입니다. 
        분할 방식(물적분할, 인적분할), 분할 대상 사업의 이전 내역, 분할 후 존속 및 신설법인의 재무 상태 등을 통해 기업의 사업구조 재편 및 지배구조 변화 가능성, 향후 리스크 요인을 분석할 수 있습니다.

        【핵심 제공 데이터】
        - 분할방식/형태/목적(dv_mth, dv_impef): 인적/물적, 단순 구조조정인지, 사업 독립 목적 등 판단
        - 분할비율(dv_rt): 존속/신설 법인 간 자산 및 지분 분할 기준
        - 이전 사업/재산 내역(dv_trfbsnprt_cn): 분할 대상 사업 부문과 권리·의무 이전 내용
        - 분할 후 존속회사 재무정보(atdvfdtl_*): 자산, 부채, 자본 상태 및 상장 유지 여부
        - 신설회사 정보(dvfcmp_cmpnm, ffdtl_*): 분할 설립 법인의 자산/부채 및 주요 사업
        - 감자 관련 항목(abcr_*): 신주배정, 거래정지, 감자비율 등 병행 감자 여부 확인
        - 주주총회 예정일, 채권자 이의 제출기간 등(gmtsck_prd, cdobprpd_*): 법적 절차 일정 확인
        - 이사회결의 정보(bddd, od_a_at_t, od_a_at_b, adt_a_atn): 내부 결정 절차의 정당성 확인
        - 풋옵션, 신고 여부(popt_ctr_atn, rs_sm_atn 등): 향후 계약 리스크 및 규제 요건 검토

        【연계 분석 도구】
        - get_single_acc: 분할 전후 재무구조 비교
        - get_major_holder_changes: 분할로 인한 주요 주주 지분율 변화 감시
        - get_disclosure_list: 분할 관련 후속 공시 흐름 파악
        - get_executive_trading: 분할 직전 임원 주식거래 여부 점검

        【활용 시나리오】
        - 물적분할 방식인 경우, 향후 신설법인 상장 시 기존 주주 지분 희석 가능성 평가
        - 이전 사업부문 분석을 통해 핵심 사업 회피 또는 리스크 이전 시도 여부 판단
        - 분할 후 신설회사 재무 건전성이 낮은 경우, 분할 목적의 합리성 재검토 필요
        - 감자 항목이 병행될 경우, get_disclosure_list 병행 조회로 자본 구조 변동 흐름 모니터링
        - 채권자 이의제출기간 분석을 통해 우발채무 전가 여부 사전 탐지

        【효과적 활용 방법】
        - atdvfdtl_teqt와 ffdtl_teqt를 비교하여 재무 리스크의 이동 방향 분석
        - dvfcmp_rlst_atn이 ‘예’일 경우, 상장 우회 가능성 및 분할 취지 재검토
        - 분할 이전 권리·의무가 어느 법인에 귀속되는지 dv_trfbsnprt_cn 상세 검토
        - 분할기일(dvdt)과 등기예정일(dvrgsprd)을 기준으로 후속 공시 일정 사전 예측
        - get_major_holder_changes로 분할 이후 지배구조 이탈 조짐 사전 감지

        【주의사항 및 팁】
        - 물적분할 시 대주주 지분율 유지 여부와 소액주주 보호 조치를 반드시 함께 검토
        - 분할목적이 불분명하거나 이전 사업부문이 핵심일 경우, 사실상 알박기 가능성 존재
        - 계약·소송·지식재산권의 귀속처리 방식이 불명확할 경우 법적 분쟁 소지 있음
        - 공정위 신고 대상 여부(ftc_stt_atn)와 popt_ctr_atn(풋옵션 존재 여부)는 거래 안정성에 직접적 영향
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, **분할합병 결정**에 관한 상세 내역을 조회하는 도구입니다.  
        분할합병은 특정 사업 부문을 분할한 후 이를 다른 회사와 합병하는 복합 구조로, 해당 절차를 통해 **사업 재편**, **지배구조 개편**, **재무구조 변화**가 동시에 발생할 수 있습니다.  
        분할사업부문, 합병비율, 외부평가 결과, 합병상대회사의 재무 상태 등 다양한 정량적·정성적 데이터를 바탕으로 리스크 탐지가 가능합니다.

        【핵심 제공 데이터】
        - 분할합병 방식 및 목적(dvmg_mth, dvmg_impef): 물적분할 + 흡수합병 등 복합 구조 파악
        - 분할 이전 내역(dv_trfbsnprt_cn): 이전되는 사업부문 및 자산·권리의 귀속 상세
        - 합병상대회사 정보(mgptncmp_*): 주요사업, 재무지표, 관계사 여부 등 위험요인 판단
        - 합병비율 및 평가(dvmg_rt, dvmg_rt_bs, exevl_*): 희석율 및 외부평가 적정성 확인
        - 분할 후 존속회사 및 신설회사 정보(atdv_*, dvfcmp_*): 분할 이후 재무 안정성 및 사업 집중도 분석
        - 분할합병 일정(dvmgsc_*): 주총, 주주확정일, 반대의사통지기간, 등기 예정일 등
        - 주식매수청구권 관련(aprskh_*): 행사 조건, 기간, 매수가격 등 주주 보호 절차 확인
        - 감자 및 풋옵션 정보(abcr_*, popt_ctr_*): 자본 감소 및 거래 안정성 관련 변수

        【연계 분석 도구】
        - get_single_acc: 분할합병 전후 자산, 부채, 자본 구조 변화 분석
        - get_major_holder_changes: 지분율 및 지배구조 변경 여부 추적
        - get_disclosure_list: 분할합병과 동시 발표된 주요 공시 흐름 확인
        - get_executive_trading: 분할합병 직전 임원 주식 매매 여부 감시

        【활용 시나리오】
        - 분할사업부문이 핵심 수익원이었는지 dv_trfbsnprt_cn과 atdv_excmp_exbsn_rsl로 분석
        - 합병상대회사의 적정성 평가 결과가 '부적정' 또는 미흡할 경우, 공정성 논란 소지
        - 포괄적 사업이전 후 합병비율이 불합리할 경우, 소액주주 피해 가능성 판단
        - 신설회사 상장 여부(dvfcmp_atdv_lstmn_at, nmgcmp_rlst_atn)가 '예'인 경우 우회상장 가능성 점검
        - 주식매수청구권 관련 조항에서 행사 조건 제한이 명시되었는지 여부 분석

        【효과적 활용 방법】
        - dvmg_rt와 기존 발행주식수 대비 희석율 계산
        - 합병상대회사의 재무지표(rbsnfdtl_*)를 기준으로 합병 가치의 정당성 검토
        - 분할합병 일정과 aprskh_ex_pc_mth_pd_pl 등을 활용하여 투자자 권리 행사 기간 확보 여부 검토
        - get_single_acc 또는 get_disclosure_list 병행 조회로 후속 분할/흡수/감자 여부 추가 탐색
        - get_major_holder_changes를 통해 경영권 변동 가능성 사전 진단

        【주의사항 및 팁】
        - '현금 대가' 방식의 분할합병은 지분 희석은 없지만, 비상장 자산의 공정가치 왜곡 우려 있음
        - 외부평가의견이 포스코 사례처럼 '간접 인용'일 경우, 평가기관 직접 검토 필요
        - 분할합병 대상 자산의 귀속처와 사후 법적 분쟁 가능성(dv_trfbsnprt_cn)을 면밀히 검토
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

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
    description="""상장법인 또는 주요 비상장법인이 제출한 주요사항보고서 중, **주식의 포괄적 교환 또는 이전 결정**에 대한 상세 정보를 조회하는 도구입니다.  
        주식교환은 지배구조 개편, 완전자회사 편입, 또는 사업 통합 등의 전략적 수단으로 활용되며, 주식 가치 평가, 합리성 검토, 주주 권리 보장 여부 등을 다각도로 분석할 수 있습니다.

        【핵심 제공 데이터】
        - 교환·이전 구조 및 대상 정보(extr_sen, extr_stn, extr_tgcmp_*): 대상 법인 정보, 관계, 발행 주식 수 등
        - 교환 비율 및 근거(extr_rt, extr_rt_bs): 기준 주가, 본질가치 등 산출방식과 비율의 정당성
        - 대상 법인의 재무 요약(rbsnfdtl_*): 최근 사업연도 자산, 부채, 자본금, 자본총계 등
        - 외부평가(exevl_*): 평가기관, 평가의견, 평가기간, 평가 근거
        - 교환 목적 및 일정(extr_pp, extrsc_*): 지배력 확보, 시너지 효과, 상장일자 등 포함
        - 주식매수청구권(aprskh_*): 행사 조건, 기간, 가격, 계약상 효력
        - 기타 판단 요소: 우회상장 여부(bdlst_atn), 풋옵션 존재(popt_ctr_atn), 증권신고서 제출 여부(rs_sm_atn)

        【연계 분석 도구】
        - get_single_acc: 교환 전후 자기자본 또는 총자산의 변화 확인
        - get_major_holder_changes: 완전 자회사화 이후 지배구조 변화 추적
        - get_disclosure_list: 동일 시기의 다른 공시(예: 유상증자, 투자 계약 등) 탐색
        - get_foreign_listing_decision: 향후 상장 계획 및 해외 진출 여부 파악

        【활용 시나리오】
        - extr_rt와 extr_rt_bs의 괴리가 클 경우, 합병/교환 비율 조정의 정당성 검토 필요
        - extr_tgcmp_rl_cmpn이 계열사이며 교환비율이 현저히 불균형할 경우, 소액주주 피해 여부 점검
        - 외부평가(exevl_op)가 부적정이거나 생략된 경우, 평가 공정성 의문 제기
        - extr_pp에 명시된 교환 목적이 지배력 강화, 가치 제고라면 사후 성과와 비교 필요
        - extrsc_extrdt ~ extrsc_nstklstprd 사이의 일정이 비정상적으로 짧을 경우, 절차상 리스크 존재 가능성

        【효과적 활용 방법】
        - 외부평가 결과의 기준가 대비 할인/할증 적용 여부 분석
        - 교환 대상 법인의 최근 재무제표(rbsnfdtl_*)를 통해 잠재 리스크 사전 점검
        - get_disclosure_list와 병행 조회하여 자회사 관련 신규 투자, 자산 이전 등과의 연계성 분석
        - aprskh_ctref에 명시된 ‘계약 효력’ 조건에 따라 주주 권리 제한 여부 확인

        【주의사항 및 팁】
        - 완전자회사화 이후 비상장 법인의 회계 불투명성 우려 존재
        - 교환비율 산정의 공정성은 시장평가 및 회계기준에 따라 판단해야 함
        - 우회상장 목적이 의심되는 경우, bdlst_atn 및 otcpr_bdlst_sf_atn 항목 반드시 확인
        """,
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
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020053
    """
    result = with_context(ctx, "get_stock_exchange", lambda context: context.ds005.get_stock_exchange(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

