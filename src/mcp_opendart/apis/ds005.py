from typing import Dict, Any, Optional, List

from ..apis.client import OpenDartClient


class MajorReportAPI:
    """DS005 - 주요사항보고서 주요정보 API"""
    
    def __init__(self, client: OpenDartClient):
        self.client = client
    
    def get_asset_transfer(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        자산양수도(기타), 풋백옵션
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020018
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "astInhtrfEtcPtbkOpt.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_bankruptcy(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        부도발생
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020019
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "dfOcr.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_business_suspension(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        영업정지
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020020
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "bsnSp.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_rehabilitation(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        회생절차 개시신청
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020021
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "ctrcvsBgrq.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_dissolution(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        해산사유 발생
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020022
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "dsRsOcr.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_paid_in_capital_increase(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        유상증자 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020023
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "piicDecsn.json"
        params = {            
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_free_capital_increase(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        무상증자 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020024
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "fricDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_paid_free_capital_increase(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        유무상증자 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020025
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "pifricDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_capital_reduction(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        감자 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020026
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "crDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_creditor_management(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        채권은행 등의 관리절차 개시
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020027
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "bnkMngtPcbg.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_lawsuit(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        소송 등의 제기
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020028
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "lwstLg.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_foreign_listing_decision(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        해외 증권시장 주권등 상장 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020029
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "ovLstDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_foreign_delisting_decision(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        해외 증권시장 주권등 상장폐지 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020030
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "ovDlstDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_foreign_listing(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        해외 증권시장 주권등 상장
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020031
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "ovLst.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_foreign_delisting(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        해외 증권시장 주권등 상장폐지
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020032
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "ovDlst.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_convertible_bond(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        전환사채권 발행결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020033
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "cvbdIsDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_bond_with_warrant(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        신주인수권부사채권 발행결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020034
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "bdwtIsDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_exchangeable_bond(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        교환사채권 발행결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020035
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "exbdIsDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_creditor_management_termination(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        채권은행 등의 관리절차 중단
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020036
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "bnkMngtPcsp.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_write_down_bond(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        상각형 조건부자본증권 발행결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020037
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "wdCocobdIsDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_treasury_stock_acquisition(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        자기주식 취득 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020038
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "tsstkAqDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_treasury_stock_disposal(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        자기주식 처분 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020039
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "tsstkDpDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_treasury_stock_trust_contract(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        자기주식취득 신탁계약 체결 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020040
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "tsstkAqTrctrCnsDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_treasury_stock_trust_termination(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        자기주식취득 신탁계약 해지 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020041
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "tsstkAqTrctrCcDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_business_transfer(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        영업양수 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020042
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "bsnInhDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_business_acquisition(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        영업양도 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020043
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "bsnTrfDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_tangible_asset_transfer(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        유형자산 양수 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020044
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "tgastInhDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_tangible_asset_acquisition(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        유형자산 양도 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020045
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "tgastTrfDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_other_corp_stock_transfer(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        타법인 주식 및 출자증권 양수결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020046
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "otcprStkInvscrInhDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_other_corp_stock_acquisition(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        타법인 주식 및 출자증권 양도결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020047
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "otcprStkInvscrTrfDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_stock_related_bond_transfer(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        주권 관련 사채권 양수 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020048
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "stkrtbdInhDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_stock_related_bond_acquisition(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        주권 관련 사채권 양도 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020049
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "stkrtbdTrfDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_merger(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        회사합병 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020050
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "cmpMgDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_division(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        회사분할 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020051
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "cmpDvDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_division_merger(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        회사분할합병 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020052
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "cmpDvmgDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)

    def get_stock_exchange(
        self, 
        corp_code: str, 
        bgn_de: str, 
        end_de: str
    ) -> Dict[str, Any]:
        """
        주식교환·이전 결정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020053
        
        Parameters:
            corp_code (str): 고유번호 공시대상회사의 고유번호(8자리) ※ 개발가이드 > 공시정보 > 고유번호 참고
            bgn_de (str): 검색시작 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
            end_de (str): 검색종료 접수일자(YYYYMMDD) ※ 2015년 이후 부터 정보제공
        """
        endpoint = "stkExtrDecsn.json"
        params = {
            "corp_code": corp_code, 
            "bgn_de": bgn_de, 
            "end_de": end_de
        }
        return self.client.get(endpoint, params)