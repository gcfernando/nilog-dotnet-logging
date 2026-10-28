# Repository standards

This repository follows the shared administration and documentation baseline across Gehan Fernando's local repositories. Project-specific build, source, data and licensing requirements remain in the existing guides.

## Structure

| Location | Purpose |
| --- | --- |
| `README.md` | Project overview, prerequisites, usage and support |
| `documentation.md` | Entry point to the existing guides |
| `CONTRIBUTING.md` | Contribution process and actual validation commands |
| `SECURITY.md` | Private vulnerability reporting and scope |
| `.github/ISSUE_TEMPLATE/` | Public issue forms and private security-reporting link |
| `.github/pull_request_template.md` | Change description, validation and impact |
| `.github/workflows/` | Active CI, release and documentation workflows |
| `.github/scripts/check_repository.py` | Dependency-free metadata check |
| `.github/dependabot.yml` | Weekly updates for GitHub Actions pins |

Keep the existing `Nilog/` solution and root packaging/documentation metadata. Preserve existing source and dataset paths, package boundaries, generated assets, imported snapshots and published routes. Do not add empty source or test directories for visual symmetry. Keep new written guides with the existing documentation; use lowercase hyphenated ordinary filenames and conventional names such as `README.md`.

## Formatting and configuration

Use UTF-8 without a byte order mark, LF line endings and a final newline for root documentation and repository administration. Use one level-one title in each primary guide, hierarchical headings and blank lines around headings and lists. Keep intentional two-space Markdown line breaks, code fences, attribution and stable anchors. Match link paths and filename case exactly.

The shared `.editorconfig` and `.gitattributes` sections cover documentation and administration. Existing application-specific settings and Git LFS rules take precedence within their scope. Do not run repository-wide source formatters or Git renormalization as part of metadata maintenance. Ignore local secrets, editor caches and generated output; keep safe example configuration explicit.

## Automation

Active workflows pin external actions to full commit SHAs, declare read-only default contents permissions and set job timeouts. Grant write permissions only to jobs that publish artifacts or documentation. Dependabot proposes weekly GitHub Actions updates; review them before merging. Preserve project-specific SDKs, dependency locks and release triggers.

Run `python .github/scripts/check_repository.py` with Python 3.12 or later. The Repository standards workflow runs the same check on pushes, pull requests and manual dispatch. Its scope is root documentation and repository administration. Follow [CONTRIBUTING.md](CONTRIBUTING.md) for application, data, hardware and site checks.

## GitHub settings

The shared baseline uses `main`, an enabled issue tracker, the repository's documentation homepage, all three merge methods, read-only default workflow tokens, private vulnerability reporting, secret scanning and push protection. Main-branch protection prevents force pushes and deletion. Required reviews and status checks are configured only when a project's contribution process calls for them.

Wikis and discussions remain optional project features. Existing Pages deployment modes are preserved: the developer resource site uses its custom Actions build, while the other repositories publish from `main` at the root. Preserve existing merge cleanup preferences and project-specific topics. Keep the homepage consistent with `_config.yml`.

## Licensing and review boundaries

Keep existing license texts and third-party notices. Do not assign a license to an unlicensed project or dataset without an explicit rights decision. Public availability alone does not grant reuse permission. Describe verification accurately and keep source-code changes separate from repository administration work.
