<!--
Fill in Summary and Test plan normally. The "Action items" section below is
required by hooks/guard-bash.py on `gh pr create` / `gh pr edit` — the
heading has to exist even when there's nothing to list, so a reader can tell
it was considered rather than forgotten. Delete this comment block before
opening the PR.

In repos that have .github/PULL_REQUEST_TEMPLATE/ui_change.md: changing what
a user sees (a component, screen, Spark, or token)? Use the UI template
instead: add `?template=ui_change.md` to the compare URL, or copy
.github/PULL_REQUEST_TEMPLATE/ui_change.md. It carries the UI definition of
done and the required proof links.
-->

## Summary

-

## Test plan

-

## Prevention

<!--
For a bug-fix PR: one line naming the mechanism that keeps this class of bug
from recurring silently. Delete this section for non-fix PRs.

- Regression test: <path to the test that would fail if this bug came back>
- Mechanism: <hook/check/type that would also catch it, if one applies>
- N/A: <reason, if genuinely nothing applies — e.g. a docs-only change>
-->

-

## Action items

<!--
List concrete follow-up work this PR knowingly leaves behind — not
everything worth doing eventually, just what this PR itself surfaced. If
there's genuinely none, write "No action items." and delete the checklist
and YAML block below.

Each item needs a due datetime (ISO 8601, with a timezone offset — no bare
dates) and an owner ("unassigned" is fine). Keep the human checklist and the
YAML block in sync; the YAML is what `scripts/sync-repos.sh` reads to
resurface overdue items automatically, the checklist is what a human reads.

To resolve an item later: edit THIS BODY (`gh pr edit --body-file`) — check
its checklist box and delete or clear its entry from the YAML block below.
`scripts/sync-repos.sh` queries `--state all` and reads only the body, so
the item keeps resurfacing after merge until the body itself says it's done.
A `gh pr comment` is good for a human-readable record of what happened, but
it does not clear the item — see agents/lessons.md.
-->

- [ ] **\<short imperative title\>.** \<what needs doing and why it wasn't
      done in this PR\>. Due **\<YYYY-MM-DDTHH:MM:SS±HH:MM\>**. Owner:
      \<name, agent, or "unassigned"\>.

<details>
<summary>Machine-readable action items (for an agent picking this up later)</summary>

```yaml
action_items:
  - id: short-kebab-case-id
    title: Short imperative title, matches the checklist item above
    due: YYYY-MM-DDTHH:MM:SS±HH:MM
    owner: unassigned
    blocking: false
```
</details>
