from mcp_opendart.registry.tool_registry import ToolRegistry

def export_prompt_with_links(registry: ToolRegistry) -> str:
    """
    모든 도구의 설명과 연관 도구(linked_tools)를 포함한 system prompt를 생성합니다.
    Claude 또는 Open-WebUI에게 도구 간 관계를 명확히 전달하기 위해 사용됩니다.
    """
    lines = []
    for tool in registry.list_tools():
        kor = f" ({tool.korean_name})" if tool.korean_name else ""
        line = f"- {tool.name}{kor}: {tool.description.strip()}"
        if tool.linked_tools:
            linked = ", ".join(tool.linked_tools)
            line += f"\n  ↪ 연관 도구: {linked}"
        lines.append(line)
    return "\n".join(lines)

def build_system_prompt(registry: ToolRegistry) -> str:
    """
    Claude 또는 기타 LLM에게 제공할 system prompt를 생성합니다.
    도구의 설명과 함께 연관 도구 정보를 포함합니다.
    """
    intro = "당신은 OpenDART 공시 분석 전문가입니다.\n"
    intro += "아래는 사용할 수 있는 도구 목록입니다:\n\n"
    tools = export_prompt_with_links(registry)
    outro = "\n\n사용자의 질문에 따라 가장 적절한 도구를 선택하고,\n필요시 연관 도구도 함께 사용할 수 있습니다."
    return intro + tools + outro
