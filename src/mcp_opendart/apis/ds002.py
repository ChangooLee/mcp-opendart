from typing import Dict, Any, Optional, List

from ..apis.client import OpenDartClient


class PeriodicReportAPI:
    """DS002 - 정기보고서 주요정보 API"""
    
    def __init__(self, client: OpenDartClient):
        self.client = client
    
    def get_stock_increase_decrease(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        증자(감자) 현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019004
        """
        endpoint = "irdsSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_dividend_info(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        배당에 관한 사항
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019005
        """
        endpoint = "alotMatter.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_treasury_stock(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        자기주식 취득 및 처분 현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019006
        """
        endpoint = "tesstkAcqsDspsSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_major_shareholder(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        최대주주 현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019007
        """
        endpoint = "hyslrSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_major_shareholder_changes(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        최대주주 변동현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019008
        """
        endpoint = "hyslrChgSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_minority_shareholder(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        소액주주 현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019009
        """
        endpoint = "mrhlSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_executive_info(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        임원 현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019010
        """
        endpoint = "exctvSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_employee_info(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        직원 현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019011
        """
        endpoint = "empSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_individual_compensation(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        이사·감사의 개인별 보수현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019012
        """
        endpoint = "hmvAuditIndvdlBySttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_total_compensation(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        이사·감사 전체의 보수현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019013
        """
        endpoint = "hmvAuditAllSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_individual_compensation_amount(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        개인별 보수지급 금액
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019014
        """
        endpoint = "indvdlByPay.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_investment_in_other_corp(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        타법인 출자현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019015
        """
        endpoint = "otrCprInvstmntSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_stock_total(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        주식의 총수 현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020002
        """
        endpoint = "stockTotqySttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_debt_securities_issued(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        채무증권 발행실적
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020003
        """
        endpoint = "detScritsIsuAcmslt.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_commercial_paper_outstanding(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        기업어음증권 미상환 잔액
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020004
        """
        endpoint = "entrprsBilScritsNrdmpBlce.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_short_term_bond_outstanding(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        단기사채 미상환 잔액
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020005
        """
        endpoint = "srtpdPsndbtNrdmpBlce.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_corporate_bond_outstanding(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        회사채 미상환 잔액
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020006
        """
        endpoint = "cprndNrdmpBlce.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_hybrid_securities_outstanding(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        신종자본증권 미상환 잔액
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020007
        """
        endpoint = "newCaplScritsNrdmpBlce.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_contingent_convertible_bond_outstanding(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        조건부 자본증권 미상환 잔액
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020008
        """
        endpoint = "cndlCaplScritsNrdmpBlce.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_accounting_auditor_opinion(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        회계감사인의 명칭 및 감사의견
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020009
        
        Args:
            corp_code: 고유번호
            bsns_year: 사업연도
            reprt_code: 보고서 코드 (11011: 사업보고서, 11012: 반기보고서, 11013: 1분기보고서, 11014: 3분기보고서)
            
        Returns:
            감사인의 감사의견 정보
        """
        endpoint = "accnutAdtorNmNdAdtOpinion.json"
        params = {
            "corp_code": corp_code,
            "bsns_year": bsns_year,
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params=params)
    
    def get_audit_service_contract(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        감사용역체결현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020010
        """
        endpoint = "adtServcCnclsSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_non_audit_service_contract(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        회계감사인과의 비감사용역 계약체결 현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020011
        """
        endpoint = "accnutAdtorNonAdtServcCnclsSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_outside_director_status(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        사외이사 및 그 변동현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020012
        """
        endpoint = "outcmpnyDrctrNdChangeSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_unregistered_exec_compensation(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        미등기임원 보수현황
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020013
        """
        endpoint = "unrstExctvMendngSttus.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_executive_compensation_approved(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        이사·감사 전체의 보수현황(주주총회 승인금액)
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020014
        """
        endpoint = "drctrAdtAllMendngSttusGmtsckConfmAmount.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_executive_compensation_by_type(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        이사·감사 전체의 보수현황(보수지급금액 - 유형별)
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020015
        """
        endpoint = "drctrAdtAllMendngSttusMendngPymntamtTyCl.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_public_fund_usage(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        공모자금의 사용내역
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020016
        """
        endpoint = "pssrpCptalUseDtls.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)
    
    def get_private_fund_usage(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        사모자금의 사용내역
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2020017
        """
        endpoint = "prvsrpCptalUseDtls.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        return self.client.get(endpoint, params)