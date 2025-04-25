import os
import logging
from typing import Literal, cast
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
    transport: Literal["stdio", "sse"] = "stdio"
    
    @classmethod
    def from_env(cls) -> "MCPConfig":
        """Create MCP configuration from environment variables."""
        return cls(
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            server_name=os.getenv("MCP_SERVER_NAME", "opendart-mcp"),
            transport=cast(Literal["stdio", "sse"], os.getenv("TRANSPORT", "stdio"))
        )

# 설정 인스턴스 생성
mcp_config = MCPConfig.from_env()
opendart_config = OpenDartConfig.from_env()