# Release Checklist

Follow these steps to ensure a consistent and high-quality release process for `generic-rag`.

## Pre-Release Preparation

- [ ] **Clean Git Status**: Ensure you are on the `main` branch and have no uncommitted changes.
- [ ] **Latest Code**: `git pull origin main` to ensure you have the latest changes.
- [ ] **Verify Version**: Check `pyproject.toml` and ensure the `version` field is correctly set (e.g., `1.0.0`).

## Quality Assurance (QA)

- [ ] **Run Unit Tests**: Execute `python -m pytest` and ensure all tests pass.
- [ ] **Verify Compilation**: Execute `python -m compileall src examples` to catch syntax errors.
- [ ] **CLI Smoke Tests**:
  - [ ] `generic-rag --version` (matches `pyproject.toml`)
  - [ ] `generic-rag doctor`
  - [ ] `generic-rag demo offline`
  - [ ] `generic-rag provider check-env`
  - [ ] `generic-rag inspect file README.md`
- [ ] **Documentation Review**:
  - [ ] README.md links and version status are correct.
  - [ ] CHANGELOG.md includes the new version and its changes.
  - [ ] API Reference is up to date.

## Execution

- [ ] **Commit Release**: If you bumped the version, commit with `chore: bump version to X.Y.Z`.
- [ ] **Create Tag**: `git tag -a vX.Y.Z -m "Release vX.Y.Z"` (e.g., `git tag -a v1.0.0 -m "Release v1.0.0"`).
- [ ] **Push to Main**: `git push origin main`.
- [ ] **Push Tags**: `git push origin --tags`.

## Post-Release

- [ ] **GitHub Release**:
  - [ ] Go to the repository on GitHub.
  - [ ] Draft a new release using the tag you just pushed.
  - [ ] Copy the relevant section from `CHANGELOG.md` into the release notes.
  - [ ] Publish the release.

## Rollback Procedure

- **Never mutate or delete a published tag/release** if possible.
- If a critical bug is found immediately after release, fix it and release a new patch version (e.g., `v1.0.1`).
