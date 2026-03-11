---
description: check antigravity brain session sizes, extract skills from large sessions, then delete them
---

# Antigravity Brain Cleanup

## 1. Audit session sizes

// turbo
Run `du -sh ~/.gemini/antigravity/brain/*/ 2>/dev/null | sort -rh | head -30` to list sessions by size.

## 2. Identify candidates for skill extraction

For each session over ~50MB:
- Check what the session was about by reading `ls ~/.gemini/antigravity/brain/<id>/` and any artifact files inside.
- Cross-reference with the conversation summaries provided at conversation start.
- Ask: "Is there a repeatable workflow or domain knowledge here worth capturing as a skill?"

## 3. Create skills from valuable sessions

For sessions containing repeatable workflows (e.g. research patterns, domain-specific scraping, project-specific ops):
- Identify the target repo and create the skill under `<repo>/.agents/skills/<skill-name>/SKILL.md`
- The SKILL.md should follow the format: YAML frontmatter (`name`, `description`) + markdown body
- Include: repo/dir structure, key concepts/formulas, step-by-step workflow, known gotchas, file templates
- Commit the skill: `git add .agents/skills/<name>/SKILL.md && git commit -m "chore: add <name> agent skill"`

## 4. Clean up large sessions

Delete sessions whose knowledge has been extracted (or is not worth preserving):
```
rm -rf ~/.gemini/antigravity/brain/<session-id>
```
Delete multiple at once where possible. Always keep sessions from the last 24h.

## 5. Remove empty session dirs

// turbo
Run `find ~/.gemini/antigravity/brain -maxdepth 1 -type d -empty ! -name brain | xargs rm -rf`

## 6. Confirm final size

// turbo
Run `du -sh ~/.gemini/antigravity/brain/` to confirm the cleanup result.
