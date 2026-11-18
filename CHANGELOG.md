# SENTRY: Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

First public release, accompanying the SENTRY paper.

### Added

- Pretrained SENTRY models for senescent vs. non-senescent cells and primary vs. secondary
  senescence, in `models/`.
- A working test profile (`-profile test,conda`) with synthetic data in `assets/test/`, run in CI.
- Relative paths in the samplesheet and in the threshold combinations file are resolved from
  each file's own folder.
- Documentation for every criterion type, parameter and output.

### Changed

- Renamed the pipeline to SENTRY (`nerettilab/SENTRY`).
- Output file names include the sample name, e.g. `analyzed_data_<sample>_processed_data.tsv.gz`.
- `--column1`, `--column2` and `--threshold_combinations` are required; `--use_raw` is a boolean.
- Conda environments no longer use the Anaconda `defaults` channel.

### Fixed

- Only the first sample in a samplesheet was processed, and outputs of different samples
  overwrote each other.
- `--use_raw false` enabled raw data.
- Human data scored with a mouse model mapped no genes and predicted from all-zero input.
- A combination referencing a missing gene was not skipped as a whole.
- Ages such as `"18-24 months"` were parsed as `1824`.
- Bar charts failed for `column2` values containing `/`.
- Editing the threshold combinations file did not invalidate `-resume` caches, and relative
  paths to it failed.
- Compatibility with pandas 3.

### Removed

- The unused `--minimal_genes` and `--random_sample_proportion` parameters.
- The placeholder `test_full` profile and nf-core-specific GitHub workflows.
