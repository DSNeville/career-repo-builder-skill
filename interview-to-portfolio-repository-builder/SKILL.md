---
name: interview-to-portfolio-repository-builder
description: Conduct a structured, evidence-aware interview and write or update a portfolio-ready /career repository (career.json, project.md, website.json, evidence.yml, claims.md, backlog_questions.md, README.md) for automated portfolio generation and role-targeted resume tailoring.
---

# Interview-to-Portfolio Repository Builder

## Overview

Run a structured interview, capture only user-provided facts, and maintain a durable career dataset on disk for downstream portfolio-site generation and job-targeted resume variants. Keep outputs scannable, evidence-aware, privacy-safe, and directly buildable.

## Non-Negotiable Rules

1. Enforce no fabrication. Never invent facts, metrics, dates, titles, employers, outcomes, awards, or technologies.
2. Enforce evidence-aware claims. For quantified claims, always record:
- `Confidence: HIGH|MEDIUM|LOW`
- `Evidence: <url/path/quote reference or MISSING>`
3. Enforce source bounds. Use only user-provided chat content plus user-provided files/links.
4. Enforce iterative safe writes. Never delete user-authored content. Append or minimally edit sections.
5. Enforce publication safety by default:
- Hide local/private paths and internal notes from public outputs.
- Do not expose client names unless explicitly approved.
- If dates are incomplete, default to hiding them in public site rendering.
6. Enforce public voice defaults:
- Portfolio/public copy defaults to first-person (`I ...`).
- Recruiter chatbot answers should open with `JP is ...`.
7. Enforce build-ready project structure:
- Every project must have public-safe title, summary, `highlights[]`, and `outcomes[]` in `website.json.structured_fields`.
8. Enforce role-fit traceability. When tailoring for jobs, map projects and claims to target role requirements and keywords.

## Output Contract

Ensure these paths exist before completion:

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

Use `scripts/bootstrap_career_repo.py` to initialize missing files safely.

## Workflow

Run modules in order. Stop-and-save after each module when requested.

### Module 0: Setup

Ask short, specific questions:
1. Display name.
2. Target roles.
3. Tone (`professional`, `playful`, `minimalist`).
4. Emphasis areas (leadership, ML, product, consulting, infra, etc.).
5. Sources:
- Resume (required): paste or file path.
- Optional: older resumes, LinkedIn URL/export, GitHub, project writeups, decks.
6. Confirm write target path (`/career`) and whether it already exists.
7. Confirm whether role-targeted resume outputs are needed.
8. If yes, request 1-3 target roles or job postings.

Then initialize missing paths:

```bash
python3 scripts/bootstrap_career_repo.py --root /career
```

Use `--project-slug <slug>` for any known projects.

### Module 0B: Public-Site Guardrails (new, required)

Before deep interviewing, set explicit publication and site defaults in `career.json`:
1. `publication_preferences.default_public_voice` (`first_person` or `third_person`, default `first_person`).
2. `publication_preferences.anonymize_clients` (default `true`).
3. `publication_preferences.show_project_dates` (`always|only_if_precise|hide`, default `only_if_precise`).
4. `publication_preferences.show_evidence_on_site` (default `false`).
5. `site_build_hints.home_style` (`portfolio_first` by default).
6. `site_build_hints.archive_strategy` (`separate_page` by default).
7. `site_build_hints.project_detail_layout` (`highlights_outcomes` by default).
8. `site_build_hints.chat_audience` (`recruiter_or_hiring_manager` by default).

### Module 1: Resume Extraction (checkpoint)

Extract and write:
1. Roles timeline: company, title, location, start/end.
2. Skills and stack.
3. Project bullets, including vague ones.

Update:
1. `/career/career.json`
2. `/career/backlog_questions.md` with missing dates, acronym expansions, unclear scope, missing metrics
3. `/career/claims.md` with initial claims (`Evidence: MISSING` where needed)
4. `/career/README.md` with update and generation instructions

### Module 2: Timeline + Skill Clarification

Ask targeted questions to close ambiguity:
1. Exact dates and official titles.
2. Team size, reporting line, scope boundaries.
3. Skills not represented in the latest resume but used in real projects.
4. Which tools/skills are public-safe to list.

Update `/career/career.json`, `/career/claims.md`, and `/career/backlog_questions.md`.

### Module 2B: Leadership and Management Signal Capture

Ask targeted leadership questions so chatbot answers can be grounded in repository data:
1. Typical projects managed concurrently.
2. Typical people-management scope.
3. Team operating model and leadership rituals.
4. Conflict-resolution approach with one concrete example.
5. Resource rebalancing approach under delivery pressure.
6. Decision-making style for roadmap and tradeoff calls.

Write to `career.json.leadership_profile`. Add unresolved items to `/career/backlog_questions.md`.

### Module 3: Flagship Project Deep Dive (repeat 3-8 times)

