# AURELION Memory (Lite Edition)

> **Part of the AURELION Ecosystem**  
> **Built on AAI:** Autonomous Agentic AI Framework

A 5-floor library-based memory management system for organizing personal knowledge with graph-based relationships. Works in conjunction with the AURELION Kernel to provide complete cognitive architecture.

**AURELION** = **A**utonomous **U**niversal **R**easoning **E**ngine with **L**ong-term **I**ntelligence, **O**perational Memory & **N**eural Nexus

**AAI** = **A**utonomous **A**gentic **A**I

---

## 🏗️ Project Status

**Status:** ✅ Production (v1.0.0)  
**Released:** February 17, 2026  
**License:** MIT

AURELION Memory Lite is production-ready for personal knowledge management. We're building in the open and would love your feedback!

**Current Features:**
- ✅ Core 5-floor architecture (Foundation, Systems, Networks, Action, Vision)
- ✅ Knowledge graph with automatic relationship detection
- ✅ Python API and CLI tools
- ✅ Markdown-based content management
- ✅ File-based storage (no external dependencies)

**Roadmap:**

**Community Expansion (Lite Tier):**
- Auto-tagging scripts for markdown files
- Export/import utilities (JSON, CSV, other knowledge bases)
- Query optimization examples and patterns
- Integration examples with popular note-taking tools

**Premium Features (Open Source - Q3 2026):**
- 📋 Semantic search with vector embeddings
- 📋 Visualization tools and timeline views
- 📋 Advanced graph traversal algorithms

*Premium = MIT licensed code requiring paid infrastructure (vector DBs, APIs)*

**Business Features (BSL Licensed - 2027+):**
- 📋 Multi-tenant architecture
- 📋 Enterprise RBAC and audit logs
- 📋 Production monitoring and caching

*Business = Source available (BSL), multi-user/team features*

💬 **Have feedback or ideas?** Share with the ecosystem maintainers!

---

## 🚀 Quick Start

```bash
pip install aurelion-memory-lite
aurelion-memory-lite init my-knowledge-base
cd my-knowledge-base
aurelion-memory-lite serve
```

## 🎯 Features

- **5-Floor Architecture**: Organize knowledge across Foundation, Systems, Networks, Action, and Vision
- **Knowledge Graph**: Automatic relationship detection between documents
- **Markdown-Based**: Works with any text editor
- **Python API**: Programmatic access to your knowledge base
- **CLI Tools**: Quick operations from command line

## 📖 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - Understanding the 5-floor system and AAI principles
- [Floor Mapping](docs/FLOOR_MAPPING.md) - What goes on each floor
- [Build Process](docs/BUILD_PROCESS.md) - How the system is built
- [Examples](examples/) - Usage examples

**Get Started:**
1. Use [aurelion-kernel-lite](../../kernel/aurelion-kernel-lite/) for content templates
2. Install this memory module to power the system: `pip install -e .`
3. Use together for complete cognitive architecture

## 🔗 AURELION Ecosystem

This Memory module is part of the larger AURELION Ecosystem:

- **[aurelion-memory-lite](../aurelion-memory-lite/)** (this module) - File-based knowledge graph
- **[aurelion-kernel-lite](../../kernel/aurelion-kernel-lite/)** - Cognitive structure templates
- **[aurelion-nexus](../../nexus/aurelion-nexus/)** - World engine & agent system
- **[aurelion-sim](../../sim/aurelion-sim/)** - Simulation framework

**See the [AURELION Hub](https://github.com/chase-key/aurelion-hub) for complete ecosystem overview and integration guides.**

## 📦 Installation

```bash
pip install aurelion-memory-lite
```

## 🛠️ Usage

```python
from aurelion_memory_lite import LibrarySystem, Architecture

# Initialize the architecture
arch = Architecture()
print(arch.get_all_floors())

# Create a library system
library = LibrarySystem()
```

## 🤝 Contributing

Contributions welcome! This is the knowledge management engine that powers personal knowledge systems.

**Ways to contribute:**
- 🐛 Report bugs or suggest features via [Issues](../../issues)
- 💬 Share your use case in [Discussions](../../discussions)
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repo if you find it useful!

## 💡 Philosophy: AAI Framework

**Autonomous Agentic AI (AAI)** is our approach to personal knowledge management:

- **Autonomous:** Self-organizing systems that maintain structure automatically
- **Agentic:** AI systems that can act on your behalf with your knowledge
- **AI Framework:** Architecture designed for intelligent agents and LLM integration

AAI emphasizes spatial organization (5-floor library), graph-based relationships, and agent-ready structure.

## 🗺️ AURELION Ecosystem

**AURELION** is a suite of modular AI systems designed to work together:

- **AURELION Memory-Lite** (this repo): Memory management system (the engine)
- **[AURELION Kernel-Lite](https://github.com/chase-key/aurelion-kernel-lite)**: Cognitive Kernel (the content structure)
- **AURELION-N**: Neural Nexus for autonomous agents (coming soon)

**AURELION Memory-Lite + AURELION Kernel-Lite work together:**
- AURELION Kernel-Lite provides the template structure (5 floors, career docs, skills inventory)
- AURELION Memory-Lite provides the Python engine (knowledge graph, cross-referencing, API)
- Together they form a complete personal knowledge system

**Recommended Usage:**
1. Clone [AURELION Kernel-Lite](https://github.com/chase-key/aurelion-kernel-lite) for your content structure
2. Install AURELION Memory-Lite to power the knowledge graph and API
3. Use both together for a complete system

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

Free to use for personal and commercial projects. We believe in open source!

## 🏢 About

AURELION Memory-Lite is developed by Chase (chase-key) as part of the AURELION ecosystem.

**Contributors:**
- **Chase (chase-key)** - Creator & Primary Developer
- **z3rosl33p** - Documentation & Release Engineering

**Interested in enterprise features or support?** Reach out via [Discussions](../../discussions).

---

**Need templates to get started?** Check out [aurelion-k](https://github.com/chase-key/aurelion-k) for ready-to-use Cognitive Kernel templates.
