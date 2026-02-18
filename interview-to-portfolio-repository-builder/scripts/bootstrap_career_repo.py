#!/usr/bin/env python3
"""
Create or safely extend a /career repository skeleton for portfolio generation
and role-targeted resume tailoring.

Usage examples:
  python3 scripts/bootstrap_career_repo.py --root /career
  python3 scripts/bootstrap_career_repo.py --root /career --project-slug fraud-detection-v2
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


CAREER_TEMPLATE = {
    "name": "",
    "headline": "",
    "location": "",
    "links": {"linkedin": "", "github": "", "website": "", "email": ""},
    "summary": "",
    "profile_context": {
        "work_mode": "individual_contributor",
        "seniority": "",
        "domain_focus": [],
    },
    "assessment_dimensions": [
        {"id": "technical_delivery", "enabled": True, "priority": "HIGH"},
        {"id": "people_leadership", "enabled": False, "priority": "MED"},
        {"id": "mentorship_coaching", "enabled": False, "priority": "MED"},
        {"id": "product_strategy", "enabled": False, "priority": "MED"},
        {"id": "research_innovation", "enabled": False, "priority": "LOW"},
        {"id": "public_presence", "enabled": False, "priority": "LOW"},
    ],
    "portfolio_style_profile": {
        "tone": "professional",
        "primary_color": "neutral",
        "section_emphasis": [
            "featured_projects",
            "about",
            "skills",
        ],
    },
    "publication_preferences": {
        "default_public_voice": "first_person",
        "anonymize_clients": True,
        "anonymize_employer_names": False,
        "show_evidence_on_site": False,
        "show_project_dates": "only_if_precise",
        "include_writing_section": False,
    },
    "site_build_hints": {
        "home_style": "portfolio_first",
        "archive_strategy": "separate_page",
        "project_detail_layout": "highlights_outcomes",
        "enable_chatbot": False,
        "chat_audience": "",
    },
    "target_roles": [],
    "skills": {
        "core": [],
        "tools": [],
        "cloud": [],
        "ml": [],
        "data": [],
    },
    "experience": [],
    "featured_projects": [],
    "leadership_profile": {
        "enabled": False,
        "summary": "",
        "scope": {},
        "examples": [],
    },
    "assistant_profile": {
        "enabled": False,
        "audience": "",
        "response_style": "",
        "fallback_contact": "",
        "faq_signals": {},
    },
    "targeting_profile": {
        "target_roles": [],
        "target_industries": [],
        "target_locations": [],
        "constraints": {
            "work_mode": "",
            "work_authorization": "",
            "compensation_notes": "",
        },
        "job_postings": [],
        "keyword_bank": {
            "must_have": [],
            "nice_to_have": [],
            "gaps": [],
        },
    },
    "story_bank": [],
    "resume_variants": [],
    "education": [],
    "certifications": [],
    "talks": [],
    "writing": [],
}


README_TEMPLATE = """# Career Repository

This folder stores a structured, evidence-aware career dataset used for automated portfolio generation.

## Contents
- `career.json`: core profile, timeline, skills, and featured projects
- `projects/<slug>/project.md`: project narrative and impact
- `projects/<slug>/evidence.yml`: evidence links and provenance
- `projects/<slug>/website.json`: publication controls and structured portfolio fields
- `claims.md`: claims with confidence and evidence traceability
- `backlog_questions.md`: unresolved clarification/evidence questions
- `career.json.assessment_dimensions`: adaptive interview coverage by profile type
- `career.json.leadership_profile`: optional leadership-specific signals
- `career.json.assistant_profile`: optional chatbot-specific signals
- `career.json.targeting_profile`: role targeting and keyword mapping inputs
- `career.json.story_bank`: interview-ready STAR/CAR stories
- `career.json.resume_variants`: role-specific resume tailoring pack

## Update Protocol
1. Do not fabricate details. Use `NEEDS_CLARIFICATION` for unknowns.
2. For quantified claims, include confidence and evidence.
3. Preserve prior user-authored content unless explicitly corrected.
4. For sensitive quantified claims, confirm public-safe generalized wording.
5. For tailored resumes, map project evidence and claims to target-role keywords.

## Publish-safe workflow
1. Create or update project `website.json` files:
   - `section_visibility` for public/private section handling.
   - `structured_fields` for portfolio rendering (`public_summary`, `highlights`, `outcomes`, `stack`).
   - `voice_variants` for `first_person` and `third_person`.
2. Export sanitized public payloads:
   - `python3 scripts/publish_safe_export.py --root /career --voice first_person`
3. Lint publish outputs:
   - `python3 scripts/publish_lint.py --path /career/public_site`
4. Generate build handoff artifacts:
   - `python3 scripts/build_handoff.py --root /career`
"""


CLAIMS_TEMPLATE = """# Claims

