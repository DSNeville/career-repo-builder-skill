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
**Context:** <1-2 sentence setup>
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

## Leadership & delivery (optional)
- <only if relevant>

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
  "display": {
    "title": "<public-safe title>",
    "timeline_display": "hide"
  },
  "structured_fields": {
    "public_summary": "<portfolio summary>",
    "highlights": ["<bullet>"],
    "outcomes": ["<bullet>"],
    "what_i_built": ["<compatibility bullet>"],
    "impact_highlights": ["<compatibility bullet>"],
    "stack": ["<tech>"]
  },
  "voice_variants": {
    "first_person": {
      "public_summary": "I built ...",
      "highlights": ["I designed ..."],
      "outcomes": ["I improved ..."],
      "what_i_built": ["I designed ..."],
      "impact_highlights": ["I improved ..."]
    },
    "third_person": {
      "public_summary": "The candidate built ...",
      "highlights": ["The candidate designed ..."],
      "outcomes": ["The candidate improved ..."],
      "what_i_built": ["The candidate designed ..."],
      "impact_highlights": ["The candidate improved ..."]
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
  "links": {"linkedin": "", "github": "", "website": "", "email": ""},
  "summary": "",
  "profile_context": {
    "work_mode": "individual_contributor|manager|hybrid|founder|other",
    "seniority": "",
    "domain_focus": []
  },
  "assessment_dimensions": [
    {"id": "technical_delivery", "enabled": true, "priority": "HIGH"},
    {"id": "people_leadership", "enabled": false, "priority": "MED"},
    {"id": "mentorship_coaching", "enabled": false, "priority": "MED"},
    {"id": "product_strategy", "enabled": false, "priority": "MED"},
    {"id": "research_innovation", "enabled": false, "priority": "LOW"},
    {"id": "public_presence", "enabled": false, "priority": "LOW"}
  ],
  "portfolio_style_profile": {
    "tone": "professional|playful|minimalist",
    "primary_color": "neutral|<other>",
    "section_emphasis": ["featured_projects", "about", "skills"]
  },
  "publication_preferences": {
    "default_public_voice": "first_person|third_person",
    "anonymize_clients": true,
    "anonymize_employer_names": false,
    "show_evidence_on_site": false,
    "show_project_dates": "always|only_if_precise|hide",
    "include_writing_section": false
  },
  "site_build_hints": {
    "home_style": "portfolio_first",
    "archive_strategy": "separate_page",
    "project_detail_layout": "highlights_outcomes",
    "enable_chatbot": false,
    "chat_audience": ""
  },
  "target_roles": [],
  "skills": {
    "core": [],
    "tools": [],
    "cloud": [],
    "ml": [],
    "data": []
  },
  "experience": [],
  "featured_projects": [],
  "leadership_profile": {
    "enabled": false,
    "summary": "",
    "scope": {},
    "examples": []
  },
  "assistant_profile": {
    "enabled": false,
    "audience": "",
    "response_style": "",
    "fallback_contact": "",
    "faq_signals": {}
  },
  "targeting_profile": {},
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

## `backlog_questions.md`

```markdown
## Missing details
- [ ] <question> (priority: HIGH|MED|LOW) (related: <slug>)
```

## `public_site/website_handoff.json` shape

```json
{
  "generated_at_utc": "<iso8601>",
  "source_root": "<career path>",
  "defaults": {
    "public_voice": "first_person",
    "anonymize_clients": true,
    "show_evidence_on_site": false,
    "show_project_dates": "only_if_precise"
  },
  "site_profile": {
    "home_style": "portfolio_first",
    "archive_strategy": "separate_page",
    "project_detail_layout": "highlights_outcomes",
    "enable_chatbot": false,
    "chat_audience": ""
  },
  "navigation": ["about", "featured-projects", "skills", "archive", "contact"],
  "featured_project_order": ["<slug>"],
  "projects": [{"slug": "<slug>", "bucket": "featured|archive", "ready_for_site": true}],
  "chat_requirements": null,
  "public_safety_rules": ["..."]
}
```

## Publish-safe scripts

```bash
python3 scripts/publish_safe_export.py --root /career --voice first_person
python3 scripts/publish_lint.py --path /career/public_site
python3 scripts/build_handoff.py --root /career
```
