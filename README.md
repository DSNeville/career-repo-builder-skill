# Interview-to-Portfolio Repository Builder

A Codex skill that interviews a user and builds a structured, evidence-aware career repository for:
1. Portfolio-site generation
2. Role-targeted resume tailoring
3. Chatbot-ready professional Q&A grounding

## Repository Layout

```text
career-repo-builder-skill/
  README.md
  interview-to-portfolio-repository-builder/
    SKILL.md
    agents/openai.yaml
    scripts/bootstrap_career_repo.py
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
cp -R /Users/jpneville/projects/career-repo-builder-skill/interview-to-portfolio-repository-builder \
  ~/.codex/skills/interview-to-portfolio-repository-builder
```

## Workflow Summary

1. Run the skill interview to populate `/career`.
2. Complete evidence and publication-safety iteration (sensitive metrics generalized if needed).
3. Confirm leadership/profile data is captured (`leadership_profile`).
4. Optionally run role-targeting modules (`targeting_profile`, `resume_variants`).
5. Hand off `/career` to a portfolio-site build prompt.

## Handoff Contract (Recommended)

Treat these files as required handoff inputs:

1. `career.json`
2. `projects/<slug>/project.md`
3. `projects/<slug>/evidence.yml`
4. `claims.md`
5. `backlog_questions.md`

Publish gating rule:
Only include claims in public output that are publication-safe and have acceptable confidence/evidence.

## Prompt: Build Portfolio Site

Use this prompt with Codex to generate the site:

```text
Build a production-ready portfolio website using the data in <CAREER_ROOT>.

Inputs:
- <CAREER_ROOT>/career.json
- <CAREER_ROOT>/projects/*/project.md
- <CAREER_ROOT>/projects/*/evidence.yml
- <CAREER_ROOT>/claims.md
- <CAREER_ROOT>/backlog_questions.md

Requirements:
1) Generate pages for Home/About, Experience, Projects, and Contact.
2) Use `featured_projects` from career.json first, then optionally additional projects.
3) Render project pages from project.md sections (Context, Role, Impact, Constraints, Team, Leadership, Evidence, Lessons).
4) Show confidence badges for impact claims.
5) Respect evidence visibility:
   - public: render links
   - private/local: show "Evidence available on request" without exposing private paths
6) Add a "Leadership" section using `leadership_profile`.
7) Add a "Selected Stories" section from `story_bank` if present.
8) Exclude or de-emphasize items still marked NEEDS_CLARIFICATION.
9) Keep content scannable and professional.
10) Output a complete runnable project and include run/build commands.

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
cd /Users/jpneville/projects/career-repo-builder-skill
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
