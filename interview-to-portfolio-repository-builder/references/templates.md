# Templates

Use these templates directly when creating or updating repository files.

## `project.md`

```markdown
# <Project Name>
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

**When:** <start-end or year>
**Context:** <1-2 sentence setup: who/why>
**My role:** <what you owned>
**Stack:**
- <tech>

## What I built
- <bullets>

## Impact
- <claim> (Confidence: HIGH|MEDIUM|LOW, Evidence: <url/path or MISSING>)

## Constraints & tradeoffs
- <bullets>

## Team & collaboration
- <bullets>

## Leadership & delivery
- <people management scope>
- <delivery cadence / planning model>
- <conflict handling / unblock approach>

## Role relevance
- Target role(s): <role names>
- Why this project is relevant: <short bullets>
- Keywords covered: <comma-separated list>
- Keyword gaps: <comma-separated list or NONE>

## Evidence
- <link list, or MISSING>

## Notes / lessons
- <bullets>
```

## `website.json` (per project)

```json
{
  "section_visibility": {
    "context": "public",
    "what_i_built": "public",
    "impact": "public",
    "constraints_tradeoffs": "public",
    "team_collaboration": "public",
    "leadership_delivery": "public",
    "role_relevance": "public",
    "evidence": "private",
    "notes_lessons": "public"
  },
  "structured_fields": {
    "public_summary": "<portfolio summary>",
    "what_i_built": ["<bullet>"],
    "impact_highlights": ["<bullet>"],
    "stack": ["<tech>"]
  },
  "voice_variants": {
    "first_person": {
      "public_summary": "I built ...",
      "what_i_built": ["I designed ..."],
      "impact_highlights": ["I improved ..."]
    },
    "third_person": {
      "public_summary": "JP Neville built ...",
      "what_i_built": ["JP designed ..."],
      "impact_highlights": ["JP improved ..."]
    }
  }
}
```

## `evidence.yml`

```yaml
project: "<Project Name>"
time_window: "<start-end>"
evidence:
  - type: "repo|pr|doc|deck|screenshot|blog|video|other"
    label: "<short label>"
    url_or_path: "<url or relative path>"
    visibility: "public|private|local"
    notes: "<optional>"
```

## `career.json` minimum shape

```json
{
  "name": "",
  "headline": "",
  "location": "",
  "links": {"linkedin": "", "github": "", "website": ""},
  "summary": "",
  "portfolio_style_profile": {
    "tone": "professional|playful|minimalist",
    "primary_color": "orange|<other>",
    "section_emphasis": ["current_focus", "featured_projects", "leadership"]
  },
  "target_roles": [],
  "skills": {
    "core": [],
    "tools": [],
    "cloud": [],
    "ml": [],
    "data": []
  },
  "experience": [
    {
      "company": "",
      "title": "",
      "location": "",
      "start_date": "",
      "end_date": "",
      "highlights": [],
      "projects": ["<project_slug>"]
    }
  ],
  "featured_projects": [],
  "leadership_profile": {
    "projects_managed_concurrently": "",
    "people_management_scope": {
      "direct_reports": "",
      "dotted_line_reports": "",
      "mentored_individuals": ""
    },
    "team_management_examples": [],
    "conflict_management_approach": [],
    "resource_rebalancing_approach": [],
    "leadership_rituals": [],
    "chatbot_faq_signals": {
      "projects_managed_at_once": "",
      "people_managed_at_once": "",
      "handling_team_conflict": ""
    }
  },
  "targeting_profile": {
    "target_roles": [],
    "target_industries": [],
    "target_locations": [],
    "constraints": {
      "work_mode": "",
      "work_authorization": "",
      "compensation_notes": ""
    },
    "job_postings": [],
    "keyword_bank": {
      "must_have": [],
      "nice_to_have": [],
      "gaps": []
    }
  },
  "story_bank": [],
  "resume_variants": []
}
```

## `claims.md`

```markdown
- Claim: "<text>"
  Confidence: HIGH|MEDIUM|LOW
  Evidence: <url/path or MISSING>
  Related: <project_slug or role>
```

Publication guidance:
- If exact numbers are sensitive for public posting, keep the claim truthful but generalized.
- Keep detailed numbers in private evidence notes or backlog until approved for publication.
- When a claim is reused in a resume variant, prefer HIGH/MEDIUM confidence items.

## `backlog_questions.md`

```markdown
## Missing details
- [ ] <question> (priority: HIGH|MED|LOW) (related: <slug>)
```

## Publish-safe scripts

```bash
python3 scripts/publish_safe_export.py --root /career --voice first_person
python3 scripts/publish_lint.py --path /career/public_site
```
