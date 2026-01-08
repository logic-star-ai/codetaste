from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class Line(BaseModel):
    """Represents a single line in a commit."""

    uri: str  # File path
    commit: str  # Commit hash
    line_number: int  # Line number in the file
    content: Optional[str] = None  # The actual line content

    def __hash__(self):
        """Make Line hashable for use in sets (excludes commit and content)."""
        return hash((self.uri, self.line_number))

    def __eq__(self, other):
        """Compare Lines for equality (excludes commit and content)."""
        if not isinstance(other, Line):
            return False
        return (
            self.uri == other.uri
            and self.line_number == other.line_number
        )
    
# OPENGREP SARIF MODEL


class SARIFMessage(BaseModel):
    text: str

class SARIFDescriptor(BaseModel):
    id: str

class SARIFToolExecutionNotification(BaseModel):
    descriptor: SARIFDescriptor
    level: str
    message: SARIFMessage

class SARIFInvocation(BaseModel):
    executionSuccessful: bool
    toolExecutionNotifications: Optional[List[SARIFToolExecutionNotification]] = Field(default_factory=list)

class SARIFResult(BaseModel):
    model_config = ConfigDict(extra='allow')

    ruleId: Optional[str] = None
    message: Optional[dict] = None
    locations: Optional[List[dict]] = Field(default_factory=list)

class SARIFRun(BaseModel):
    model_config = ConfigDict(extra='allow')

    invocations: Optional[List[SARIFInvocation]] = Field(default_factory=list)
    results: Optional[List[SARIFResult]] = Field(default_factory=list)
    tool: Optional[dict] = None

class SARIFOpengrep(BaseModel):
    model_config = ConfigDict(extra='ignore')

    schema_: Optional[str] = Field(None, alias='$schema')
    version: str
    runs: List[SARIFRun]