from typing import Dict, Any, Optional, List

from ..apis.client import OpenDartClient


class SecuritiesFilingAPI:
    """DS006 - 증권신고서 주요정보 API"""
    
    def __init__(self, client: OpenDartClient):
        self.client = client
    
    def get_equity(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        지분증권
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020054
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "estkRs.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_debt(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        채무증권
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020055
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "bdRs.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_depository_receipt(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        증권예탁증권
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020056
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "stkdpRs.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_merger_report(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        합병
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020057
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "mgRs.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_stock_exchange_report(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        주식의포괄적교환·이전
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020058
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "extrRs.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_division_report(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        분할
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020059
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "dvRs.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)