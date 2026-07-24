class MCPError(Exception):
    """
    Base exception for all MCP-related errors.
    """
    pass


class MCPConnectionError(MCPError):
    """
    Raised when the MCP server cannot be reached.
    """
    pass


class MCPTimeoutError(MCPError):
    """
    Raised when an MCP request times out.
    """
    pass


class MCPAuthenticationError(MCPError):
    """
    Raised when authentication with the MCP server fails.
    """
    pass


class MCPToolError(MCPError):
    """
    Raised when an MCP tool execution fails.
    """
    pass


class MCPResponseError(MCPError):
    """
    Raised when the MCP server returns an invalid response.
    """
    pass