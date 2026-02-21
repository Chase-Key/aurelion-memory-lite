# AURELION Memory — MCP Server

The AURELION Memory MCP server exposes your local knowledge graph to any MCP-compatible AI client — Claude Desktop, VS Code Copilot Chat, or any client implementing the Model Context Protocol.

---

## Requirements

- Python 3.9+
- `pip install mcp` (Anthropic MCP SDK)
- `aurelion-memory-lite` installed

---

## Installation

```bash
# 1. Install the package
pip install aurelion-memory-lite

# 2. Install the MCP SDK
pip install mcp

# 3. Verify
python -m aurelion_memory_mcp --help
```

---

## Setup: Claude Desktop

Find your `claude_desktop_config.json`:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the server:
```json
{
  "mcpServers": {
    "aurelion-memory": {
      "command": "python",
      "args": ["-m", "aurelion_memory_mcp"],
      "env": {
        "AURELION_MEMORY_PATH": "/absolute/path/to/your/memory-store"
      }
    }
  }
}
```

Restart Claude Desktop. You should see the AURELION Memory tools available in the chat interface.

---

## Setup: VS Code Copilot Chat

Add to your VS Code `settings.json` (`Ctrl+Shift+P` → "Open User Settings (JSON)"):

```json
{
  "github.copilot.chat.mcp.servers": {
    "aurelion-memory": {
      "command": "python",
      "args": ["-m", "aurelion_memory_mcp"],
      "env": {
        "AURELION_MEMORY_PATH": "${workspaceFolder}"
      }
    }
  }
}
```

Use `${workspaceFolder}` if your memory store is your workspace root, or replace with an absolute path.

---

## Windows Paths

On Windows, use forward slashes or escape backslashes:
```json
"AURELION_MEMORY_PATH": "C:/Users/chase/my-memory-store"
```

Or with the Python executable path if `python` is not on PATH:
```json
{
  "command": "C:/Users/chase/.venv/Scripts/python.exe",
  "args": ["-m", "aurelion_memory_mcp"]
}
```

---

## Available Tools

Once the server is running, the AI has access to these tools:

| Tool | What It Does |
|------|-------------|
| `memory_search` | Full-text search, optionally scoped to a floor |
| `memory_read` | Read a specific document by path |
| `memory_write` | Write or update a document with floor assignment |
| `memory_floor` | List all documents on a specific floor |
| `memory_session` | Load handoff note + current goals to restore session context |

---

## Example Prompts

Once the MCP server is connected, use prompts like:

```
"Search my memory for anything about my promotion criteria."
"Read Floor_01_Foundation/career-master.md"
"Write the following to Floor_04_Action/sprint-2026-02.md: [content]"
"List everything on Floor 5."
"Load my session context — where did we leave off?"
```

---

## Troubleshooting

**Server not starting:**
```bash
# Check Python can find the package
python -c "from aurelion_memory_mcp import main; print('OK')"

# Check MCP SDK
python -c "import mcp; print(mcp.__version__)"
```

**AURELION_MEMORY_PATH error:**  
Make sure the path exists and contains at least one `Floor_0X_*` directory.

**"Unknown tool" response:**  
Restart the AI client to reload the tool list after any server changes.

---

## Architecture

```
aurelion_memory_mcp/
├── __init__.py         ← Package entry
├── __main__.py         ← python -m entry point
└── server.py           ← MCP server implementation
    ├── search_files()  ← Full-text floor-scoped search
    ├── read_document() ← File reader
    ├── write_document()← File writer with floor routing
    ├── list_floor()    ← Floor index
    └── load_session()  ← Handoff + goals loader
```

The server is pure stdlib + `mcp` SDK. No vector database, no embedding API, no cloud required. Everything lives in your local markdown files.

---

## Related

- [AURELION Memory Lite](../README.md) — Full documentation
- [AURELION Hub](https://github.com/chase-key/aurelion-hub) — Full ecosystem
- [MCP Specification](https://github.com/anthropics/mcp) — Model Context Protocol
