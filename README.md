# Deep Research Fact-Checker Skill for Autonomous Agents

[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-blue.svg)](https://modelcontextprotocol.io)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-brightgreen.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-zero-success.svg)](requirements.txt)

Critical safety and anti-hallucination engine for autonomous research agents. Cross-references extracted factual claims against multiple independent source documents, computing verification scores and identifying ungrounded claims.

## Capabilities
- **Multi-Source Corroboration**: Checks claims against multiple texts to ensure broad factual consensus.
- **Ungrounded Claim Detection**: Flags statements with low lexical overlap or zero citations.
- **Confidence Scoring**: Returns deterministic, normalized confidence metrics (0.0 to 1.0).

## MCP Server Integration
```bash
python mcp_server.py
```

### Available MCP Tools
- `verify_claim`: Evaluate claim veracity across a dictionary of source documents.
