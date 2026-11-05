# Actions Builder Repository

This private repository (`ameya-ff/actions`) acts as a secure container for shared internal tools, reusable GitHub Actions, environment variables, base64-encoded keystores, and Netlify/Cloudflare R2 secrets.

Other repositories (e.g. `flutter`, `aether_flutter`) trigger workflows in this repository through GitHub's `repository_dispatch` webhook mechanism.

## Feature Documentation

- [CI/CD Builder Workflows](.github/workflows/README.md)

## Leak guard

Hooks in `.githooks/` and the `leakguard` workflow block banned terms in diffs, commit messages, branch names and PR text, and block commits whose author or committer email isn't the allowed one. Terms are stored only as hashes, and findings show file and line, never the text.

- Enable locally (once per clone): `git config core.hooksPath .githooks`
- Add a term: append `<length> <hash>` to `.githooks/banned.sha256`, where the hash is `printf %s 'term' | tr A-Z a-z | shasum -a 256` and the length is the term's character count.
- Check the guard: `python3 scripts/leakguard.py --self-test`
