#!/usr/bin/env python3
"""Create website-build handoff artifacts from a /career repository.

Usage:
  python3 scripts/build_handoff.py --root /career
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return fallback or {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback or {}


def slug_to_title(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def parse_backlog_high_priority(backlog_path: Path) -> list[str]:
    if not backlog_path.exists():
        return []

    items: list[str] = []
    for raw_line in backlog_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("- [ ]") and "priority: HIGH" in line.upper():
            items.append(line)
    return items


def collect_project_payloads(root: Path, featured_order: list[str]) -> list[dict[str, Any]]:
    projects_dir = root / "projects"
    if not projects_dir.exists():
        return []

    featured_set = set(featured_order)
    payload: list[dict[str, Any]] = []

    for project_dir in sorted([path for path in projects_dir.iterdir() if path.is_dir()]):
        slug = project_dir.name
        website = load_json(project_dir / "website.json", fallback={})
        structured = website.get("structured_fields") if isinstance(website.get("structured_fields"), dict) else {}
        display = website.get("display") if isinstance(website.get("display"), dict) else {}

        title = str(display.get("title") or slug_to_title(slug))
        summary = str(structured.get("public_summary") or "").strip()
        highlights = [item for item in structured.get("highlights", []) if isinstance(item, str)]
        outcomes = [item for item in structured.get("outcomes", []) if isinstance(item, str)]
        if not highlights:
            highlights = [item for item in structured.get("what_i_built", []) if isinstance(item, str)]
        if not outcomes:
            outcomes = [item for item in structured.get("impact_highlights", []) if isinstance(item, str)]

        has_placeholder = any(
            marker in (title + " " + summary).upper() for marker in ["NEEDS_CLARIFICATION", "MISSING"]
        )

        payload.append(
            {
                "slug": slug,
                "title": title,
                "bucket": "featured" if slug in featured_set else "archive",
                "timeline_display": str(display.get("timeline_display") or "hide"),
                "public_summary": summary,
                "highlights_count": len(highlights),
                "outcomes_count": len(outcomes),
                "ready_for_site": bool((summary or highlights or outcomes) and not has_placeholder),
            }
        )

    featured = [item for slug in featured_order for item in payload if item["slug"] == slug]
    remainder = [item for item in payload if item["slug"] not in featured_order]
    return featured + remainder


def build_handoff(root: Path) -> dict[str, Any]:
    career = load_json(root / "career.json", fallback={})
    display_name = str(career.get("name") or "The candidate").strip()
    publication = career.get("publication_preferences") if isinstance(career.get("publication_preferences"), dict) else {}
    style = career.get("portfolio_style_profile") if isinstance(career.get("portfolio_style_profile"), dict) else {}
    hints = career.get("site_build_hints") if isinstance(career.get("site_build_hints"), dict) else {}
    dimensions = career.get("assessment_dimensions") if isinstance(career.get("assessment_dimensions"), list) else []

    featured_order = [item for item in career.get("featured_projects", []) if isinstance(item, str)]
    projects = collect_project_payloads(root, featured_order)
    high_priority_backlog = parse_backlog_high_priority(root / "backlog_questions.md")
    enable_chatbot = bool(hints.get("enable_chatbot", False))
    enabled_dimensions = [
        str(item.get("id"))
        for item in dimensions
        if isinstance(item, dict) and bool(item.get("enabled")) and str(item.get("id", "")).strip()
    ]
    has_leadership_dimension = any(
        isinstance(item, dict)
        and str(item.get("id", "")).strip().lower() == "people_leadership"
        and bool(item.get("enabled"))
        for item in dimensions
    )

    navigation = ["about", "featured-projects"]
    if has_leadership_dimension:
        navigation.append("leadership")
    navigation.extend(["skills", "archive", "contact"])
    if enable_chatbot:
        navigation.append("chat")

    chat_requirements: dict[str, Any] | None = None
    if enable_chatbot:
        chat_requirements = {
            "strict_grounding": True,
            "fallback_text": "I don’t have enough evidence in my repository to answer that confidently,",
            "open_with_phrase": f"{display_name} is",
            "suggested_questions": [
                "Which projects best demonstrate this candidate's hands-on delivery style?",
                "How would you summarize this candidate's current focus for a recruiter?",
                "What is this candidate's strongest achievement and likely value for a team?",
            ],
        }

    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_root": str(root),
        "defaults": {
            "public_voice": str(publication.get("default_public_voice") or "first_person"),
            "anonymize_clients": bool(publication.get("anonymize_clients", True)),
            "show_evidence_on_site": bool(publication.get("show_evidence_on_site", False)),
            "show_project_dates": str(publication.get("show_project_dates") or "only_if_precise"),
        },
        "site_profile": {
            "tone": str(style.get("tone") or "professional"),
            "home_style": str(hints.get("home_style") or "portfolio_first"),
            "archive_strategy": str(hints.get("archive_strategy") or "separate_page"),
            "project_detail_layout": str(hints.get("project_detail_layout") or "highlights_outcomes"),
            "enable_chatbot": enable_chatbot,
            "chat_audience": str(hints.get("chat_audience") or ""),
        },
        "enabled_dimensions": enabled_dimensions,
        "navigation": navigation,
        "featured_project_order": featured_order,
        "projects": projects,
        "chat_requirements": chat_requirements,
        "public_safety_rules": [
            "No client names unless explicitly approved.",
            "Do not expose local file paths, private evidence links, or confidence/evidence metadata in public copy.",
            "If dates are incomplete, hide them.",
        ],
        "high_priority_backlog": high_priority_backlog,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Website Build Handoff")
    lines.append("")
    lines.append("## Defaults")
    defaults = payload.get("defaults", {})
    for key in ["public_voice", "anonymize_clients", "show_evidence_on_site", "show_project_dates"]:
        lines.append(f"- {key}: `{defaults.get(key)}`")

    lines.append("")
    lines.append("## Site Profile")
    profile = payload.get("site_profile", {})
    for key in ["tone", "home_style", "archive_strategy", "project_detail_layout", "enable_chatbot", "chat_audience"]:
        lines.append(f"- {key}: `{profile.get(key)}`")

    lines.append("")
    lines.append("## Enabled Dimensions")
    dimensions = payload.get("enabled_dimensions", [])
    if dimensions:
        for item in dimensions:
            lines.append(f"- `{item}`")
    else:
        lines.append("- technical_delivery (default)")

    lines.append("")
    lines.append("## Navigation")
    for item in payload.get("navigation", []):
        lines.append(f"- `{item}`")

    lines.append("")
    lines.append("## Featured Project Order")
    featured = payload.get("featured_project_order", [])
    if featured:
        for slug in featured:
            lines.append(f"- `{slug}`")
    else:
        lines.append("- NONE")

    lines.append("")
    lines.append("## Project Readiness")
    for project in payload.get("projects", []):
        lines.append(
            f"- `{project['slug']}` ({project['bucket']}): "
            f"summary={bool(project['public_summary'])}, "
            f"highlights={project['highlights_count']}, outcomes={project['outcomes_count']}, "
            f"timeline_display={project['timeline_display']}, ready={project['ready_for_site']}"
        )

    lines.append("")
    lines.append("## Public Safety Rules")
    for rule in payload.get("public_safety_rules", []):
        lines.append(f"- {rule}")

    chat = payload.get("chat_requirements")
    lines.append("")
    lines.append("## Chat Requirements")
    if chat:
        lines.append(f"- strict_grounding: `{chat.get('strict_grounding')}`")
        lines.append(f"- fallback_text: `{chat.get('fallback_text')}`")
        lines.append(f"- open_with_phrase: `{chat.get('open_with_phrase')}`")
    else:
        lines.append("- chatbot disabled")

    lines.append("")
    lines.append("## High Priority Backlog")
    backlog = payload.get("high_priority_backlog", [])
    if backlog:
        for item in backlog:
            lines.append(f"- {item}")
    else:
        lines.append("- NONE")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate build handoff artifacts from /career.")
    parser.add_argument("--root", required=True, help="Path to /career")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        raise SystemExit(f"Missing root path: {root}")

    handoff = build_handoff(root)
    out_dir = root / "public_site"
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "website_handoff.json"
    md_path = out_dir / "website_handoff.md"

    json_path.write_text(json.dumps(handoff, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(handoff), encoding="utf-8")

    print(f"Wrote: {json_path}")
    print(f"Wrote: {md_path}")


if __name__ == "__main__":
    main()
