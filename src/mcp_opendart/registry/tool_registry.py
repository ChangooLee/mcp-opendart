import logging

logger = logging.getLogger("mcp-opendart")

from typing import Dict, List, Optional

class ToolMetadata:
    def __init__(
        self,
        name: str,
        description: str,
        parameters: dict,
        korean_name: Optional[str] = None,
        linked_tools: Optional[List[str]] = None
    ):
        self.name = name
        self.korean_name = korean_name
        self.description = description
        self.parameters = parameters
        self.linked_tools = linked_tools or []

    def to_function_schema(self) -> dict:
        """OpenAI function_call용 포맷 변환"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

    def brief_summary(self) -> str:
        """System prompt용 간단 요약"""
        kor = f" ({self.korean_name})" if self.korean_name else ""
        return f"- {self.name}{kor}: {self.description}"

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, ToolMetadata] = {}

    def register_tool(
        self,
        name: str,
        description: str,
        parameters: dict,
        korean_name: Optional[str] = None,
        linked_tools: Optional[List[str]] = None
    ):
        self.tools[name] = ToolMetadata(
            name=name,
            description=description,
            parameters=parameters,
            korean_name=korean_name,
            linked_tools=linked_tools
        )

    def list_tools(self) -> List[ToolMetadata]:
        return list(self.tools.values())

    def export_function_schemas(self) -> List[dict]:
        logger.info(f"Exporting function schemas: {self.tools.values()}")
        return [tool.to_function_schema() for tool in self.tools.values()]

    def export_brief_summary(self) -> str:
        return "\n".join(tool.brief_summary() for tool in self.tools.values())

    def get_tool(self, name: str) -> Optional[ToolMetadata]:
        return self.tools.get(name)