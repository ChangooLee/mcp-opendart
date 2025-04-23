import sys
import asyncio
from mcp_opendart.server import run_server

if __name__ == "__main__":
    sys.exit(asyncio.run(run_server())) 