from typing import Dict, Any, Optional, List

from ..apis.client import OpenDartClient


class FinancialInfoAPI:
    """DS003 - 정기보고서 재무정보 API"""
    
    def __init__(self, client: OpenDartClient):
        self.client = client
    
    def get_single_acnt(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str,
        fs_div: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        단일회사 주요계정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019016
        """
        endpoint = "fnlttSinglAcnt.json"
        data = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code,
            "fs_div": fs_div
        }
        # None 값 제거
        data = {k: v for k, v in data.items() if v is not None}
        
        return self.client.get(endpoint, data)
    
    def get_multi_acnt(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str,
        fs_div: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        다중회사 주요계정
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019017
        """
        endpoint = "fnlttMultiAcnt.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code,
            "fs_div": fs_div
        }
        # None 값 제거
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.client.get(endpoint, params)
    
    def get_xbrl_file(
        self, 
        rcept_no: str, 
        reprt_code: str
    ) -> Dict[str, Any]:
        """
        재무제표 원본파일(XBRL)
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019019
        
        Args:
            rcept_no (str): 접수번호
            reprt_code (str): 보고서 코드 (1분기보고서: 11013, 반기보고서: 11012, 3분기보고서: 11014, 사업보고서: 11011)
        """
        endpoint = "fnlttXbrl.xml"
        data = {
            "rcept_no": rcept_no,
            "reprt_code": reprt_code
        }
        # None 값 제거
        data = {k: v for k, v in data.items() if v is not None}
        
        response = self.client.download(endpoint, data)
        
        # Save the response to the specified directory if successful
        if response.get("status") == "000" and isinstance(response.get("content"), bytes):
            import os
            from pathlib import Path
            import zipfile
            from io import BytesIO
            
            # Get the absolute path of the project root
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / 'opendart' / 'utils' / 'data'
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # Create a directory for extracted files using rcept_no
            extract_dir = data_dir / f'{rcept_no}_{reprt_code}'
            extract_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract ZIP content
            with zipfile.ZipFile(BytesIO(response["content"])) as zip_file:
                zip_file.extractall(extract_dir)
            
            # Add extracted directory path information to the response
            response["saved_path"] = str(extract_dir)
        
        return response
    
    def get_single_acc(
        self,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
        fs_div: str = "OFS",
    ) -> dict[str, Any]:
        """
        단일회사 전체 재무제표 API
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019020

        Args:
            corp_code (str): 고유번호
            bsns_year (str): 사업연도
            reprt_code (str): 보고서 코드 (1분기보고서: 11013, 반기보고서: 11012, 3분기보고서: 11014, 사업보고서: 11011)
            fs_div (str, optional): 개별/연결구분 (OFS:재무제표, CFS:연결재무제표). Defaults to "OFS".

        Returns:
            dict[str, Any]: API 응답
        """
        return self.client.get(
            "fnlttSinglAcntAll.json",
            params={
                "corp_code": corp_code,
                "bsns_year": bsns_year,
                "reprt_code": reprt_code,
                "fs_div": fs_div,
            },
        )
    
    def get_xbrl_taxonomy(
        self, 
        sj_div: str, 
        corp_code: Optional[str] = None, 
        bsns_year: Optional[str] = None, 
        reprt_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        XBRL택사노미재무제표양식
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2020001
        """
        endpoint = "xbrlTaxonomy.json"
        params = {
            "sj_div": sj_div,
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code
        }
        # None 값 제거
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.client.get(endpoint, params)
        
    def get_single_index(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str,
        idx_cl_code: str
    ) -> Dict[str, Any]:
        """
        단일회사 주요 재무지표
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2022001

        Args:
            corp_code (str): 고유번호
            bsns_year (str): 사업연도
            reprt_code (str): 보고서 코드 (11011:사업보고서, 11012:반기보고서, 11013:1분기보고서, 11014:3분기보고서)
            idx_cl_code (str): 지표분류코드 (M210000:수익성지표, M220000:안정성지표, M230000:성장성지표, M240000:활동성지표)
        """
        endpoint = "fnlttSinglIndx.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code,
            "idx_cl_code": idx_cl_code
        }
        # None 값 제거
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.client.get(endpoint, params)
        
    def get_multi_index(
        self, 
        corp_code: str, 
        bsns_year: str, 
        reprt_code: str,
        idx_cl_code: str
    ) -> Dict[str, Any]:
        """
        다중회사 주요 재무지표
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2022002

        Args:
            corp_code (str): 고유번호
            bsns_year (str): 사업연도
            reprt_code (str): 보고서 코드 (11011:사업보고서, 11012:반기보고서, 11013:1분기보고서, 11014:3분기보고서)
            idx_cl_code (str): 지표분류코드 (M210000:수익성지표, M220000:안정성지표, M230000:성장성지표, M240000:활동성지표)
        """
        endpoint = "fnlttCmpnyIndx.json"
        params = {
            "corp_code": corp_code, 
            "bsns_year": bsns_year, 
            "reprt_code": reprt_code,
            "idx_cl_code": idx_cl_code
        }
        # None 값 제거
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.client.get(endpoint, params)