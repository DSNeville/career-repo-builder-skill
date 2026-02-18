---
name: interview-to-portfolio-repository-builder
description: Conduct a structured, evidence-aware interview and write or update a portfolio-ready /career repository (career.json, project.md, website.json, evidence.yml, claims.md, backlog_questions.md, README.md) for portfolio generation and optional resume/chatbot outputs.
---

# Interview-to-Portfolio Repository Builder

## Overview

Run an adaptive interview, capture only user-provided facts, and maintain a durable `/career` dataset that can power:
1. Portfolio sites
2. Resume tailoring
3. Optional chatbot grounding

Do not assume everyone is a people leader or wants a chatbot.

## Non-Negotiable Rules

1. No fabrication. Never invent facts, metrics, dates, titles, outcomes, or technologies.
2. Evidence-aware claims. Quantified claims must include:
- `Confidence: HIGH|MEDIUM|LOW`
- `Evidence: <url/path/quote reference or MISSING>`
3. Source bounds. Use only user-provided content/files/links.
4. Safe iterative writes. Preserve user-authored content; edit minimally.
5. Public safety defaults:
- no local/private path leakage
- no client name exposure unless explicitly approved
- hide dates when precision is weak
6. Adaptive workflow. Activate only relevant modules based on user profile and desired outputs.

## Output Contract

Required files:

```text
/career
  /career.json
  /projects/<project_slug>/project.md
  /projects/<project_slug>/website.json
  /projects/<project_slug>/evidence.yml
  /claims.md
  /backlog_questions.md
  /README.md
  /public_site/website_handoff.json
  /public_site/website_handoff.md
```

Use:

```bash
python3 scripts/bootstrap_career_repo.py --root /career
```

## Adaptive Workflow

### Module 0: Setup + Capability Scan (required)

Ask concise calibration questions:
1. What output do you want now? (`portfolio`, `resume`, `both`, optional `chatbot`)
2. What is your current work mode? (`individual contributor`, `manager`, `hybrid`, `founder`, `other`)
3. Which dimensions should be emphasized?
- technical delivery
- people leadership
- product/strategy
- mentorship/coaching
- research/innovation
- public presence (writing/speaking)
4. Public-safety preferences:
- anonymize clients? (default yes)
- show project dates? (`always|only_if_precise|hide`)
- show evidence links publicly? (default no)
5. Confirm source inputs and write target path.

Write these into:
- `career.json.profile_context`
- `career.json.assessment_dimensions`
- `career.json.publication_preferences`
- `career.json.site_build_hints`

### Module 1: Resume/Source Extraction (required)

Extract:
1. timeline (company/title/location/start/end)
2. skills + tools
3. project candidates

Update:
1. `career.json`
2. `claims.md`
3. `backlog_questions.md`
4. `README.md`

### Module 2: Clarification Pass (required)

Close gaps with targeted questions:
1. date precision
2. scope and ownership
3. missing impact evidence
4. missing skill coverage

### Module 3: Project Deep Dive (required, repeat)

For each flagship project capture:
1. context/problem
2. ownership and role
3. architecture/implementation specifics
4. constraints and tradeoffs
5. outcomes/impact with evidence
6. public-safe phrasing

Write:
1. `projects/<slug>/project.md`
2. `projects/<slug>/website.json`
3. `projects/<slug>/evidence.yml`

Required `website.json.structured_fields`:
- `public_summary`
- `highlights[]`
- `outcomes[]`
- `stack[]`

Compatibility fields may also be present:
- `what_i_built[]`
- `impact_highlights[]`

### Module 4: Optional Specialized Modules (adaptive)

Only run modules enabled by `assessment_dimensions` or explicit user request.

1. Leadership module:
- populate `career.json.leadership_profile` only when leadership is relevant
2. Chatbot module:
- populate `career.json.assistant_profile` only when chatbot output is requested
3. Public presence module:
- writing/speaking sections only when relevant
4. Resume targeting module:
- `career.json.targeting_profile` and `resume_variants` only when requested

### Module 5: Evidence + Publication Review (required)

1. downgrade or mark weak claims
2. generalize sensitive metrics with user approval
3. ensure public copy excludes private/local references

### Module 6: Build Handoff (required)

Run:

```bash
python3 scripts/publish_safe_export.py --root /career --voice first_person
python3 scripts/publish_lint.py --path /career/public_site
python3 scripts/build_handoff.py --root /career
```

Then summarize:
1. files updated
2. unresolved HIGH-priority backlog items
3. enabled modules and why
4. copy/paste prompt for next portfolio build step

## Dynamic Questioning Standard

Do not use a fixed static questionnaire. Build next questions from current evidence gaps:
1. ask only what unlocks the next artifact
2. prioritize missing facts blocking `public_summary/highlights/outcomes`
3. ask follow-ups when claims are vague, unproven, or non-public-safe

## Backlog Format

Use:

```text
## Missing details
- [ ] <question> (priority: HIGH|MED|LOW) (related: <slug>)
```

## End Condition

Done when:
1. `career.json` includes profile context + adaptive dimensions + publication defaults
2. at least three project folders have `project.md`, `website.json`, `evidence.yml`
3. `claims.md` and `backlog_questions.md` are updated
4. handoff artifacts exist under `public_site/`

Then output exactly:

`Career Repository ready. Next: run the portfolio-site generator prompt using /career as input.`
