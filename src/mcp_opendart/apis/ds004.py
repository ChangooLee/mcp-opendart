from typing import Dict, Any, Optional, List

from ..apis.client import OpenDartClient


class OwnershipDisclosureAPI:
    """DS004 - 지분공시 종합정보 API"""
    
    def __init__(self, client: OpenDartClient):
        self.client = client
    
    def get_major_holder_changes(
        self, 
        corp_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        대량보유 상황보고
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019021
        """
        endpoint = "majorstock.json"
        params = {
            "corp_code": corp_code
        }
        # None 값 제거
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.client.get(endpoint, params)
    
    def get_executive_trading(
        self, 
        corp_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        임원·주요주주 소유보고
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019022
        """
        endpoint = "elestock.json"
        params = {
            "corp_code": corp_code
        }
        # None 값 제거
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.client.get(endpoint, params)