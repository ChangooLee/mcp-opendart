import requests
from urllib.parse import urljoin
import json
import logging
from typing import Dict, Any, Optional
import zipfile
import io

from ..config import opendart_config, OpenDartConfig

# 로거 설정
logger = logging.getLogger(__name__)

class OpenDartClient:
    """OpenDART API 클라이언트"""
    
    def __init__(self, config: Optional[OpenDartConfig] = None):
        self.config = config or opendart_config
        self.api_key = self.config.api_key
        self.base_url = self.config.base_url
        
        if not self.api_key:
            raise ValueError("OpenDART API 키가 설정되지 않았습니다.")
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None, method: str = "GET") -> Dict[str, Any]:
        """API 요청을 보내고 응답을 반환합니다."""
        if params is None:
            params = {}
        
        # API 키 추가
        params["crtfc_key"] = self.api_key
        
        url = urljoin(self.base_url, endpoint)
        
        # 디버그 로깅 추가
        logger.debug(f"\n=== API 요청 정보 ===")
        logger.debug(f"URL: {url}")
        logger.debug(f"Method: {method}")
        logger.debug(f"Parameters: {params}")
        logger.debug("====================")
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, data=params)
            else:
                raise ValueError(f"지원하지 않는 HTTP 메서드: {method}")
            
            # 응답 로깅 추가
            logger.debug(f"\n=== API 응답 정보 ===")
            logger.debug(f"상태 코드: {response.status_code}")
            logger.debug(f"Content-Type: {response.headers.get('Content-Type', '없음')}")
            if "application/json" in response.headers.get("Content-Type", ""):
                logger.debug(f"응답 내용: {response.text}")
            logger.debug("====================")
            
            response.raise_for_status()
            
            # 응답 형식에 따라 처리
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                data: Dict[str, Any] = response.json()
                return data
            elif "application/zip" in content_type or "application/x-zip-compressed" in content_type:
                return {
                    "status": "000",
                    "message": "정상",
                    "content": response.content
                }
            elif "text/xml" in content_type or "application/xml" in content_type:
                return {
                    "status": "000",
                    "message": "정상",
                    "content": response.text
                }
            else:
                # 응답이 zip 파일인지 확인
                try:
                    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
                    return {
                        "status": "000",
                        "message": "정상",
                        "content": response.content
                    }
                except:
                    return {
                        "status": "000",
                        "message": "정상",
                        "content": response.text
                    }
        
        except requests.RequestException as e:
            logger.error(f"API 요청 실패: {str(e)}")
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """GET 요청을 수행합니다."""
        return self._make_request(endpoint, params, "GET")
    
    def post(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """POST 요청을 수행합니다."""
        return self._make_request(endpoint, params, "POST")

    def download(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        파일을 다운로드합니다.
        
        Args:
            endpoint (str): API 엔드포인트
            params (Dict[str, Any], optional): 요청 파라미터
            
        Returns:
            Dict[str, Any]: 다운로드 결과
        """
        if params is None:
            params = {}
        
        # API 키 추가
        params["crtfc_key"] = self.api_key
        
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            # 디버그 로깅 추가
            logger.debug(f"\n=== API 응답 정보 ===")
            logger.debug(f"상태 코드: {response.status_code}")
            logger.debug(f"Content-Type: {response.headers.get('Content-Type', '없음')}")
            logger.debug("====================")
            
            # 응답 내용 반환
            return {
                "status": "000",
                "message": "정상",
                "content": response.content
            }
                
        except requests.RequestException as e:
            logger.error(f"파일 다운로드 실패: {str(e)}")
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}