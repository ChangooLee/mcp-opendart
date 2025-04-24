# MCP OpenDART

![License](https://img.shields.io/github/license/ChangooLee/mcp-opendart)
![PyPI Version](https://img.shields.io/pypi/v/mcp-opendart)
![PyPI Downloads](https://img.shields.io/pypi/dm/mcp-opendart)

Model Context Protocol (MCP) server for OpenDART (Korea Financial Supervisory Service's Data Analysis, Retrieval and Transfer System). This integration enables secure, contextual AI interactions with OpenDART while maintaining data privacy and security.

## Example Usage

Ask your AI assistant to:

- **📊 Financial Reports** - "Get the latest quarterly report for Samsung Electronics"
- **🔍 Disclosure Search** - "Find major shareholding changes in KOSPI companies last month"
- **📈 Corporate Analysis** - "Show me the financial statements of Hyundai Motor for the past 3 years"
- **⚡ Real-time Updates** - "Get today's important disclosures for technology sector"

### Feature Demo

[Demo video will be added here]

### Compatibility

| Feature | Support Status | Description |
|---------|---------------|-------------|
| **Disclosure Information** | ✅ Fully supported | Company information, disclosure documents |
| **Periodic Reports** | ✅ Fully supported | Annual, quarterly, semi-annual reports |
| **Financial Information** | ✅ Fully supported | Financial statements, XBRL data |
| **Ownership Disclosure** | ✅ Fully supported | Major shareholders, executive holdings |
| **Major Reports** | ✅ Fully supported | Business reports, significant events |
| **Securities Filing** | ✅ Fully supported | Securities issuance, prospectus |

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

# Install from PyPI
pip install mcp-opendart

# Or install in development mode
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

### Configuration Methods

There are two main approaches to configure the server:

1. **Environment Variables in Config** (recommended)
2. **Using Environment File** (alternative)

Note: Common environment variables include:
- `OPENDART_API_KEY`: Your OpenDART API key
- `OPENDART_BASE_URL`: API base URL (defaults to official URL)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `MCP_SERVER_NAME`: Custom server name
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

### Configuration Examples

**Method 1 (Environment Variables in Config):**

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
        "MCP_SERVER_NAME": "mcp-opendart"
      }
    }
  }
}
```

<details>
<summary>Method 2: Using Environment File</summary>

1. Create a `.env` file:
```bash
OPENDART_API_KEY=your_api_key_here
OPENDART_BASE_URL=https://opendart.fss.or.kr/api/
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
MCP_SERVER_NAME=mcp-opendart
```

2. Update your configuration:
```json
{
  "mcpServers": {
    "mcp-opendart": {
      "command": "python",
      "args": ["-m", "mcp_opendart", "--env-file", "/path/to/your/.env"]
    }
  }
}
```
</details>

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
<summary>View Tools</summary>

| Category | Tools |
|----------|-------|
| **Disclosure Information** | `get_corporation_code_by_name`, `get_disclosure_list`, `get_corporation_info`, `get_disclosure_document`, `get_corporation_code` |
| **Periodic Reports** | `get_annual_report`, `get_quarterly_report`, `get_semi_annual_report` |
| **Financial Information** | `get_single_acnt`, `get_multi_acnt`, `get_xbrl_file`, `get_single_acc`, `get_xbrl_taxonomy`, `get_single_index`, `get_multi_index` |
| **Ownership Disclosure** | `get_major_shareholders`, `get_executive_holdings` |
| **Major Reports** | `get_major_reports`, `get_business_reports` |
| **Securities Filing** | `get_securities_filing`, `get_prospectus` |

</details>

## Troubleshooting & Debugging

### Common Issues

- **Authentication Failures**:
  - Check if your API key is valid and active
  - Verify your API key has the necessary permissions
  - Check if you've exceeded the API rate limit (20,000 calls/day)

- **Data Access Issues**:
  - Some data may require additional permissions
  - Certain data might have delayed access (up to 24 hours)
  - Check if the company is within your accessible range

- **Connection Problems**:
  - Verify your internet connection
  - Check if the OpenDART API service is available
  - Ensure your firewall isn't blocking the connection

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
- Keep `.env` files secure and private
- Use appropriate rate limiting
- Monitor your API usage
- Store sensitive data in environment variables

## Contributing

We welcome contributions! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This is not an official OpenDART product. OpenDART is a registered trademark of the Financial Supervisory Service of Korea. 