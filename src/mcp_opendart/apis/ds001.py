from typing import Dict, Any, Optional, List

from ..apis.client import OpenDartClient


class DisclosureAPI:
    """DS001 - 공시정보 API"""
    
    def __init__(self, client: OpenDartClient):
        self.client = client
    
    def get_corporation_code_by_name(self, corp_name: str) -> Dict[str, Any]:
        """
        기업명으로 고유번호 검색
        """
        from ..utils.corp_code_search import read_local_xml, parse_corp_code_xml, search_corporations
        
        try:
            xml_content = read_local_xml()
            corporations = parse_corp_code_xml(xml_content)
            results = search_corporations(corporations, corp_name)
            
            return {
                "status": "000",
                "message": "정상",
                "items": results
            }
        except FileNotFoundError:
            return {
                "status": "400",
                "message": "CORPCODE.xml 파일이 없습니다. get_corporation_code를 먼저 실행해주세요."
            }
        except Exception as e:
            return {
                "status": "500",
                "message": f"오류가 발생했습니다: {str(e)}"
            }    
            
    def get_disclosure_list(
        self,
        corp_code: Optional[str] = None,
        bgn_de: Optional[str] = None,
        end_de: Optional[str] = None,
        last_report_at: Optional[str] = None,
        pblntf_ty: Optional[str] = None,
        pblntf_detail_ty: Optional[str] = None,
        corp_cls: Optional[str] = None,
        sort: Optional[str] = None,
        sort_mth: Optional[str] = None,
        page_no: int = 1,
        page_count: int = 10
    ) -> Dict[str, Any]:
        """
        공시검색
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001
        """
        endpoint = "list.json"
        params = {
            "corp_code": corp_code,
            "bgn_de": bgn_de,
            "end_de": end_de,
            "last_reprt_at": last_report_at,
            "pblntf_ty": pblntf_ty,
            "pblntf_detail_ty": pblntf_detail_ty,
            "corp_cls": corp_cls,
            "sort": sort,
            "sort_mth": sort_mth,
            "page_no": page_no,
            "page_count": page_count
        }
        # None 값 제거
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.client.get(endpoint, params)

    def get_corporation_info(self, corp_code: str) -> Dict[str, Any]:
        """
        기업개황 조회
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019002
        """
        endpoint = "company.json"
        params = {"corp_code": corp_code}
        return self.client.get(endpoint, params)

    def get_disclosure_document(self, rcp_no: str) -> Dict[str, Any]:
        """
        공시서류원본파일 조회
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019003
        """
        import zipfile
        import io
        
        endpoint = "document.xml"
        params = {"rcept_no": rcp_no}
        response = self.client.get(endpoint, params)
        
        # Save the response to the specified directory if successful
        if response.get("status") == "000" and isinstance(response.get("content"), bytes):
            import os
            from pathlib import Path
            
            # Get the absolute path of the project root
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / 'opendart' / 'utils' / 'data'
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # Save the zip content to a temporary file
            zip_path = data_dir / f'disclosure_{rcp_no}.zip'
            with open(zip_path, 'wb') as f:
                f.write(response["content"])
            
            try:
                # Extract the XML file from the zip
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(data_dir)
                
                # Remove the temporary zip file
                os.remove(zip_path)
                
                # Add file path information to the response
                response["saved_path"] = str(data_dir / f'disclosure_{rcp_no}.xml')
            except Exception as e:
                print(f"Failed to extract zip file: {e}")
                if os.path.exists(zip_path):
                    os.remove(zip_path)
        
        return response
    
    def get_corporation_code(self) -> Dict[str, Any]:
        """
        고유번호 조회 및 저장
        https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018
        """
        import zipfile
        import io
        
        endpoint = "corpCode.xml"
        response = self.client.get(endpoint)
        
        # Save the response to the specified file
        if response.get("status") == "000" and isinstance(response.get("content"), bytes):
            import os
            from pathlib import Path
            
            # Get the absolute path of the project root
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / 'opendart' / 'utils' / 'data'
            data_dir.mkdir(parents=True, exist_ok=True)
            
            # Save the zip content to a temporary file
            zip_path = data_dir / 'CORPCODE.zip'
            with open(zip_path, 'wb') as f:
                f.write(response["content"])
            
            try:
                # Extract the XML file from the zip
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(data_dir)
                
                # Remove the temporary zip file
                os.remove(zip_path)
            except Exception as e:
                print(f"Failed to extract zip file: {e}")
                if os.path.exists(zip_path):
                    os.remove(zip_path)
        
        return response

