from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / ".opencode"


def test_config_is_strict_json_and_minimal() -> None:
    data = json.loads((ADAPTER / "opencode.json").read_text(encoding="utf-8"))
    assert data["$schema"] == "https://opencode.ai/config.json"
    assert data["skills"] == ["./skills"]
    assert data["instructions"] == [".opencode/instructions.md"]
    for key in (
        "model",
        "default_agent",
        "agents",
        "permissions",
        "mcp",
        "providers",
        "plugins",
    ):
        assert key not in data


def test_instructions_contract() -> None:
    text = (ADAPTER / "instructions.md").read_text(encoding="utf-8")
    for phrase in (
        ".claude-plugin/plugin.json",
        "CLAUDE_PLUGIN_ROOT",
        "CLAUDE_PLUGIN_DATA",
        "CLAUDE_SEO_DATA_DIR",
        "repository root",
        "./scripts/claude-seo",
        "CLAUDE.md",
        "CLAUDE_SKILL_DIR",
        "webfetch",
        "timeout",
        "doctor --json",
        "Windows",
        "py -3 scripts/runtime.py",
        "Build",
        'mode must be `"manual"`',
    ):
        assert phrase in text, phrase
    assert "/opt/" not in text
    assert "/Users/" not in text
    assert "export CLAUDE_PLUGIN_ROOT" not in text


def test_command_contract() -> None:
    text = (ADAPTER / "commands" / "seo.md").read_text(encoding="utf-8")
    assert "$ARGUMENTS" in text
    assert "skill" in text
    assert "repository root" in text
    assert "!`" not in text


def test_gitattributes_forces_lf() -> None:
    text = (ADAPTER / ".gitattributes").read_text(encoding="utf-8")
    assert "* text eol=lf" in text
