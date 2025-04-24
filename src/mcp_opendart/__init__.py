# OpenDART MCP Python 패키지 초기화
import importlib
import click
from mcp_opendart.server import mcp

# 도구 모듈 등록 (모든 @mcp.tool decorator)
for module_name in [
    "disclosure_tools",
    "financial_info_tools",
    "major_report_tools",
    "ownership_disclosure_tools",
    "periodic_report_tools",
    "securities_filing_tools",
]:
    importlib.import_module(f"mcp_opendart.tools.{module_name}")

@click.command()
def main():
    """OpenDART MCP 서버를 실행합니다."""
    mcp.run()

if __name__ == "__main__":
    main()
