from typing import Dict, Any, List
from mcp.server.fastmcp import Context

from opendart_mcp.server import mcp

@mcp.tool()
def get_stock_increase_decrease(ctx: Context, corp_name: str) -> Dict[str, Any]:
    """증자(감자) 현황
    
    Args:
        corp_code (str): 고유번호, 공시대상회사의 고유번호(8자리)
        bsns_year (str): 사업연도, 2015년 이후 부터 정보제공
        reprt_code (str): 보고서코드, 1분기보고서: 11013, 반기보고서: 11012, 3분기보고서: 11014, 사업보고서: 11011
    Returns:		
        status : 에러 및 정보 코드
        message	에러 및 정보 메시지
        list (dict)		
            rcept_no : 접수번호, 접수번호(14자리) ※ 공시뷰어 연결에 이용예시 (https://dart.fss.or.kr/dsaf001/main.do?rcpNo=접수번호)
            corp_cls : 법인구분, 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
            corp_code : 고유번호, 공시대상회사의 고유번호(8자리)
            corp_name :	법인명,	법인명
            isu_dcrs_de : 주식발행 감소일자, 주식발행 감소일자
            isu_dcrs_stle : 발행 감소 형태, 발행 감소 형태
            isu_dcrs_stock_knd : 발행 감소 주식 종류, 발행 감소 주식 종류
            isu_dcrs_qy : 발행 감소 수량, 9,999,999,999
            isu_dcrs_mstvdv_fval_amount : 발행 감소 주당 액면 가액, 9,999,999,999
            isu_dcrs_mstvdv_amount : 발행 감소 주당 가액, 9,999,999,999
            stlm_dt : 결산기준일, YYYY-MM-DD
    """
    return ctx.request_context.lifespan_context.ds002.get_stock_increase_decrease(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool()
def get_dividend_info(ctx: Context, corp_name: str) -> Dict[str, Any]:
    """배당에 관한 사항
    
    Args:
        corp_code (str): 고유번호, 공시대상회사의 고유번호(8자리)
        bsns_year (str): 사업연도, 2015년 이후 부터 정보제공
        reprt_code (str): 보고서코드, 1분기보고서: 11013, 반기보고서: 11012, 3분기보고서: 11014, 사업보고서: 11011
    Returns:		
        status : 에러 및 정보 코드
        message	에러 및 정보 메시지
        list (dict)		
            rcept_no : 접수번호, 접수번호(14자리) ※ 공시뷰어 연결에 이용예시 (https://dart.fss.or.kr/dsaf001/main.do?rcpNo=접수번호)
            corp_cls : 법인구분, 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
            corp_code : 고유번호, 공시대상회사의 고유번호(8자리)
            corp_name :	법인명,	법인명
            se : 구분, 유상증자(주주배정), 전환권행사 등
            stock_knd : 주식 종류, 보통주 등
            thstrm : 당기, 9,999,999,999
            frmtrm : 전기, 9,999,999,999
            lwfr : 전전기, 9,999,999,999
            stlm_dt : 결산기준일, YYYY-MM-DD
    """
    return ctx.request_context.lifespan_context.ds002.get_dividend_info(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )

@mcp.tool()
def get_treasury_stock(ctx: Context, corp_name: str) -> Dict[str, Any]:
    """배당에 관한 사항
    
    Args:
        corp_code (str): 고유번호, 공시대상회사의 고유번호(8자리)
        bsns_year (str): 사업연도, 2015년 이후 부터 정보제공
        reprt_code (str): 보고서코드, 1분기보고서: 11013, 반기보고서: 11012, 3분기보고서: 11014, 사업보고서: 11011
    Returns:		
        status : 에러 및 정보 코드
        message	에러 및 정보 메시지
        list (dict)		
            rcept_no : 접수번호, 접수번호(14자리) ※ 공시뷰어 연결에 이용예시 (https://dart.fss.or.kr/dsaf001/main.do?rcpNo=접수번호)
            corp_cls : 법인구분, 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타)
            corp_code : 고유번호, 공시대상회사의 고유번호(8자리)
            corp_name :	법인명,	법인명
            acqs_mth1 : 취득방법 대분류, 배당가능이익범위 이내 취득, 기타취득, 총계 등
            acqs_mth2 : 취득방법 중분류, 직접취득, 신탁계약에 의한취득, 기타취득, 총계 등
            acqs_mth3 : 취득방법 소분류, 장내직접취득, 장외직접취득, 공개매수, 주식매수청구권행사, 수탁자보유물량, 현물보유량, 기타취득, 소계, 총계 등
            stock_knd : 주식 종류, 보통주, 우선주 등
            bsis_qy : 기초 수량, 9,999,999,999
            change_qy_acqs : 변동 수량 취득, 9,999,999,999
            change_qy_dsps : 변동 수량 처분, 9,999,999,999
            change_qy_incnr : 변동 수량 소각, 9,999,999,999
            trmend_qy : 기말 수량, 9,999,999,999
            rm : 비고, 비고
            stlm_dt : 결산기준일, YYYY-MM-DD
    """
    return ctx.request_context.lifespan_context.ds002.get_treasury_stock(
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code
    )  