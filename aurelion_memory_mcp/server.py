"""
AURELION Memory MCP Server
Exposes the aurelion-memory-lite knowledge graph to MCP-compatible AI clients.

Usage:
    python -m aurelion_memory_mcp

Environment:
    AURELION_MEMORY_PATH  - Root path of your memory store (required)

Compatible with:
    - Claude Desktop
    - VS Code Copilot Chat (MCP mode)
    - Any MCP stdio-compatible client
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

# MCP SDK — install with: pip install mcp
try:
    import mcp.server.stdio
    import mcp.types as types
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

# AURELION Memory library
try:
    from aurelion_memory_lite import LibrarySystem
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False


# ─── Constants ────────────────────────────────────────────────────────────────

FLOOR_NAMES = {
    1: "Foundation",
    2: "Systems",
    3: "Networks",
    4: "Action",
    5: "Vision",
}

FLOOR_DIRS = {
    1: "Floor_01_Foundation",
    2: "Floor_02_Systems",
    3: "Floor_03_Networks",
    4: "Floor_04_Action",
    5: "Floor_05_Vision",
}


# ─── Memory Store ─────────────────────────────────────────────────────────────

def get_memory_path() -> Path:
    """Resolve the memory store root from environment."""
    raw = os.environ.get("AURELION_MEMORY_PATH", "")
    if not raw:
        raise EnvironmentError(
            "AURELION_MEMORY_PATH is not set. "
            "Set it to the root of your AURELION memory store directory."
        )
    p = Path(raw).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"AURELION_MEMORY_PATH does not exist: {p}")
    return p


def search_files(memory_path: Path, query: str, floor: int | None = None) -> list[dict]:
    """Full-text search across markdown files in the memory store."""
    results = []
    query_lower = query.lower()

    search_dirs = []
    if floor is not None:
        dir_name = FLOOR_DIRS.get(floor)
        if dir_name:
            d = memory_path / dir_name
            if d.exists():
                search_dirs.append((floor, d))
    else:
        for f_num, dir_name in FLOOR_DIRS.items():
            d = memory_path / dir_name
            if d.exists():
                search_dirs.append((f_num, d))

    for f_num, d in search_dirs:
        for md_file in d.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                if query_lower in content.lower():
                    # Extract first matching line as snippet
                    snippet = ""
                    for line in content.splitlines():
                        if query_lower in line.lower():
                            snippet = line.strip()[:200]
                            break
                    results.append({
                        "path": str(md_file.relative_to(memory_path)),
                        "floor": f_num,
                        "floor_name": FLOOR_NAMES[f_num],
                        "snippet": snippet,
                    })
            except Exception:
                continue

    return results


def read_document(memory_path: Path, doc_path: str) -> dict:
    """Read a specific document from the memory store."""
    full_path = memory_path / doc_path
    if not full_path.exists():
        return {"error": f"Document not found: {doc_path}"}
    try:
        content = full_path.read_text(encoding="utf-8", errors="ignore")
        return {
            "path": doc_path,
            "content": content,
            "size_chars": len(content),
            "lines": content.count("\n") + 1,
        }
    except Exception as e:
        return {"error": str(e)}


def write_document(memory_path: Path, doc_path: str, content: str, floor: int) -> dict:
    """Write or update a document in the memory store."""
    dir_name = FLOOR_DIRS.get(floor)
    if not dir_name:
        return {"error": f"Invalid floor number: {floor}. Use 1–5."}

    # Ensure path is under the correct floor directory
    if not doc_path.startswith(dir_name):
        doc_path = f"{dir_name}/{doc_path.lstrip('/')}"

    full_path = memory_path / doc_path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        full_path.write_text(content, encoding="utf-8")
        return {
            "written": doc_path,
            "floor": floor,
            "floor_name": FLOOR_NAMES[floor],
            "size_chars": len(content),
        }
    except Exception as e:
        return {"error": str(e)}


def list_floor(memory_path: Path, floor: int) -> dict:
    """List all documents on a given floor."""
    dir_name = FLOOR_DIRS.get(floor)
    if not dir_name:
        return {"error": f"Invalid floor: {floor}"}
    d = memory_path / dir_name
    if not d.exists():
        return {"floor": floor, "floor_name": FLOOR_NAMES[floor], "documents": [], "note": "Floor directory does not exist yet"}
    docs = [str(f.relative_to(memory_path)) for f in d.rglob("*.md")]
    return {
        "floor": floor,
        "floor_name": FLOOR_NAMES[floor],
        "document_count": len(docs),
        "documents": sorted(docs),
    }


def load_session_context(memory_path: Path) -> dict:
    """Load active session context: handoff note + current Floor 5 goals."""
    context = {"handoff": None, "goals": [], "active_projects": []}

    # Load latest handoff from Floor 4
    f4 = memory_path / FLOOR_DIRS[4]
    if f4.exists():
        handoffs = sorted(f4.glob("*handoff*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        sessions = sorted(f4.glob("*session*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        candidates = handoffs or sessions
        if candidates:
            try:
                content = candidates[0].read_text(encoding="utf-8", errors="ignore")
                context["handoff"] = {
                    "path": str(candidates[0].relative_to(memory_path)),
                    "preview": content[:800],
                }
            except Exception:
                pass

    # Load goal files from Floor 5
    f5 = memory_path / FLOOR_DIRS[5]
    if f5.exists():
        for goal_file in sorted(f5.glob("*.md"))[:5]:
            try:
                content = goal_file.read_text(encoding="utf-8", errors="ignore")
                first_lines = "\n".join(content.splitlines()[:6])
                context["goals"].append({
                    "path": str(goal_file.relative_to(memory_path)),
                    "preview": first_lines,
                })
            except Exception:
                continue

    return context


# ─── MCP Server Definition ────────────────────────────────────────────────────

def build_server() -> "Server":
    server = Server("aurelion-memory")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="memory_search",
                description=(
                    "Search the AURELION memory store for documents matching a query. "
                    "Optionally scope to a specific floor (1=Foundation, 2=Systems, "
                    "3=Networks, 4=Action, 5=Vision)."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search terms"},
                        "floor": {
                            "type": "integer",
                            "description": "Floor 1–5 to scope search. Omit for all floors.",
                            "minimum": 1,
                            "maximum": 5,
                        },
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="memory_read",
                description="Read the full content of a specific document in the memory store.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative path to the document, e.g. Floor_01_Foundation/career-master.md",
                        }
                    },
                    "required": ["path"],
                },
            ),
            types.Tool(
                name="memory_write",
                description=(
                    "Write or update a document in the memory store. "
                    "Provide the floor number to place it in the correct directory."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File name or relative path"},
                        "content": {"type": "string", "description": "Full document content (markdown)"},
                        "floor": {
                            "type": "integer",
                            "description": "Floor 1–5 to store this document",
                            "minimum": 1,
                            "maximum": 5,
                        },
                    },
                    "required": ["path", "content", "floor"],
                },
            ),
            types.Tool(
                name="memory_floor",
                description="List all documents stored on a specific floor of the knowledge graph.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "floor": {
                            "type": "integer",
                            "description": "Floor number (1=Foundation, 2=Systems, 3=Networks, 4=Action, 5=Vision)",
                            "minimum": 1,
                            "maximum": 5,
                        }
                    },
                    "required": ["floor"],
                },
            ),
            types.Tool(
                name="memory_session",
                description=(
                    "Load the active session context: most recent handoff note from Floor 4 "
                    "and current goals from Floor 5. Use at the start of a session to restore context."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
        memory_path = get_memory_path()

        if name == "memory_search":
            query = arguments["query"]
            floor = arguments.get("floor")
            results = search_files(memory_path, query, floor)
            return [types.TextContent(
                type="text",
                text=json.dumps(results, indent=2) if results else f'No documents found matching "{query}".',
            )]

        elif name == "memory_read":
            result = read_document(memory_path, arguments["path"])
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "memory_write":
            result = write_document(
                memory_path,
                arguments["path"],
                arguments["content"],
                arguments["floor"],
            )
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "memory_floor":
            result = list_floor(memory_path, arguments["floor"])
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "memory_session":
            result = load_session_context(memory_path)
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    return server


# ─── Entry Point ──────────────────────────────────────────────────────────────

async def main() -> None:
    if not MCP_AVAILABLE:
        print(
            "ERROR: MCP SDK not installed. Run: pip install mcp",
            file=sys.stderr,
        )
        sys.exit(1)

    server = build_server()
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="aurelion-memory",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
