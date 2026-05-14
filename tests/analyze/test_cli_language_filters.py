from refactoring_benchmark.cli.analyze import (
    filter_instances_by_languages,
    language_output_suffix,
    language_plot_title,
    normalize_languages,
)
from refactoring_benchmark.utils.models import InstanceRow


def _instance(language: str) -> InstanceRow:
    return InstanceRow(
        owner="owner",
        repo=f"repo-{language}",
        commit_hash="1234567890abcdef",
        golden_commit_hash="fedcba0987654321",
        category="basic",
        language=language,
    )


def test_normalize_languages_maps_aliases_and_sorts() -> None:
    assert normalize_languages(["ts", "python", "js", "cpp", "c++"]) == ["c", "javascript", "python"]


def test_filter_instances_by_languages_filters_to_requested_languages() -> None:
    instances = [_instance("python"), _instance("javascript"), _instance("go")]

    filtered = filter_instances_by_languages(instances, ["go", "python"])

    assert [instance.language for instance in filtered] == ["python", "go"]


def test_language_output_suffix_is_stable() -> None:
    assert language_output_suffix(["go", "javascript"]) == "_lang_go_javascript"
    assert language_output_suffix([]) == ""


def test_language_plot_title_uses_display_names() -> None:
    assert language_plot_title(["javascript"]) == "Language: JavaScript/TypeScript"
    assert language_plot_title(["c", "python"]) == "Languages: C/C++, Python"
