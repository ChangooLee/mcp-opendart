import logging
from typing import Any, Optional
from mcp_opendart.server import mcp
from mcp.types import TextContent
from mcp_opendart.utils.ctx_helper import with_context

logger = logging.getLogger("mcp-opendart")

@mcp.tool(
    name="get_equity",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 신주 발행 및 주식매출에 관한 상세 내역을 조회하는 도구입니다.  
        기업의 자본 확충 계획, 실제 신주발행 규모, 인수인 현황, 자금 사용 목적 등을 종합 분석하여, 지배구조 변동 리스크, 자금 운용 위험, 투자자 보호 이슈를 평가하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 청약 및 납입 정보(sbd, pymd, sband, asand, asstd): 신주 청약, 납입, 배정 일정 파악
        - 신주인수권 사항(exstk, exprc, expd): 행사 가능 주식 종류, 행사 가격 및 행사 기간
        - 모집/매출 증권 정보(stksen, stkcnt, fv, slprc, slta, slmthn): 증권 종류별 발행수량, 액면가, 모집가액, 총액 및 방식
        - 인수인 정보(actsen, actnmn, stksen, udtcnt, udtamt, udtprc, udtmth): 인수 주체별 인수수량, 금액, 인수방법
        - 자금사용 목적(se, amt): 조달자금의 세부 사용처 및 금액
        - 매출인 관련 사항(hdr, rl_cmp, bfsl_hdstk, slstk, atsl_hdstk): 기존 보유자의 증권 매출 내역 및 잔여 보유 주식 수
        - 일반청약자 환매청구권(grtrs, exavivr, grtcnt, expd, exprc): 환매청구권 부여 여부 및 조건

        【연계 분석 도구】
        - get_paid_in_capital_increase: 유상증자 내역과 교차 분석하여 자본 확충 경로 비교
        - get_stock_total: 신주발행 이후 주식총수 변동 확인
        - get_major_holder_changes: 증자/매출 이후 주요 주주 지분율 변동 여부 분석
        - get_disclosure_list: 증자 관련 추가 공시(조건변경, 실패, 철회 등) 병행 확인

        【활용 시나리오】
        - 신주인수권 행사 조건 분석을 통해 투자자 권익 보호 수준 평가
        - 인수 주체별 인수비율 및 방식 파악 → 특정 세력에 의한 지분 집중 가능성 탐지
        - 자금 사용 계획 대비 실제 자산투자, 차입금 상환 여부 추적
        - 환매청구권(grtrs) 부여 여부를 통해 투자자 보호 장치 존재 여부 점검
        - 기존 주주 지분 희석률 계산 및 경영권 방어 가능성 분석

        【효과적 활용 방법】
        - 모집/매출 총액(slta)과 자본금 증감 내역을 비교하여 자본구조 영향 정밀 평가
        - 인수방법(udtmth) 분석을 통해 제3자배정, 일반공모, 주주배정 방식별 리스크 분류
        - 자금사용 목적(se, amt) 세부 항목별로 자산투자 대비 운영자금 비중 분석
        - 신주발행 공고일(sband) 이후 주요사항보고서 변경 여부를 get_disclosure_list로 병행 검토

        【주의사항 및 팁】
        - 일부 항목(예: 환매청구권 부여 여부)은 선택적 기재사항으로, "-" 표시된 경우 별도 확인 필요
        - 행사기간(expd) 및 행사가격(exprc)은 향후 자본 희석 가능성에 미치는 영향까지 고려하여 분석
        - 매출증권 수(slstk)가 크고 보유잔여증권수(atsl_hdstk)가 급감하는 경우, 경영권 이탈 가능성 주의
        """,
    tags={"지분증권", "증권신고서", "지분증권", "증권신고서"}
)
def get_equity(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    지분증권 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020054
    """
    result = with_context(ctx, "get_equity", lambda context: context.ds006.get_equity(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_debt",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 채무증권(회사채 등) 발행 및 매출에 관한 상세 내역을 조회하는 도구입니다.  
        채무증권 발행 조건, 인수인 구성, 담보 및 보증 여부, 자금 사용 목적 등을 종합 분석하여, 부채 리스크, 차환 위험, 재무 건전성 변동 가능성을 진단하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 채무증권 기본정보(bdnmn, slmth, fta, slta, isprc, intr, isrr, rpd): 발행 명칭, 모집방법, 발행액, 이자율, 수익률, 상환일자
        - 관리 및 대행기관(print_pymint, mngt_cmp): 원리금지급대행기관 및 사채관리회사
        - 신용등급(cdrt_int): 외부 신용평가기관 평가 결과
        - 발행 및 납입 일정(sbd, pymd, sband, asand, asstd): 청약, 납입, 공고, 배정일정
        - 표시통화/사용지역(dpcrn, usarn, usntn): 외화채 발행 여부 및 사용국가
        - 보증 및 담보 정보(grt_int, grt_amt, icmg_mgknd, icmg_mgamt): 보증기관 및 담보 제공 여부
        - 지분증권 연계정보(estk_exstk, estk_exrt, estk_exprc, estk_expd): 전환사채, 신주인수권부사채 등 연계 조건
        - 파생결합사채 여부(drcb_at, drcb_uast, drcb_optknd, drcb_mtd): ELS·DLS 연계 구조 여부
        - 인수인 정보(actsen, actnmn, udtcnt, udtamt, udtprc, udtmth): 인수 주체별 인수조건
        - 자금 사용 목적(se, amt): 모집자금의 세부 활용 계획
        - 매출인 관련 사항(hdr, rl_cmp, bfsl_hdstk, slstk, atsl_hdstk): 기존 보유자의 매출 주식 수량 및 관계 정보

        【연계 분석 도구】
        - get_debt_securities_issued: 사업/분기보고서상 채무증권 잔액과 발행정보 비교
        - get_single_acc: 총부채 대비 채무증권 발행비율 확인
        - get_creditor_management: 과도한 부채로 인한 채권단 관리 가능성 분석
        - get_disclosure_list: 발행조건 변경, 조기상환, 리파이낸싱 공시 병행 모니터링

        【활용 시나리오】
        - 이자율(intr) 및 발행수익률(isrr) 분석을 통한 자금조달 비용 및 리스크 평가
        - 담보 제공(icmg_mgknd) 및 보증(grt_int) 여부를 통해 부도 리스크 완화 여부 판단
        - 표시통화(dpcrn)이 외화인 경우 환율 변동에 따른 상환 부담 증가 가능성 분석
        - 파생결합사채 여부(drcb_at)가 'Y'인 경우, 고위험 채권 발행 여부 사전 경고
        - 자금 사용 목적(se, amt) 세부 항목 분석을 통해 영업목적 외 차입 리스크 탐지

        【효과적 활용 방법】
        - 신용등급(cdrt_int)과 이자율(intr)을 비교하여 시장 평가 대비 과도한 차입비용 여부 진단
        - slmth(모집방법) 분석을 통해 사모 발행 시 투자자 정보 비대칭성 리스크 점검
        - 담보금액(icmg_mgamt) 대비 발행총액(slta) 비율을 산출해 담보커버리지 평가
        - estk_exstk(지분연계) 항목 존재 시 주식 희석 가능성 및 조기 전환 리스크 병행 검토
        - 파생결합사채(drcb_at)가 존재하는 경우 기초자산(drcb_uast) 위험성 평가 필요

        【주의사항 및 팁】
        - 신용등급이 부여되지 않은 경우(cdrt_int 미기재), 외부 투자자 유치 어려움 또는 리스크 높은 자금조달 가능성 있음
        - 발행가액(isprc)과 발행수익률(isrr) 간 괴리율이 크다면, 시장 신뢰도 저하 가능성 있음
        - 외화채는 원화 교환 예정(wnexpl_at) 여부를 반드시 확인하여 환율리스크 고려
        - drcb_uast(기초자산)가 변동성이 높은 경우, 만기 도래 시 조기상환 리스크 커질 수 있음
        """,
    tags={"채무증권", "증권신고서", "채무증권", "증권신고서"}
)
def get_debt(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    채무증권 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020055
    """
    result = with_context(ctx, "get_debt", lambda context: context.ds006.get_debt(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_depository_receipt",
    description="""상장법인 및 주요 비상장법인이 제출한 증권신고서 중, 증권예탁증권(DR: Depositary Receipt) 발행 내역을 조회하는 도구입니다.  
        예탁기관을 통한 간접투자 구조를 통해 외화 조달, 해외투자자 유치, 유동성 확보 등의 목적이 숨겨져 있을 수 있으며, 발행조건을 분석함으로써 기업의 자금조달 전략 및 글로벌 진출 리스크를 평가할 수 있습니다.

        【핵심 제공 데이터】
        - 예탁증권 종류(drt_pd_knd): GDR, ADR, EDR 등 발행 유형
        - 발행 수량(drt_isu_cnt): 총 발행 예정 수량
        - 발행가액(drt_isu_prc): 발행 예정 단가
        - 외화표시 여부(fxcrncy_yn): 외화 표시 여부 (환율 리스크 가능성 평가)
        - 발행 목적(drt_isu_pp): 자금조달 목적 구체적 명시(설비투자, 차입금 상환 등)
        - 발행시장(drt_lstplc): 상장 예정 해외시장
        - 주관사 정보(drt_undwt_cmpnm): 발행 주관기관(IB)의 신뢰도 평가 가능

        【연계 분석 도구】
        - get_single_acc: 외화 조달 이후 자산·부채 변동 분석
        - get_disclosure_list: DR 발행과 관련된 추가 공시(예: 신규 투자, 설비 확장 등) 확인
        - get_major_holder_changes: DR 발행 후 주요 주주 지분율 변동 여부 추적

        【활용 시나리오】
        - drt_isu_cnt 대비 기존 총주식수 대비 비율을 계산하여 희석 가능성 정량 분석
        - 외화표시(fxcrncy_yn)가 'Y'인 경우, 환율 변동성 리스크(외화 부채 증가 가능성) 사전 파악
        - 발행목적(drt_isu_pp)이 차입금 상환일 경우, 단기 유동성 위기 가능성 평가
        - 주관사 신뢰도(drt_undwt_cmpnm)를 통해 발행 성공 가능성과 조건의 공정성 분석
        - 발행시장(drt_lstplc)이 제한적인 경우, 실제 유동성 확보 가능성 낮을 수 있음

        【효과적 활용 방법】
        - 외화표시 여부를 분석하여 향후 환율 변동에 따른 손익 영향 추정
        - 발행수량과 발행가격을 기준으로 총 발행 금액 산출 후, 기존 자기자본 대비 비율 검토
        - DR 발행 직후 get_disclosure_list로 자금 사용 계획의 변동 여부 및 추가 이벤트 모니터링
        - get_single_acc로 DR 발행 이후 자본구조 개선 여부를 수치로 검증

        【주의사항 및 팁】
        - 발행시장(drt_lstplc)이 비주류 거래소인 경우 실제 매매 활성도가 낮아 유동성 확보에 실패할 가능성 존재
        - 외화표시 발행임에도 환헤지 계획이 없는 경우, 환차손 리스크로 이어질 수 있음
        - 발행 목적이 구체적이지 않거나 모호한 경우, 자금 사용처 불투명성에 주의 필요
        """,
    tags={"증권예탁증권", "증권신고서", "증권예탁증권", "증권신고서"}
)
def get_depository_receipt(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    증권예탁증권 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020056
    """
    result = with_context(ctx, "get_depository_receipt", lambda context: context.ds006.get_depository_receipt(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_merger_report",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 합병(또는 분할합병) 관련 상세 내역을 조회하는 도구입니다.  
        합병 구조, 주식매수청구권 조건, 합병비율, 당사회사의 재무 상태 등을 분석하여, 경영권 변동 리스크, 합병 무효 가능성, 주주가치 훼손 가능성 등을 종합 평가하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 기본 합병 정보(stn, bddd, ctrd, gmtsck_shddstd, ap_gmtsck): 합병 형태, 이사회 결의일, 계약일, 주주총회 관련 일정
        - 주식매수청구권(aprskh_pd_bgd, aprskh_pd_edd, aprskh_prc): 행사 기간, 행사 가격 등 주주 보호 장치
        - 합병기일 및 지급조건(mgdt_etc, grtmn_etc): 합병 완료 시점 및 교부금 등 지급 조건
        - 합병비율 및 외부평가(rt_vl, exevl_int): 합병가액 비율 및 외부평가기관 평가 여부
        - 발행 예정 증권정보(kndn, cnt, fv, slprc, slta): 합병에 따라 신규 발행될 주식 종류, 수량, 액면가, 모집가액
        - 당사회사 정보(cmpnm, sen, tast, cpt, isstk_knd, isstk_cnt): 합병당사자별 총자산, 자본금, 발행주식 내역
        - 주요사항보고서 연결정보(rpt_rcpn): 관련 공시 문서 추적 가능

        【연계 분석 도구】
        - get_division_merger: 분할합병 구조와 교차 분석하여 사업구조 재편 리스크 탐지
        - get_stock_total: 합병 이후 주식총수 변동 확인
        - get_major_holder_changes: 합병 이후 주요주주 지분율 변화 분석
        - get_executive_info: 합병 이후 경영진 변동성 점검
        - get_disclosure_list: 합병 실패, 조건 변경 등 추가 공시 모니터링

        【활용 시나리오】
        - 합병비율(rt_vl) 분석을 통해 소액주주 권익 훼손 여부 평가
        - 외부평가기관(exevl_int) 유무를 통해 합병 절차의 공정성 검증
        - 주식매수청구권 행사 가격(aprskh_prc)과 시장가격 비교로 주주 이익 보호 수준 판단
        - 합병 당사회사의 총자산(tast), 자본금(cpt) 비교를 통한 합병 전후 재무 건전성 분석
        - 신규 발행 주식 수(cnt) 및 모집가(slprc) 분석으로 주식가치 희석 가능성 추정

        【효과적 활용 방법】
        - 주식매수청구권 행사 기간(aprskh_pd_bgd~aprskh_pd_edd) 설정이 비정상적으로 짧거나 불리할 경우 리스크 조기 경고
        - 발행 예정 주식수(cnt) 대비 기존 발행주식수(isstk_cnt) 비율 분석으로 기존 주주 희석률 정량 평가
        - tast(총자산), cpt(자본금) 수치로 합병 후 대차대조표 영향 예측
        - get_disclosure_list 연계로 합병 계약 변경, 합병 무산 등 리스크 신호 모니터링

        【주의사항 및 팁】
        - 합병비율(rt_vl)이 극단적으로 왜곡되어 있거나 외부평가기관(exevl_int) 평가가 생략된 경우, 주주가치 훼손 위험이 크므로 특별히 주의
        - 주식매수청구권 행사 가격(aprskh_prc)이 시가보다 현저히 낮은 경우 주주 이탈 가능성 존재
        - tast 및 cpt 값이 '-'로 표시된 경우, 일부 당사회사가 소규모 법인일 가능성이 있으므로 합병 동기 추가 분석 필요
        """,
    tags={"합병", "증권신고서", "합병", "증권신고서"}
)
def get_merger_report(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    합병 증권신고서 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020057
    """
    result = with_context(ctx, "get_merger_report", lambda context: context.ds006.get_merger_report(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_stock_exchange_report",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 주식교환 또는 주식이전(합병 없이 지배구조 변경)과 관련된 상세 내역을 조회하는 도구입니다.  
        주식교환/이전의 구조, 주식매수청구권 조건, 비율 설정, 당사회사의 재무 상태 등을 분석하여, 지배구조 재편 리스크, 소수주주 보호 이슈, 자본구조 변동 가능성을 평가하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 기본 거래 정보(stn, bddd, ctrd, gmtsck_shddstd, ap_gmtsck): 주식교환/이전 형태, 이사회 결의일, 계약일, 주주총회 일정
        - 주식매수청구권(aprskh_pd_bgd, aprskh_pd_edd, aprskh_prc): 행사기간, 행사가격 설정을 통한 소수주주 보호 여부
        - 교환/이전 비율 및 조건(rt_vl, mgdt_etc, grtmn_etc): 주식교환 또는 지급 교부금 조건
        - 외부평가 여부(exevl_int): 거래 공정성 확보를 위한 제3자 평가기관 참여 여부
        - 발행 증권 정보(kndn, cnt, fv, slprc, slta): 주식교환/이전 완료 후 발행될 증권의 종류 및 수량
        - 당사회사 재무정보(cmpnm, sen, tast, cpt, isstk_knd, isstk_cnt): 거래 참여 회사별 총자산, 자본금, 발행주식수 현황
        - 주요사항보고서 접수번호(rpt_rcpn): 관련 공시 문서 추적 가능

        【연계 분석 도구】
        - get_division_merger: 분할합병 등 타 형태의 지배구조 재편 사례와 비교 분석
        - get_major_holder_changes: 주식교환/이전 후 주요 주주 지분율 변동 여부 분석
        - get_stock_total: 주식교환/이전 이후 총발행주식수 변동 확인
        - get_disclosure_list: 거래 변경, 철회, 소송 리스크 등 추가 공시 병행 모니터링

        【활용 시나리오】
        - 주식매수청구권 행사 가격(aprskh_prc)과 시가 비교로 주주 보호 수준 평가
        - 교환/이전 비율(rt_vl)이 과도하게 왜곡된 경우, 지배구조 불안정성 리스크 탐지
        - 외부평가기관(exevl_int) 유무를 통해 거래 공정성 확보 여부 검증
        - tast(총자산), cpt(자본금) 수치를 통해 거래 전후 재무구조 변화 예측
        - 발행 예정 주식수(cnt) 증가가 기존 주주 희석 또는 지배력 변동 가능성에 미치는 영향 평가

        【효과적 활용 방법】
        - 주주총회 승인 일정(ap_gmtsck)과 매수청구권 행사기간(aprskh_pd_bgd~aprskh_pd_edd) 비교 분석으로 주주 행동 여력 평가
        - 신규 발행주식수(cnt) 대비 기존 발행주식수(isstk_cnt) 비율 계산으로 희석율 정량 평가
        - get_major_holder_changes 호출하여 지배주주 지분율 변동 추적
        - 거래 대상 회사 간 tast, cpt 비교로 상대적 재무건전성 평가

        【주의사항 및 팁】
        - 주식교환 또는 주식이전은 "합병"과 다르게 법인 소멸 없이 지배구조 변경만 일어날 수 있으므로, 거래 목적 및 구조를 명확히 구분해야 합니다.
        - 외부평가 미실시 또는 평가보고서 부실 기재(exevl_int 부재)는 향후 주주소송 리스크를 높일 수 있음
        - 지급 교부금(grtmn_etc)이 설정된 경우, 소수주주 이탈 가능성 및 추가 비용 부담 리스크 고려
        """,
    tags={"주식의포괄적교환·이전", "증권신고서", "주식의포괄적교환·이전", "증권신고서"}
)
def get_stock_exchange_report(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    주식의포괄적교환·이전 증권신고서 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020058
    """
    result = with_context(ctx, "get_stock_exchange_report", lambda context: context.ds006.get_stock_exchange_report(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))

@mcp.tool(
    name="get_division_report",
    description="""상장법인 및 주요 비상장법인이 제출한 주요사항보고서 중, 회사 분할(신설분할, 인적분할, 물적분할 등) 관련 상세 내역을 조회하는 도구입니다.  
        분할 구조, 주식매수청구권 조건, 분할 비율, 당사회사의 재무 상태 등을 분석하여, 경영구조 변화 리스크, 주주가치 훼손 가능성, 신설법인 리스크 등을 종합 평가하는 데 활용할 수 있습니다.

        【핵심 제공 데이터】
        - 기본 분할 정보(stn, bddd, ctrd, gmtsck_shddstd, ap_gmtsck): 분할 형태, 이사회 결의일, 계약일, 주주총회 관련 일정
        - 주식매수청구권 조건(aprskh_pd_bgd, aprskh_pd_edd, aprskh_prc): 행사 기간 및 행사 가격, 소수주주 보호 여부
        - 분할 기일 및 지급조건(mgdt_etc, grtmn_etc): 분할 완료 시점 및 교부금 지급 조건
        - 분할 비율(rt_vl) 및 외부평가 여부(exevl_int): 분할가액 비율 및 공정성 확보 여부
        - 발행 예정 증권 정보(kndn, cnt, fv, slprc, slta): 분할 완료 후 발행될 주식 종류, 수량, 액면가, 모집가액
        - 당사회사 재무정보(cmpnm, sen, tast, cpt, isstk_knd, isstk_cnt): 분할 참여 회사별 총자산, 자본금, 발행주식 내역
        - 주요사항보고서 접수번호(rpt_rcpn): 관련 공시 문서 추적 가능

        【연계 분석 도구】
        - get_division_merger: 분할합병 구조와 비교하여 사업 구조 재편 리스크 심층 분석
        - get_major_holder_changes: 분할 이후 주요주주 지분율 변화 분석
        - get_stock_total: 분할 이후 총발행주식수 변동 확인
        - get_disclosure_list: 분할 계약 변경, 분할 무산 등 추가 공시 병행 모니터링

        【활용 시나리오】
        - 분할 비율(rt_vl)을 분석하여 모회사-신설법인 간 주주가치 배분의 적정성 평가
        - 외부평가기관(exevl_int) 여부를 통해 분할 절차의 투명성 및 공정성 검증
        - 주식매수청구권 행사 가격(aprskh_prc)과 시장가격 비교로 소수주주 보호 수준 판단
        - tast(총자산), cpt(자본금) 변동을 통해 분할 전후 재무구조 변동성 분석
        - 신설법인의 발행주식수(cnt)와 기존 주식수(isstk_cnt) 비교로 주주 가치 희석 여부 평가

        【효과적 활용 방법】
        - 주주총회 승인 일정(ap_gmtsck)과 매수청구권 행사기간(aprskh_pd_bgd~aprskh_pd_edd) 분석으로 주주 방어권 보장 수준 평가
        - 분할 목적(grtmn_etc) 명세를 통해 경영구조 재편 목적이 지배구조 변경, 사업재편, 부실사업 정리 중 무엇인지 구체 분석
        - 분할 이후 get_major_holder_changes 호출로 지배주주 지분율 변화 추적
        - get_stock_total 호출로 분할 전후 주식수 및 유통물량 변동 분석

        【주의사항 및 팁】
        - 분할 비율(rt_vl)이 비정상적으로 불균형할 경우, 소수주주 이익 침해 및 주주총회 반대 가능성 존재
        - 외부평가기관 미선정(exevl_int 부재) 시 분할 무효 소송 리스크 상승 가능성 주의
        - 신설법인의 재무구조(tast, cpt)가 취약할 경우, 향후 부실기업 리스크로 전이될 수 있음
        """,
    tags={"분할", "증권신고서", "분할", "증권신고서"}
)
def get_division_report(
    corp_code: str,
    bgn_de: str,
    end_de: str,
    ctx: Optional[Any] = None
) -> TextContent:
    """
    분할 증권신고서 조회

    Args:
        corp_code (str): 고유번호 (8자리)
        bgn_de (str): 검색시작 접수일자 (예: 20240101)
        end_de (str): 검색종료 접수일자 (예: 20241231)

    참고: https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020059
    """
    result = with_context(ctx, "get_division_report", lambda context: context.ds006.get_division_report(
        corp_code=corp_code,
        bgn_de=bgn_de,
        end_de=end_de
    ))
    return TextContent(type="text", text=str(result))
