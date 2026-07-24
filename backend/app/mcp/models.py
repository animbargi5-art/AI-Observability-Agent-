from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MCPRequest:
    tool: str
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MCPResponse:
    success: bool
    result: Any = None
    error: Optional[str] = None


@dataclass
class ToolCall:
    tool: str
    arguments: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    tool: str
    success: bool
    data: Any = None
    error: Optional[str] = None