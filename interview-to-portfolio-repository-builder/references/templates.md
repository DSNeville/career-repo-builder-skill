# Templates

Use these templates directly when creating or updating repository files.

## `project.md`

```markdown
# <Project Name>
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
  "role_signal_profile": {
    "track": "individual-contributor|people-leader|hybrid|founder|research|product|NEEDS_CLARIFICATION",
    "scope_signals": [],
    "execution_signals": [],
    "decision_signals": [],
    "collaboration_signals": [],
    "faq_signals": {}
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
    "job_postings": [
      {
        "id": "",
        "company": "",
        "role_title": "",
        "url_or_text_ref": "",
        "priority": "HIGH|MED|LOW"
      }
    ],
    "keyword_bank": {
      "must_have": [],
      "nice_to_have": [],
      "gaps": []
    }
  },
  "story_bank": [
    {
      "id": "",
      "theme": "delivery|leadership|conflict|tradeoff|failure-recovery",
      "format": "STAR|CAR",
      "situation": "",
      "task": "",
      "action": "",
      "result": "",
      "evidence": "MISSING"
    }
  ],
  "resume_variants": [
    {
      "variant_id": "",
      "target_role": "",
      "target_job_ref": "",
      "summary_angle": "",
      "prioritized_skills": [],
      "prioritized_projects": [],
      "role_fit_bullets": [],
      "deprioritized_content": [],
      "rationale": ""
    }
  ]
}
```

Optional compatibility field:
- `leadership_profile` can be added when the user is explicitly leadership-oriented, but should not be required.

## `facts_index.json`

```json
{
  "version": "1",
  "profile": {
    "positioning": [],
    "audience_notes": [],
    "public_safety_notes": []
  },
  "intents": [
    {
      "intent": "current-focus|project-fit|skills|leadership|delivery-style|career-story|subjective-inference",
      "signals": [],
      "response_pattern": "NEEDS_CLARIFICATION",
      "source_priority": []
    }
  ],
  "facts": [
    {
      "id": "fact-001",
      "type": "profile|project|role|skill|outcome|values",
      "subject": "career|<project_slug>",
      "statement": "NEEDS_CLARIFICATION",
      "tags": [],
      "confidence": "HIGH|MEDIUM|LOW",
      "evidence": "MISSING",
      "public_safe": true
    }
  ],
  "project_cards": [
    {
      "slug": "<project_slug>",
      "highlights": [],
      "outcomes": [],
      "stack": []
    }
  ]
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
