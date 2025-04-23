# MCP OpenDART

![License](https://img.shields.io/github/license/ChangooLee/mcp-opendart)

Model Context Protocol (MCP) server for OpenDART (Korea Financial Supervisory Service's Data Analysis, Retrieval and Transfer System). This integration supports secure access to financial data through OpenDART's API system.

## Example Usage

Ask your AI assistant to:

- **📊 Financial Reports** - "Get the latest quarterly report for Samsung Electronics"
- **🔍 Disclosure Search** - "Find major shareholding changes in KOSPI companies last month"
- **📈 Corporate Analysis** - "Show me the financial statements of Hyundai Motor for the past 3 years"
- **⚡ Real-time Updates** - "Get today's important disclosures for technology sector"

### Feature Demo

[Demo video will be added here]

### Compatibility

|Feature|Support Status|
|---|---|
|**Disclosure Information**|✅ Fully supported|
|**Periodic Reports**|✅ Fully supported|
|**Financial Information**|✅ Fully supported|
|**Ownership Disclosure**|✅ Fully supported|
|**Major Reports**|✅ Fully supported|
|**Securities Filing**|✅ Fully supported|

## Quick Start Guide

### 1. Authentication Setup

First, obtain your OpenDART API key:

1. Go to [OpenDART](https://opendart.fss.or.kr/)
2. Sign up and request an API key
3. Wait for approval and receive your API key

### 2. Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

## IDE Integration

MCP OpenDART is designed to be used with AI assistants through IDE integration.

> [!TIP]
> **To apply the configuration in Claude Desktop:**
>
> **Method 1 (Recommended)**: Click hamburger menu (☰) > Settings > Developer > "Edit Config" button
>
> **Method 2**: Locate and edit the configuration file directly:
> - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
> - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
> - **Linux**: `~/.config/Claude/claude_desktop_config.json`
>
> **For Cursor**: Open Settings → Features → MCP Servers → + Add new global MCP server

### Configuration Example

```json
{
  "mcpServers": {
    "mcp-opendart": {
      "command": "python",
      "args": ["-m", "mcp_opendart"],
      "env": {
        "OPENDART_API_KEY": "your_api_key_here",
        "OPENDART_BASE_URL": "https://opendart.fss.or.kr/api/",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "LOG_LEVEL": "INFO",
        "MCP_SERVER_NAME": "opendart-mcp"
      }
    }
  }
}
```

### SSE Transport Configuration

<details>
<summary>Using SSE Instead of stdio</summary>

1. Start the server manually in a terminal:

```bash
python -m mcp_opendart --transport sse --port 9000 -vv
```

2. Configure your IDE to connect to the running server via its URL:

```json
{
  "mcpServers": {
    "mcp-opendart-sse": {
      "url": "http://localhost:9000/sse"
    }
  }
}
```
</details>

## Tools

### OpenDART Tools

- `ds001_disclosure`: Search and retrieve disclosure information
- `ds002_periodic`: Access periodic reports (annual, quarterly)
- `ds003_financial`: Get detailed financial information
- `ds004_ownership`: Access ownership disclosure information
- `ds005_major`: Retrieve major business reports
- `ds006_securities`: Access securities filing information

<details>
<summary>View All Tools</summary>

|Category|Tools|
|---|---|
|**Disclosure Information**|`get_company_info`, `search_disclosure`|
|**Periodic Reports**|`get_annual_report`, `get_quarterly_report`|
|**Financial Information**|`get_financial_statement`, `get_consolidated_finance`|
|**Ownership Disclosure**|`get_major_shareholders`, `get_executive_holdings`|
|**Major Reports**|`get_major_reports`, `get_business_reports`|
|**Securities Filing**|`get_securities_filing`, `get_prospectus`|

</details>

## Troubleshooting & Debugging

### Common Issues

- **Authentication Failures**:
  - Check if your API key is valid
  - Verify your API key has the necessary permissions
  - Check if you've exceeded the API rate limit
- **Data Access Issues**:
  - Some data may require additional permissions
  - Certain data might have delayed access
- **Connection Problems**:
  - Verify your internet connection
  - Check if the OpenDART API service is available

### Debugging Tools

```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG

# View logs
tail -f opendart.log

# Test API connection
python -m mcp_opendart test-connection
```

## Security

- Never share your API key
- Keep .env files secure and private
- Use appropriate rate limiting
- Monitor your API usage

## Contributing

We welcome contributions! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. This is not an official OpenDART product. 