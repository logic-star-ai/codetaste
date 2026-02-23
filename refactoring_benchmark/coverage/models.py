from typing import List, Optional, Set

from pydantic import BaseModel, ConfigDict, Field


# Line
class Line(BaseModel):
    """Represents a single line in a commit."""

    uri: str  # File path
    commit: str  # Commit hash
    line_number: int  # Line number in the file
    content: Optional[str] = None  # The actual line content

    def __hash__(self):
        """Make Line hashable for use in sets (excludes commit and content)."""
        return hash((self.uri, self.line_number, self.commit))

    def __eq__(self, other):
        """Compare Lines for equality (excludes commit and content)."""
        if not isinstance(other, Line):
            return False
        return self.uri == other.uri and self.line_number == other.line_number and self.commit == other.commit


# Opengrep
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
    model_config = ConfigDict(extra="allow")

    ruleId: Optional[str] = None
    message: Optional[dict] = None
    locations: Optional[List[dict]] = Field(default_factory=list)


class SARIFRun(BaseModel):
    model_config = ConfigDict(extra="allow")

    invocations: Optional[List[SARIFInvocation]] = Field(default_factory=list)
    results: Optional[List[SARIFResult]] = Field(default_factory=list)
    tool: Optional[dict] = None


class SARIFOpengrep(BaseModel):
    model_config = ConfigDict(extra="ignore")

    schema_: Optional[str] = Field(None, alias="$schema")
    version: str
    runs: List[SARIFRun]


# Precision Metrics
class PrecisionInput(BaseModel):
    sarif_addition_rules_path: Optional[str] = Field(
        None, description="Path to SARIF file with addition rules on **Post**-Refactoring codebase."
    )
    sarif_removal_rules_path: Optional[str] = Field(
        None, description="Path to SARIF file with negative findings on **Pre**-Refactoring codebase."
    )
    prediction_diff_path: Optional[str] = Field(
        None, description="Path to the diff file between **Pre**-Refactoring and **Post**-Refactoring codebases."
    )


class PrecisionMetrics(BaseModel):
    """Line-level precision metrics for refactoring changes.

    Measures what fraction of changed lines (additions/removals) are relevant
    according to SARIF rules. Complements rule-level IFR metrics.

    Note: lines_added and lines_removed are disjoint (different commits: base vs predicted).
    """

    lines_added: Set[Line] = Field(
        default_factory=set, description="Set of lines that were added (+) by the prediction.diff."
    )
    lines_removed: Set[Line] = Field(
        default_factory=set, description="Set of lines that were removed (-) by the prediction.diff."
    )
    lines_matched_by_addition_rules: Set[Line] = Field(
        default_factory=set,
        description="Set of lines in Post-Refactoring codebase that are matched by findings in the SARIF Report with addition rules.",
    )
    lines_matched_by_removal_rules: Set[Line] = Field(
        default_factory=set,
        description="Set of lines in Pre-Refactoring codebase that are matched by findings in the SARIF Report with removal rules.",
    )

    @property
    def relevant_added_lines(self) -> Set[Line]:
        """Set of lines that were added (+) by the prediction.diff and are matched by findings in the SARIF Report on Post-Refactoring codebase."""
        if not self.lines_added or not self.lines_matched_by_addition_rules:
            return set()
        assert (
            list(self.lines_added)[0].commit == list(self.lines_matched_by_addition_rules)[0].commit
        ), "Commits of added lines and matched addition rules do not match."
        return self.lines_added & self.lines_matched_by_addition_rules

    @property
    def relevant_removed_lines(self) -> Set[Line]:
        """Set of lines that were removed (-) by the prediction.diff and are matched by findings in the SARIF Report on Pre-Refactoring codebase."""
        if not self.lines_removed or not self.lines_matched_by_removal_rules:
            return set()
        assert (
            list(self.lines_removed)[0].commit == list(self.lines_matched_by_removal_rules)[0].commit
        ), "Commits of removed lines and matched removal rules do not match."
        return self.lines_removed & self.lines_matched_by_removal_rules

    @property
    def precision_added(self) -> float:
        """Precision of additions: What fraction of added lines are relevant according to the addition rules.

        Of all new lines the agent added, how many match the 'good' patterns we expected?
        """
        if not self.lines_added:
            return 0.0
        return len(self.relevant_added_lines) / len(self.lines_added)

    @property
    def precision_removed(self) -> float:
        """Precision of deletions: What fraction of removed lines are relevant according to the removal rules.

        Of all lines the agent decided to delete, how many were actually 'bad' code?
        """
        if not self.lines_removed:
            return 0.0
        return len(self.relevant_removed_lines) / len(self.lines_removed)

    @property
    def precision_overall(self) -> float:
        """Overall precision: What fraction of all changed lines (additions + removals) are relevant according to rules.

        Combined metric across both additions and removals.
        Note: lines_added and lines_removed are disjoint (different commits: base vs predicted).
        """
        total_lines = len(self.lines_added) + len(self.lines_removed)
        if total_lines == 0:
            return 0.0
        total_relevant = len(self.relevant_added_lines) + len(self.relevant_removed_lines)
        return total_relevant / total_lines


class PrecisionMetricsResult(BaseModel):
    """Computed precision metrics without storing full line sets.

    Optimized for caching - stores only scalar values, not full Line objects.
    """

    precision_added: float = Field(description="Precision of additions (0-1)")
    precision_removed: float = Field(description="Precision of removals (0-1)")
    precision_overall: float = Field(description="Overall precision (0-1)")

    # Counts for context/debugging
    lines_added_count: int = Field(description="Total lines added")
    lines_removed_count: int = Field(description="Total lines removed")
    relevant_added_count: int = Field(description="Relevant lines added")
    relevant_removed_count: int = Field(description="Relevant lines removed")


class PrecisionResult(BaseModel):
    precision_input: PrecisionInput
    precision_metrics: PrecisionMetrics


class InstanceAgentPrecision(BaseModel):
    """Precision metrics summary for a single instance-agent pair.

    Used for aggregating and reporting results across multiple instances.
    """

    instance: str = Field(description="Instance display path (e.g., 'apache/arrow/e434536e')")
    agent: str = Field(description="Agent name")
    metrics: PrecisionMetricsResult = Field(description="Precision metrics for this instance-agent pair")
