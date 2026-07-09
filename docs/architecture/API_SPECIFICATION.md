# Codex Service API Specification

Stable service methods:

- `discover(request) -> CandidateStream`
- `validate() -> ValidationReport`
- `regress() -> RegressionReport`
- `plugins() -> PluginRegistry`
- `languages() -> LanguagePackRegistry`
- `save_review(candidate_id, state) -> ReviewRecord`
- `export(request) -> ExportResult`

## Candidate

Required fields:

- id
- candidate
- translation
- score
- score_breakdown
- language
- search_mode
- source_pool
- review_status
- canon_status
- provenance
- created_at
- engine_version
