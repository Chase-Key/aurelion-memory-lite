"""Entry point for python -m aurelion_memory_mcp"""
import asyncio
from .server import main

asyncio.run(main())
