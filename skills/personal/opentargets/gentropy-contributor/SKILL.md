---
name: gentropy-contributor
description: Guides contributions in the upstream Gentropy repository. Use when contributing to the `opentargets/gentropy` repository.
---

# Gentropy Contributor

Use this skill only for work in the upstream `opentargets/gentropy` repository.

## Workflow

### Must

- Use `uv` whenever invoking Python tooling.
- Use `ruff`, `mypy`, and `pytest` in the development flow.
- Use relevant `Makefile` targets for verification when appropriate, including `make test`.
- Run `uv run pre-commit run --all-files` before finalizing changes.
- Document code primarily through Google-style docstrings so MkDocs can surface the changes automatically.
- Keep datasets derived from `Dataset`.
- Never push directly to `dev` or `main`.

### Default

- Start implementation work from a feature branch or worktree, typically `feat/{feature_name}`.
- Prefer doctests for simple public behavior and examples.
- For PySpark tests, prefer existing Spark session fixtures.
- Reflect package structure in test structure.
- Prefer PySpark SQL functions over UDFs.
- If a UDF is required, prefer `pandas_udf` before a plain UDF.

### When Applicable

- Use pytest marks defined in `pyproject.toml`.
- For new core datasets, generate the JSON schema asset in the appropriate assets directory.
- For new runnable pipeline entrypoints, add a top-level step and register it through the Hydra config surface.
- Add integration coverage for new steps and mark those tests appropriately.
- Use TDD when it fits the change shape.
- For all non-trivial Spark tasks, inspect the generated plan and simplify it when possible.
- Use `persist` or `cache` when the plan shows repeated recomputation of the same work.

## Structure

- `Dataset`: a `Dataset`-derived wrapper around a PySpark DataFrame plus dataset-specific methods.
- Core datasets: `StudyIndex`, `StudyLocus`, `TargetIndex`, `VariantIndex`, `BiosampleIndex`, `SummaryStatistics`.
- `Datasource`: provider-specific harmonisation workflow that converts external data into Gentropy core datasets.
- `Method`: an algorithm implemented on top of PySpark that operates on datasets.
- `Step`: a top-level runnable workflow or CLI entrypoint.

## Development Order

1. Read the local module, matching tests, and docstrings before editing.
2. Make the smallest change that fits the existing Gentropy structure.
3. Add or update docstrings and tests alongside the code.
4. Run targeted verification first, then broader repo verification.
