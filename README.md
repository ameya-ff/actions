# Actions Builder Repository

This private repository (`ameya-ff/actions`) acts as a secure container for shared internal tools, reusable GitHub Actions, environment variables, base64-encoded keystores, and Netlify/Cloudflare R2 secrets.

Other repositories (e.g. `farflungai/flutter`, `farflungai/aether_flutter`) trigger workflows in this repository through GitHub's `repository_dispatch` webhook mechanism.

## Feature Documentation

- [CI/CD Builder Workflows](.github/workflows/README.md)
