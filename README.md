# Interview-to-Portfolio Repository Builder

A Codex skill that interviews a user and builds a structured, evidence-aware career repository for:
1. Portfolio-site generation
2. Role-targeted resume tailoring
3. Optional chatbot-ready professional Q&A grounding
4. Contractor portfolio card buildouts

## Repository Layout

```text
career-repo-builder-skill/
  README.md
  interview-to-portfolio-repository-builder/
    SKILL.md
    agents/openai.yaml
    scripts/bootstrap_career_repo.py
    scripts/publish_safe_export.py
    scripts/publish_lint.py
    scripts/build_handoff.py
    references/templates.md
```

The skill folder is kept clean (no extra docs inside it). This README provides operational handoff guidance.

## Install the Skill

Copy the skill folder into your Codex skills path:

```bash
cp -R /path/to/interview-to-portfolio-repository-builder \
  "$CODEX_HOME/skills/interview-to-portfolio-repository-builder"
```

Common local path:

```bash
cp -R /path/to/career-repo-builder-skill/interview-to-portfolio-repository-builder \
  ~/.codex/skills/interview-to-portfolio-repository-builder
```

## Workflow Summary

1. Run the skill interview to populate `/career`.
2. Run capability scan and enable only relevant modules (IC, leadership, chatbot, resume targeting).
3. Complete evidence and publication-safety iteration (sensitive metrics generalized if needed).
4. Optionally run role-targeting modules (`targeting_profile`, `resume_variants`).
5. Export publish-safe payload and build handoff files.
6. Hand off `/career` to a portfolio-site build prompt.

## Handoff Contract (Recommended)

Treat these files as required handoff inputs:

1. `career.json`
2. `projects/<slug>/project.md`
3. `projects/<slug>/website.json`
4. `projects/<slug>/evidence.yml`
5. `claims.md`
6. `backlog_questions.md`

Publish gating rule:
Only include claims in public output that are publication-safe and have acceptable confidence/evidence.

Run the handoff generators before building the site:

```bash
python3 scripts/publish_safe_export.py --root <CAREER_ROOT> --voice first_person
python3 scripts/publish_lint.py --path <CAREER_ROOT>/public_site
python3 scripts/build_handoff.py --root <CAREER_ROOT>
```

## Prompt: Build Portfolio Site

Use this prompt with Codex to generate the site:

```text
Build a production-ready portfolio website using the data in <CAREER_ROOT>.

Inputs:
- <CAREER_ROOT>/career.json
- <CAREER_ROOT>/projects/*/project.md
- <CAREER_ROOT>/projects/*/website.json
- <CAREER_ROOT>/projects/*/evidence.yml
- <CAREER_ROOT>/claims.md
- <CAREER_ROOT>/backlog_questions.md

Requirements:
1) Generate pages for Home/About, Experience, Projects, and Contact.
2) Use `featured_projects` from career.json first, then optionally additional projects.
3) Render project pages from `project.md` + `website.json` structured fields.
4) Allow tone switching between `first_person` and `third_person` from `website.json.voice_variants`.
5) Use `assessment_dimensions` to decide whether to show leadership/chatbot sections.
6) Respect evidence visibility:
   - public: render links
   - private/local: show "Evidence available on request" without exposing private paths
7) Add a "Leadership" section only if `leadership_profile.enabled` is true.
8) Add chatbot UI only if `site_build_hints.enable_chatbot` is true.
9) Add a "Selected Stories" section from `story_bank` if present.
10) Exclude or de-emphasize items still marked NEEDS_CLARIFICATION.
11) Keep content scannable and professional.
12) Output a complete runnable project and include run/build commands.

Before finalizing, list any blocking data gaps found in backlog_questions.md.
```

## Prompt: Generate Targeted Resume Variant

```text
Using <CAREER_ROOT>, generate a tailored resume variant for target role: <TARGET_ROLE>.

Use:
- career.json (especially targeting_profile, leadership_profile, resume_variants)
- project pages and claims
- evidence visibility rules

Instructions:
1) Prioritize achievements and keywords matching the target role.
2) Use only publication-safe, sufficiently supported claims.
3) Convert project evidence into concise bullet outcomes (action + result + scope).
4) Include leadership and people/project management signals explicitly.
5) Output:
   - 1-page resume markdown
   - ATS keyword checklist
   - gap analysis (missing evidence/keywords)
6) Write/update an entry in `career.json.resume_variants` for this target.
```

## Prompt: Build Chatbot Knowledge Pack

```text
Create a chatbot-ready Q&A knowledge pack from <CAREER_ROOT> with emphasis on:
- leadership_profile
- project ownership and impact
- conflict/resource-management approach
- role-targeting context

Output:
1) FAQ markdown with concise answers.
2) JSON knowledge index keyed by topic (projects, leadership, skills, outcomes, role-fit).
3) "Do not answer" list for claims with low confidence or missing evidence.
```

## Publish This Repo

```bash
cd /path/to/career-repo-builder-skill
git init
git add .
git commit -m "Add interview-to-portfolio skill with handoff prompts"
```

Then create a remote repo and push:

```bash
git branch -M main
git remote add origin <YOUR_REPO_URL>
git push -u origin main
```
