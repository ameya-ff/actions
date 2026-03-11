# Actions / Builders

This directory contains the central GitHub Actions build runner workflows. We use a **two-repo dispatch pattern** where external repositories (like `farflungai/aether_flutter` and `farflungai/flutter`) trigger these central workflows via `repository_dispatch`.

This architecture allows us to keep sensitive secrets (like Android Keystore variables, Google Play service accounts, Netlify tokens, Cloudflare R2 credentials) contained within this private repository instead of duplicating them across multiple projects.

## Components

### Aether Flutter Workflow (`aether-flutter.yaml`)
Handles cross-platform CI/CD for the `farflungai/aether_flutter` repository.

**Triggers:**
*   **Dev:** Triggered by push to `main` via `trigger-aether-flutter-workflow` dispatch.
*   **Prod:** Triggered by `v*` tag creation via `trigger-aether-flutter-workflow` dispatch.
*   **Manual:** Can be triggered via `workflow_dispatch`.

**Features:**
1.  **Web Build:** Compiles the app for Web (`--dart-define-from-file=env/{env}.json`) and uploads to Netlify. Conditionally uses `NETLIFY_SITE_ID_AETHER_DEV` or `NETLIFY_SITE_ID_AETHER_PROD` based on the payload environment.
2.  **Android Build:** Sets up the keystore from `AETHER_ANDROID_KEYSTORE_BASE_64` and `AETHER_ANDROID_KEYPROPERTIES_BASE_64`. Builds `APK` and `AAB`.
3.  **Storage:** Automatically uploads artifacts to Cloudflare R2 buckets for backup and sharing.
4.  **Google Play Distribution:** When triggered with `env: prod`, it uploads the generated `AAB` to the Google Play Store internal track.

### Legacy/Other Workflows
*   `flutter.yaml` - The main CI/CD builder for the original `farflungai/flutter` consumer app.
*   `flutter-stage.yaml` - A builder that executes pull-request previews (web builds) for the `farflungai/flutter` app.
