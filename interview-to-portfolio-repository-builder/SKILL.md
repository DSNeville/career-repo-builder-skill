---
name: interview-to-portfolio-repository-builder
description: Conduct a structured, evidence-aware interview and write or update a portfolio-ready /career repository (career.json, project.md, website.json, evidence.yml, claims.md, backlog_questions.md, README.md) for automated portfolio generation and role-targeted resume tailoring.
---

# Interview-to-Portfolio Repository Builder

## Overview

Run a structured interview, capture only user-provided facts, and maintain a durable career dataset on disk for downstream portfolio-site generation and job-targeted resume variants. Keep outputs scannable, evidence-aware, and safe to extend over multiple sessions.

## Non-Negotiable Rules

1. Enforce no fabrication. Never invent facts, metrics, dates, titles, employers, outcomes, awards, or technologies. Mark unknown fields as `NEEDS_CLARIFICATION`.
2. Enforce evidence-aware claims. For every quantified claim, always record:
- `Confidence: HIGH|MEDIUM|LOW`
- `Evidence: <url/path/quote reference or MISSING>`
3. Enforce source bounds. Use only user-provided chat content plus user-provided files/links.
4. Enforce iterative safe writes. Never delete user-authored content. Append or minimally edit sections.
5. Enforce portfolio readiness. Keep writing clear, bullet-first, and suitable for portfolio pages.
6. Enforce publication safety. If a claim is true but too sensitive/specific for public use, iterate with the user to produce a professional, generalized public phrasing and keep detailed internals private.
7. Enforce role-fit traceability. When tailoring for jobs, map projects and claims to target role requirements and keywords.

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
```

Use `scripts/bootstrap_career_repo.py` to initialize missing files quickly and safely.

## Workflow

Run modules in order. Stop-and-save after each module when the user requests it.

### Module 0: Setup

Ask short, specific questions:
1. Display name.
2. Target roles.
3. Tone (`professional`, `playful`, `minimalist`).
4. Emphasis areas (leadership, ML, product, consulting, infra, etc.) and section priorities.
5. Sources:
- Resume (required): paste or file path.
- Optional: old resumes, LinkedIn URL/export, GitHub, personal site, project writeups, decks.
6. Confirm the write target: `/career` and whether it already exists.
7. Confirm whether the user also wants role-targeted resume outputs.
8. If yes, request 1-3 target roles or job postings (URL or pasted text).

Then initialize missing paths with:

```bash
python3 scripts/bootstrap_career_repo.py --root /career
```

Use `--project-slug <slug>` for any project folders you already know.

### Module 1: Resume Extraction (checkpoint)

If resume is a file, read it. If pasted, parse directly.

Extract and write:
1. Roles timeline: company, title, location, start/end.
2. Skills and stack.
3. Project bullets, including vague ones.

Update:
1. `/career/career.json`
2. `/career/backlog_questions.md` with missing dates, acronym expansions, unclear scope, missing metrics
3. `/career/claims.md` with initial claims and `Evidence: MISSING` where needed
4. `/career/README.md` with update and generation instructions

### Module 2: Timeline Clarification

Ask targeted questions to close ambiguity:
1. Exact dates.
2. Official titles.
3. Team size and reporting line.
4. Scope ownership and boundaries.

Update `/career/career.json`, `/career/claims.md`, and `/career/backlog_questions.md`.

### Module 2B: Leadership and Management Signal Capture

Ask targeted leadership questions so chatbot answers can be grounded in repository data:
1. Typical projects managed concurrently.
2. Typical people-management scope (direct reports, dotted-line, mentees, contractors).
3. Team operating model and leadership rituals (1:1s, planning, retros, stakeholder updates).
4. Conflict-resolution approach with one concrete example.
5. Resource rebalancing approach when key contributors are blocked or overloaded.
6. Decision-making style for roadmap/tradeoff calls.

Write results under `career.json.leadership_profile` and add unresolved items to `/career/backlog_questions.md`.

### Module 3: Flagship Project Deep Dive (repeat 3-8 times)

For each project, ask:
1. Project name and time window.
2. Problem/context (who and why).
3. Ownership and role.
4. Constraints (latency, cost, compliance, timeline).
5. Specific stack.
6. Impact (quantitative preferred, qualitative allowed).
7. Collaboration context (team size and stakeholders).
8. Leadership and delivery context (who you managed, execution cadence, unblock/escalation patterns).
9. Lessons and what to change in retrospect.
10. Evidence links (repo, PR, docs, screenshots, decks).
11. Role relevance (which target roles this project supports, covered keywords, likely gaps).
12. Public section visibility by section (`public|private`) for publication safety.
13. Structured website fields:
- `public_summary`
- `what_i_built[]`
- `impact_highlights[]`
- `stack[]`
14. Voice variants for website copy:
- `first_person`
- `third_person`

Write:
1. `/career/projects/<slug>/project.md`
2. `/career/projects/<slug>/website.json`
3. `/career/projects/<slug>/evidence.yml`

Also update:
1. `/career/claims.md` with confidence and evidence
2. `/career/backlog_questions.md` with unresolved proof gaps

Use templates in `references/templates.md`.

### Module 4: Evidence and Verification Pass

Review `claims.md` and request proof for portfolio-visible claims first.

Run a claim formalization loop for publication readiness:
1. Flag any claim that is too specific/sensitive for public posting.
2. Propose 1-2 professional generalized alternatives that stay true.
3. Confirm wording with the user before finalizing public-facing phrasing.
4. Keep any sensitive exact details in private evidence notes, not public claim text.

Normalize evidence:
1. Public URLs preferred.
2. Private links allowed; mark as `PRIVATE`.
3. Local files allowed; keep relative paths.

Upgrade confidence when evidence exists. Downgrade confidence when evidence is weak or missing.

### Module 5: Portfolio Assembly Hints

Tag:
1. `featured_projects` (3-6 projects).
2. About narrative draft.
3. Skill clusters (ML, cloud, product analytics, etc.).

Ensure `career.json` supports common portfolio pages:
1. `summary`
2. `headline`
3. `links`
4. `experience`
5. `featured_projects`
6. `skills`
7. `education`
8. `certifications`
9. `talks`
10. `writing`
11. `leadership_profile`
12. `story_bank`
13. `targeting_profile`
14. `resume_variants`
15. `portfolio_style_profile` (`tone`, `primary_color`, `section_emphasis`)

### Module 6: Role Targeting

Capture resume-targeting inputs:
1. Target role title(s) and seniority.
2. Target industries and company type preferences.
3. Geography, remote/hybrid constraints, and work authorization constraints.
4. Must-have and nice-to-have keywords from target job descriptions.
5. One to three target job postings (URL or pasted text).

Write to `career.json.targeting_profile`:
1. `target_roles`
2. `target_industries`
3. `target_locations`
4. `constraints`
5. `job_postings`
6. `keyword_bank`

Update each flagship project's relevance notes (supported role(s), covered keywords, missing keywords).

### Module 7: Resume Tailoring Pack

Generate resume-ready structured variants in `career.json.resume_variants`:
1. `variant_id`
2. `target_role`
3. `target_job_ref`
4. `summary_angle`
5. `prioritized_skills`
6. `prioritized_projects`
7. `role_fit_bullets`
8. `deprioritized_content`

For each variant:
1. Keep only claims with acceptable confidence/evidence for external use.
2. Prefer publication-safe wording for sensitive metrics.
3. Include a short rationale for why this variant matches the target role.

### Module 8: Handoff Pack

Before ending, prepare handoff-ready instructions for the next build step:
1. Confirm `career` input paths are complete and readable.
2. Summarize unresolved high-priority backlog items.
3. Provide a copy/paste portfolio-site build prompt that references `career.json`, project markdown, evidence files, and claims/backlog gating.
4. If role targeting is enabled, provide a copy/paste resume-tailoring prompt for the top target role.
5. State publication-safety rules explicitly (private/local evidence handling and sensitive metric generalization).
6. Export and lint publish-safe artifacts:
   - `python3 scripts/publish_safe_export.py --root /career --voice first_person`
   - `python3 scripts/publish_lint.py --path /career/public_site`

## File Update Protocol

1. Prefer editing existing files over replacing them.
2. Preserve user-authored content unless explicitly corrected by user.
3. Keep unresolved items visible as `NEEDS_CLARIFICATION`.
4. After each module, show what changed by listing touched files and key additions.
5. Keep interview questions short.
6. For role targeting or resume variants, include explicit keyword-gap questions in backlog.

## Claim Quality Rules

For each claim in `/career/claims.md`, always include:

```text
- Claim: "<text>"
  Confidence: HIGH|MEDIUM|LOW
  Evidence: <url/path or MISSING>
  Related: <project_slug or role>
```

Treat as quantified claims when they mention values like `%`, `$`, counts, latency, throughput, or user scale.
If a quantified claim is not publication-safe, generalize wording with user approval and retain detailed proof context in evidence notes.
When claims are used in resume variants, prefer `HIGH` or `MEDIUM` confidence items unless user explicitly asks to include low-confidence claims.

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
3. Suggested next module to run.

## End Condition

Complete when `/career` contains at least:
1. `career.json` with timeline and skills.
2. Three project folders each with `project.md` and `evidence.yml`.
3. Updated `claims.md` and `backlog_questions.md`.

Then output exactly:

`Career Repository ready. Next: run the portfolio-site generator prompt using /career as input.`
