[한국어](README.md) | English

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
| **Disclosure Information** | ✅ Fully supported | Company information and disclosure document search |
| **Periodic Report Key Information** | ✅ Fully supported | Key information from annual, quarterly, and semi-annual reports |
| **Periodic Report Financial Information** | ✅ Fully supported | Financial statements and XBRL data |
| **Comprehensive Share Ownership Information** | ✅ Fully supported | Major shareholders and executive holdings information |
| **Major Report Key Information** | ✅ Fully supported | Key information from major business reports |
| **Securities Filing Key Information** | ✅ Fully supported | Key information from securities issuance filings |

## Quick Start Guide

### 1. Authentication Setup

First, obtain your OpenDART API key:

1. Go to [OpenDART](https://opendart.fss.or.kr/)
2. Sign up and request an API key
3. Wait for approval and receive your API key

### 2. Installation

```bash
# Clone repository
git clone https://github.com/ChangooLee/mcp-opendart.git
cd mcp-opendart

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

```

## IDE Integration

MCP OpenDART is designed to be used with AI assistants through IDE integration.

### Claude Desktop Configuration

1. Click hamburger menu (☰) > Settings > Developer > "Edit Config" button
2. Add the following configuration:

```json
{
  "mcpServers": {
    "mcp-opendart": {
      "command": "YOUR_LOCATION/.venv/bin/mcp-opendart",
      "env": {
        "OPENDART_API_KEY": "API-KEY",
        "OPENDART_BASE_URL": "https://opendart.fss.or.kr/api/",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "TRANSPORT": "stdio",
        "LOG_LEVEL": "INFO",
        "MCP_SERVER_NAME": "mcp-opendart"
      }
    }
  }
}
```

> [!NOTE]
> - `YOUR_LOCATION`: Replace with the actual path where your virtual environment is installed
> - `API-KEY`: Replace with your OpenDART API key

### Environment Variables

- `OPENDART_API_KEY`: Your OpenDART API key
- `OPENDART_BASE_URL`: API base URL (defaults to official URL)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `TRANSPORT`: Transport method (stdio recommended)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `MCP_SERVER_NAME`: Server name

## Tools

### OpenDART Tools

- `ds001_disclosure`: Search and retrieve disclosure information
- `ds002_periodic`: Access periodic report key information
- `ds003_financial`: Access periodic report financial information
- `ds004_ownership`: Access comprehensive share ownership information
- `ds005_major`: Access major report key information
- `ds006_securities`: Access securities filing key information

<details>
<summary>Main Tools List</summary>

| Category | Tools |
|----------|-------|
| **Disclosure Information** | `get_corporation_code_by_name`, `get_disclosure_list`, `get_corporation_info`, `get_disclosure_document`, `get_corporation_code` |
| **Periodic Report Key Information** | `get_annual_report`, `get_quarterly_report`, `get_semi_annual_report` |
| **Periodic Report Financial Information** | `get_single_acnt`, `get_multi_acnt`, `get_xbrl_file`, `get_single_acc`, `get_xbrl_taxonomy`, `get_single_index`, `get_multi_index` |
| **Comprehensive Share Ownership Information** | `get_major_shareholders`, `get_executive_holdings` |
| **Major Report Key Information** | `get_major_reports`, `get_business_reports` |
| **Securities Filing Key Information** | `get_securities_filing`, `get_prospectus` |

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

This project is licensed under the [MIT License](LICENSE).

This is not an official OpenDART product. OpenDART is a registered trademark of the Financial Supervisory Service of Korea. 