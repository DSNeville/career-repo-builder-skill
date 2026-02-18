#!/usr/bin/env python3
"""Export sanitized, publish-safe payloads from a /career repository.

Usage:
  python3 scripts/publish_safe_export.py --root /career --voice first_person
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_VOICE = "first_person"
DEFAULT_NAME = "JP Neville"
PRIVATE_LINE_PATTERNS = [
    re.compile(r"NEEDS_CLARIFICATION", re.IGNORECASE),
    re.compile(r"PRIVATE_UNSHARED", re.IGNORECASE),
    re.compile(r"PRIVATE/UNSHARED", re.IGNORECASE),
    re.compile(r"^\s*MISSING\b", re.IGNORECASE),
    re.compile(r"/Users/", re.IGNORECASE),
]

PUBLISH_METADATA_PATTERNS = [
    re.compile(r"\s*\(Confidence:.*$", re.IGNORECASE),
    re.compile(r"\s*\(Evidence:.*$", re.IGNORECASE),
    re.compile(r"\s*\(publication-safe phrasing approved\)", re.IGNORECASE),
]

PUBLIC_SECTION_DEFAULTS = {
    "context": "public",
    "what_i_built": "public",
    "impact": "public",
    "constraints_tradeoffs": "public",
    "team_collaboration": "public",
    "leadership_delivery": "public",
    "role_relevance": "public",
    "evidence": "private",
    "notes_lessons": "public",
}


def section_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def is_public_line(value: str) -> bool:
    line = value.strip()
    if not line:
        return False
    return not any(pattern.search(line) for pattern in PRIVATE_LINE_PATTERNS)


def strip_publish_metadata(value: str) -> str:
    text = value
    for pattern in PUBLISH_METADATA_PATTERNS:
        text = pattern.sub("", text)
    return text.strip()


def sanitize_text(value: str) -> str:
    lines = [strip_publish_metadata(line.strip()) for line in value.splitlines()]
    kept = [line for line in lines if is_public_line(line)]
    return "\n".join(kept).strip()


def sanitize_list(values: list[str]) -> list[str]:
    cleaned = [strip_publish_metadata(item.strip()) for item in values]
    return [item for item in cleaned if is_public_line(item)]


def load_json(path: Path, fallback: dict[str, Any] | None = None) -> dict[str, Any]:
    if not path.exists():
        return fallback or {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback or {}


def strip_frontmatter(markdown: str) -> str:
    if not markdown.startswith("---\n"):
        return markdown

    end = markdown.find("\n---\n", 4)
    if end == -1:
        return markdown

    return markdown[end + 5 :]


def parse_project_markdown(markdown: str) -> dict[str, Any]:
    clean_markdown = strip_frontmatter(markdown.replace("\r\n", "\n")).strip()
    title_match = re.search(r"^#\s+(.+)$", clean_markdown, flags=re.MULTILINE)

    first_section_match = re.search(r"^##\s+", clean_markdown, flags=re.MULTILINE)
    preface = clean_markdown[: first_section_match.start()] if first_section_match else clean_markdown

    def extract_meta(label: str) -> str:
        pattern = re.compile(rf"\*\*{re.escape(label)}:\*\*\s*(.+)")
        match = pattern.search(preface)
        return match.group(1).strip() if match else ""

    stack_match = re.search(r"\*\*Stack:\*\*[\s\S]*?(?=\n##\s+|$)", preface)
    stack = []
    if stack_match:
        stack = [
            line.strip()[2:].strip()
            for line in stack_match.group(0).splitlines()
            if line.strip().startswith("- ")
        ]

    section_matches = list(re.finditer(r"^##\s+(.+)$", clean_markdown, flags=re.MULTILINE))
    sections: list[dict[str, Any]] = []
    for index, match in enumerate(section_matches):
        heading = match.group(1).strip()
        body_start = match.end()
        body_end = section_matches[index + 1].start() if index + 1 < len(section_matches) else len(clean_markdown)
        body = clean_markdown[body_start:body_end].strip()

        bullets = [
            line.strip()[2:].strip()
            for line in body.splitlines()
            if line.strip().startswith("- ")
        ]

        prose = "\n".join(
            line for line in body.splitlines() if line.strip() and not line.strip().startswith("- ")
        ).strip()

        sections.append(
            {
                "heading": heading,
                "key": section_key(heading),
                "body": prose,
                "bullets": bullets,
            }
        )

    return {
        "title": title_match.group(1).strip() if title_match else "Untitled Project",
        "when": extract_meta("When"),
        "context": extract_meta("Context"),
        "my_role": extract_meta("My role"),
        "stack": stack,
        "sections": sections,
    }


def first_person(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        return cleaned
    if cleaned.startswith("I "):
        return cleaned
    if re.match(r"^[A-Z][a-z]+s\b", cleaned):
        return cleaned
    return f"I {cleaned[0].lower()}{cleaned[1:]}"


def third_person(text: str, display_name: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        return cleaned
    if cleaned.startswith(display_name):
        return cleaned
    if cleaned.startswith("I "):
        return f"{display_name} {cleaned[2:]}"
    return f"{display_name} {cleaned[0].lower()}{cleaned[1:]}"


def normalize_voice_variants(website: dict[str, Any], structured: dict[str, Any], display_name: str) -> dict[str, Any]:
    variants = website.get("voice_variants") if isinstance(website.get("voice_variants"), dict) else {}

    base_summary = str(structured.get("public_summary", "")).strip()
    base_highlights = structured.get("highlights", [])
    base_outcomes = structured.get("outcomes", [])
    base_built = structured.get("what_i_built", [])
    base_impact = structured.get("impact_highlights", [])

    first = variants.get("first_person") if isinstance(variants.get("first_person"), dict) else {}
    third = variants.get("third_person") if isinstance(variants.get("third_person"), dict) else {}

    def clean_summary(value: Any) -> str:
        text = str(value or "").strip()
        return text if is_public_line(text) else ""

    first_summary = clean_summary(first.get("public_summary")) or clean_summary(base_summary)
    third_summary = clean_summary(third.get("public_summary")) or clean_summary(base_summary)

    first_payload = {
        "public_summary": first_person(first_summary),
        "highlights": [first_person(item) for item in sanitize_list(list(first.get("highlights") or base_highlights))],
        "outcomes": [first_person(item) for item in sanitize_list(list(first.get("outcomes") or base_outcomes))],
        "what_i_built": [first_person(item) for item in sanitize_list(list(first.get("what_i_built") or base_built))],
        "impact_highlights": [
            first_person(item) for item in sanitize_list(list(first.get("impact_highlights") or base_impact))
        ],
    }

    third_payload = {
        "public_summary": third_person(third_summary, display_name),
        "highlights": [third_person(item, display_name) for item in sanitize_list(list(third.get("highlights") or base_highlights))],
        "outcomes": [third_person(item, display_name) for item in sanitize_list(list(third.get("outcomes") or base_outcomes))],
        "what_i_built": [third_person(item, display_name) for item in sanitize_list(list(third.get("what_i_built") or base_built))],
        "impact_highlights": [
            third_person(item, display_name)
            for item in sanitize_list(list(third.get("impact_highlights") or base_impact))
        ],
    }

    return {
        "first_person": first_payload,
        "third_person": third_payload,
    }


def export_project(project_dir: Path, voice: str, display_name: str) -> dict[str, Any] | None:
    project_md = project_dir / "project.md"
    if not project_md.exists():
        return None

    parsed = parse_project_markdown(project_md.read_text(encoding="utf-8"))
    website = load_json(project_dir / "website.json", fallback={})
    display = website.get("display") if isinstance(website.get("display"), dict) else {}

    visibility = dict(PUBLIC_SECTION_DEFAULTS)
    visibility.update(website.get("section_visibility", {}))

    public_sections = []
    for section in parsed["sections"]:
        visibility_key = section["key"]
        if visibility.get(visibility_key, "public") != "public":
            continue

        body = sanitize_text(section["body"])
        bullets = sanitize_list(section["bullets"])
        if not body and not bullets:
            continue

        public_sections.append(
            {
                "heading": section["heading"],
                "key": section["key"],
                "body": body,
                "bullets": bullets,
            }
        )

    structured_input = website.get("structured_fields") if isinstance(website.get("structured_fields"), dict) else {}
    highlights = list(structured_input.get("highlights", []))
    outcomes = list(structured_input.get("outcomes", []))
    what_i_built = list(structured_input.get("what_i_built", []))
    impact_highlights = list(structured_input.get("impact_highlights", []))

    if not highlights:
        highlights = list(what_i_built)
    if not outcomes:
        outcomes = list(impact_highlights)

    if not what_i_built:
        what_i_built = list(highlights)

    if not what_i_built:
        for section in public_sections:
            if section["key"] == "what_i_built":
                what_i_built = section["bullets"]
                break

    if not impact_highlights:
        impact_highlights = list(outcomes)

    if not impact_highlights:
        for section in public_sections:
            if section["key"] == "impact":
                impact_highlights = section["bullets"]
                break

    structured = {
        "public_summary": sanitize_text(str(structured_input.get("public_summary", parsed["context"]))),
        "highlights": sanitize_list(highlights),
        "outcomes": sanitize_list(outcomes),
        "what_i_built": sanitize_list(what_i_built),
        "impact_highlights": sanitize_list(impact_highlights),
        "stack": sanitize_list(list(structured_input.get("stack", parsed["stack"]))),
    }

    voice_variants = normalize_voice_variants(website, structured, display_name)

    timeline_display = str(display.get("timeline_display") or "hide")
    title = sanitize_text(str(display.get("title") or parsed["title"]))
    when = sanitize_text(parsed["when"]) if timeline_display != "hide" else ""

    return {
        "slug": project_dir.name,
        "title": title,
        "when": when,
        "context": sanitize_text(parsed["context"]),
        "my_role": sanitize_text(parsed["my_role"]),
        "stack": sanitize_list(parsed["stack"]),
        "display": {"timeline_display": timeline_display},
        "public_sections": public_sections,
        "structured_fields": structured,
        "voice_variants": voice_variants,
        "selected_voice": voice,
        "selected_content": voice_variants.get(voice, voice_variants[DEFAULT_VOICE]),
    }


def sanitize_any(value: Any) -> Any:
    if isinstance(value, str):
        return sanitize_text(value)
    if isinstance(value, list):
        return [item for item in (sanitize_any(item) for item in value) if item not in ("", [], {}, None)]
    if isinstance(value, dict):
        output = {key: sanitize_any(item) for key, item in value.items()}
        return {key: item for key, item in output.items() if item not in ("", [], {}, None)}
    return value


def export_career(career_root: Path, voice: str) -> dict[str, Any]:
    career = load_json(career_root / "career.json", fallback={})

    public_fields = {
        "name": career.get("name", DEFAULT_NAME),
        "headline": career.get("headline", ""),
        "location": career.get("location", ""),
        "links": career.get("links", {}),
        "summary": career.get("summary", ""),
        "target_roles": career.get("target_roles", []),
        "skills": career.get("skills", {}),
        "experience": career.get("experience", []),
        "featured_projects": career.get("featured_projects", []),
        "leadership_profile": career.get("leadership_profile", {}),
        "current_focus": career.get("current_focus", {}),
        "writing": career.get("writing", []),
        "portfolio_style_profile": career.get("portfolio_style_profile", {}),
    }

    sanitized = sanitize_any(public_fields)
    summary = str(sanitized.get("summary", ""))

    if voice == "first_person":
        sanitized["summary"] = first_person(summary)
    else:
        sanitized["summary"] = third_person(summary, str(sanitized.get("name", DEFAULT_NAME)))

    sanitized["selected_voice"] = voice
    sanitized["supported_voices"] = ["first_person", "third_person"]
    return sanitized


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export publish-safe portfolio payloads from a /career repository.")
    parser.add_argument("--root", required=True, help="Path to /career")
    parser.add_argument(
        "--voice",
        choices=["first_person", "third_person"],
        default=DEFAULT_VOICE,
        help="Select voice variant for selected content.",
    )
    parser.add_argument(
        "--out-dir",
        default="public_site",
        help="Output directory name (relative to --root) or absolute path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    career_root = Path(args.root).expanduser().resolve()
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = career_root / out_dir

    projects_dir = career_root / "projects"
    out_projects_dir = out_dir / "projects"
    out_projects_dir.mkdir(parents=True, exist_ok=True)

    career_public = export_career(career_root, args.voice)
    display_name = str(career_public.get("name", DEFAULT_NAME))

    project_payloads = []
    if projects_dir.exists():
        for project_dir in sorted([path for path in projects_dir.iterdir() if path.is_dir()]):
            project_payload = export_project(project_dir, args.voice, display_name)
            if not project_payload:
                continue
            project_payloads.append(project_payload)
            (out_projects_dir / f"{project_payload['slug']}.json").write_text(
                json.dumps(project_payload, indent=2) + "\n",
                encoding="utf-8",
            )

    (out_dir / "career.public.json").write_text(json.dumps(career_public, indent=2) + "\n", encoding="utf-8")
    (out_dir / "index.json").write_text(
        json.dumps(
            {
                "voice": args.voice,
                "career_file": "career.public.json",
                "projects": [payload["slug"] for payload in project_payloads],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"Publish-safe payload exported to: {out_dir}")


if __name__ == "__main__":
    main()