For each project, ask:
1. Project name and time window.
2. Public-safe project title (clear to hiring managers, not internal jargon).
3. Problem/context (who/why) with public-safe wording.
4. Ownership and role.
5. Technical depth:
- architecture and deployment shape
- model hosting/runtime and inference path
- evaluation strategy, tuning/iteration process
- reliability/cost/performance tradeoffs
6. Constraints (latency, cost, compliance, timeline).
7. Collaboration context (team and stakeholders).
8. Leadership and delivery context.
9. Impact (quant preferred, qualitative allowed) with confidence/evidence.
10. Lessons and what to change in retrospect.
11. Evidence links (repo, PR, docs, screenshots, decks).
12. Role relevance (supported roles, covered keywords, gaps).
13. Public section visibility by section (`public|private`).
14. Structured website fields (required):
- `public_summary`
- `highlights[]`
- `outcomes[]`
- `stack[]`
15. Compatibility fields (recommended):
- `what_i_built[]`
- `impact_highlights[]`
16. Voice variants:
- `first_person`
- `third_person`

Write:
1. `/career/projects/<slug>/project.md`
2. `/career/projects/<slug>/website.json`
3. `/career/projects/<slug>/evidence.yml`

Also update:
1. `/career/claims.md`
2. `/career/backlog_questions.md`

Use templates in `references/templates.md`.

### Module 4: Evidence and Verification Pass

Review `claims.md` and request proof for public-facing claims first.

Publication readiness loop:
1. Flag claims too specific/sensitive for public posting.
2. Propose 1-2 generalized alternatives.
3. Confirm wording with user.
4. Keep sensitive exact details in private notes only.

Normalize evidence:
1. Public URLs preferred.
2. Private links allowed; mark as `PRIVATE`.
3. Local files allowed; keep relative paths.

### Module 5: Portfolio Assembly Hints

Tag:
1. `featured_projects` (3-6 projects).
2. About narrative draft (portfolio-first, not resume dump).
3. Skill clusters (core, tools, cloud, ML, data).
4. Archive strategy and page-level content rules.

Ensure `career.json` supports site generation:
1. `summary`
2. `headline`
3. `links`
4. `experience`
5. `featured_projects`
6. `skills`
7. `leadership_profile`
8. `story_bank`
9. `targeting_profile`
10. `resume_variants`
11. `portfolio_style_profile`
12. `publication_preferences`
13. `site_build_hints`

### Module 6: Role Targeting

Capture targeting inputs:
1. Target role title(s) and seniority.
2. Target industries and company type preferences.
3. Geography and work constraints.
4. Must-have and nice-to-have keywords.
5. 1-3 target job postings.

Write to `career.json.targeting_profile` and update project role relevance notes.

### Module 7: Resume Tailoring Pack

Generate `career.json.resume_variants` with:
1. `variant_id`
2. `target_role`
3. `target_job_ref`
4. `summary_angle`
5. `prioritized_skills`
6. `prioritized_projects`
7. `role_fit_bullets`
8. `deprioritized_content`

Prefer HIGH/MEDIUM confidence claims unless user explicitly requests otherwise.

### Module 8: Build Handoff Pack (required)

Before ending:
1. Confirm `career` input paths are complete and readable.
2. Summarize unresolved high-priority backlog items.
3. Provide copy/paste portfolio-site build prompt.
4. If role targeting is enabled, provide top-role resume-tailoring prompt.
5. State publication-safety rules explicitly.
6. Export and lint publish-safe artifacts:

```bash
python3 scripts/publish_safe_export.py --root /career --voice first_person
python3 scripts/publish_lint.py --path /career/public_site
python3 scripts/build_handoff.py --root /career
```

7. Validate chatbot-readiness in handoff summary:
- show 3 suggested recruiter questions
- confirm fallback text
- confirm no private evidence leakage

## File Update Protocol

1. Prefer editing existing files over replacing them.
2. Preserve user-authored content unless explicitly corrected.
3. Keep unresolved items visible as `NEEDS_CLARIFICATION`.
4. After each module, list touched files and key additions.
5. Keep interview questions short.
6. For role targeting, include explicit keyword-gap questions in backlog.

## Claim Quality Rules

For each claim in `/career/claims.md`, always include:

```text
- Claim: "<text>"
  Confidence: HIGH|MEDIUM|LOW
  Evidence: <url/path or MISSING>
  Related: <project_slug or role>
```

Treat as quantified claims when they include `%`, `$`, counts, latency, throughput, or user scale.
If quantified claims are not publication-safe, generalize wording with user approval.

## Backlog Format

Use this format in `/career/backlog_questions.md`:

```text
## Missing details
- [ ] <question> (priority: HIGH|MED|LOW) (related: <slug>)
```

## Stop and Ship Behavior

If user says `stop` or `ship it`, finish current file writes, then provide:
1. Exact files updated.
2. Outstanding high-priority backlog questions.
3. Suggested next module.

## End Condition

Complete when `/career` contains at least:
1. `career.json` with timeline, skills, publication preferences, and site build hints.
2. Three project folders each with `project.md`, `website.json`, and `evidence.yml`.
3. Updated `claims.md` and `backlog_questions.md`.
4. `public_site/website_handoff.json` and `public_site/website_handoff.md`.

Then output exactly:

`Career Repository ready. Next: run the portfolio-site generator prompt using /career as input.`
