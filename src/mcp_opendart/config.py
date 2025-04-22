import os
import requests
from urllib.parse import urljoin
import json
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 로거 설정
logger = logging.getLogger(__name__)

@dataclass
class OpenDartConfig:
    """OpenDART API configuration."""
    
    api_key: str
    base_url: str = "https://opendart.fss.or.kr/api/"
    cache_ttl_hours: int = 1
    cache_max_size: int = 1000
    api_rate_limit: int = 1000
    api_rate_limit_period: int = 3600
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: str = "opendart.log"
    
    @classmethod
    def from_env(cls) -> "OpenDartConfig":
        """Create configuration from environment variables.

        Returns:
            OpenDartConfig with values from environment variables

        Raises:
            ValueError: If any required environment variable is missing
        """
        api_key = os.getenv("OPENDART_API_KEY")
        if not api_key:
            raise ValueError("OpenDART API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
            
        return cls(
            api_key=api_key,
            base_url=os.getenv("OPENDART_BASE_URL", "https://opendart.fss.or.kr/api/"),
            cache_ttl_hours=int(os.getenv("CACHE_TTL_HOURS", "1")),
            cache_max_size=int(os.getenv("CACHE_MAX_SIZE", "1000")),
            api_rate_limit=int(os.getenv("API_RATE_LIMIT", "1000")),
            api_rate_limit_period=int(os.getenv("API_RATE_LIMIT_PERIOD", "3600")),
            log_format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
            log_file=os.getenv("LOG_FILE", "opendart.log")
        )

@dataclass
class MCPConfig:
    """MCP Server configuration."""
    
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    server_name: str = "opendart-mcp"
    
    @classmethod
    def from_env(cls) -> "MCPConfig":
        """Create MCP configuration from environment variables."""
        return cls(
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            server_name=os.getenv("MCP_SERVER_NAME", "opendart-mcp")
        )

# 설정 인스턴스 생성
mcp_config = MCPConfig.from_env()
opendart_config = OpenDartConfig.from_env()

class OpenDartClient:
    """OpenDART API 클라이언트"""
    
    def __init__(self, config: Optional[OpenDartConfig] = None):
        self.config = config or opendart_config
        self.api_key = self.config.api_key
        self.base_url = self.config.base_url
        
        if not self.api_key:
            raise ValueError("OpenDART API 키가 설정되지 않았습니다.")
    
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None, method: str = "GET") -> Dict[str, Any]:
        """API 요청을 보내고 응답을 반환합니다."""
        if params is None:
            params = {}
        
        # API 키 추가
        params["crtfc_key"] = self.api_key
        
        url = urljoin(self.base_url, endpoint)
        
        # 디버그 로깅 추가
        print(f"\n=== API 요청 정보 ===")
        print(f"URL: {url}")
        print(f"Method: {method}")
        print(f"Parameters: {params}")
        print("====================")
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params)
            elif method.upper() == "POST":
                response = requests.post(url, data=params)
            else:
                raise ValueError(f"지원하지 않는 HTTP 메서드: {method}")
            
            # 응답 로깅 추가
            print(f"\n=== API 응답 정보 ===")
            print(f"상태 코드: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type', '없음')}")
            if "application/json" in response.headers.get("Content-Type", ""):
                print(f"응답 내용: {response.text}")
            print("====================")
            
            response.raise_for_status()
            
            # 응답 형식에 따라 처리
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return response.json()
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
                    import zipfile
                    import io
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
    
    def get(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """GET 요청을 수행합니다."""
        return self._make_request(endpoint, params, "GET")
    
    def post(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """POST 요청을 수행합니다."""
        return self._make_request(endpoint, params, "POST")

    def download(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
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
            print(f"\n=== API 응답 정보 ===")
            print(f"상태 코드: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type', '없음')}")
            print("====================")
            
            # 응답 내용 반환
            return {
                "status": "000",
                "message": "정상",
                "content": response.content
            }
                
        except requests.RequestException as e:
            logger.error(f"파일 다운로드 실패: {str(e)}")
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}