- Claim: "NEEDS_CLARIFICATION"
  Confidence: LOW
  Evidence: MISSING
  Related: general
"""


BACKLOG_TEMPLATE = """## Missing details
- [ ] Add missing resume fields: full dates, metrics, and project evidence. (priority: HIGH) (related: general)
"""


PROJECT_MD_TEMPLATE = """# {project_name}
---
section_visibility:
  context: public
  what_i_built: public
  impact: public
  constraints_tradeoffs: public
  team_collaboration: public
  leadership_delivery: public
  role_relevance: public
  evidence: private
  notes_lessons: public
---

**When:** NEEDS_CLARIFICATION
**Context:** NEEDS_CLARIFICATION
**My role:** NEEDS_CLARIFICATION
**Stack:**
- NEEDS_CLARIFICATION

## What I built
- NEEDS_CLARIFICATION

## Impact
- NEEDS_CLARIFICATION (Confidence: LOW, Evidence: MISSING)

## Constraints & tradeoffs
- NEEDS_CLARIFICATION

## Team & collaboration
- NEEDS_CLARIFICATION

## Leadership & delivery
- NEEDS_CLARIFICATION

## Role relevance
- NEEDS_CLARIFICATION

## Evidence
- MISSING

## Notes / lessons
- NEEDS_CLARIFICATION
"""


WEBSITE_JSON_TEMPLATE = {
    "section_visibility": {
        "context": "public",
        "what_i_built": "public",
        "impact": "public",
        "constraints_tradeoffs": "public",
        "team_collaboration": "public",
        "leadership_delivery": "public",
        "role_relevance": "public",
        "evidence": "private",
        "notes_lessons": "public",
    },
    "display": {
        "title": "NEEDS_CLARIFICATION",
        "timeline_display": "hide",
    },
    "structured_fields": {
        "public_summary": "NEEDS_CLARIFICATION",
        "highlights": [],
        "outcomes": [],
        "what_i_built": [],
        "impact_highlights": [],
        "stack": [],
    },
    "voice_variants": {
        "first_person": {
            "public_summary": "I NEEDS_CLARIFICATION",
            "highlights": [],
            "outcomes": [],
            "what_i_built": [],
            "impact_highlights": [],
        },
        "third_person": {
            "public_summary": "Candidate NEEDS_CLARIFICATION",
            "highlights": [],
            "outcomes": [],
            "what_i_built": [],
            "impact_highlights": [],
        },
    },
}


EVIDENCE_YML_TEMPLATE = """project: "{project_name}"
time_window: "NEEDS_CLARIFICATION"
evidence:
  - type: "other"
    label: "MISSING"
    url_or_path: "MISSING"
    visibility: "local"
    notes: "Add source link or path."
"""


def write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def ensure_career_json(path: Path) -> None:
    if not path.exists():
        path.write_text(json.dumps(CAREER_TEMPLATE, indent=2) + "\n", encoding="utf-8")
        return

    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        path.write_text(json.dumps(CAREER_TEMPLATE, indent=2) + "\n", encoding="utf-8")
        return

    try:
        existing = json.loads(raw)
    except json.JSONDecodeError:
        backup = path.with_suffix(".json.bak")
        backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        path.write_text(json.dumps(CAREER_TEMPLATE, indent=2) + "\n", encoding="utf-8")
        return

    changed = False
    for key, default_value in CAREER_TEMPLATE.items():
        if key not in existing:
            existing[key] = default_value
            changed = True

    if changed:
        path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")


def ensure_project(root: Path, slug: str) -> None:
    project_dir = root / "projects" / slug
    project_name = slug.replace("-", " ").title()

    write_if_missing(
        project_dir / "project.md",
        PROJECT_MD_TEMPLATE.format(project_name=project_name),
    )
    write_if_missing(
        project_dir / "website.json",
        json.dumps(WEBSITE_JSON_TEMPLATE, indent=2) + "\n",
    )
    write_if_missing(
        project_dir / "evidence.yml",
        EVIDENCE_YML_TEMPLATE.format(project_name=project_name),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap or extend a /career repository.")
    parser.add_argument(
        "--root",
        required=True,
        help="Target career directory path, e.g. /career or ./career",
    )
    parser.add_argument(
        "--project-slug",
        action="append",
        default=[],
        help="Optional project slug to precreate under projects/<slug>/",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    ensure_career_json(root / "career.json")
    write_if_missing(root / "claims.md", CLAIMS_TEMPLATE)
    write_if_missing(root / "backlog_questions.md", BACKLOG_TEMPLATE)
    write_if_missing(root / "README.md", README_TEMPLATE)

    for slug in args.project_slug:
        if not slug.strip():
            continue
        ensure_project(root, slug.strip())

    print(f"Career repository ensured at: {root}")


if __name__ == "__main__":
    main()
