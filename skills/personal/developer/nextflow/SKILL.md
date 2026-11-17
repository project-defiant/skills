---
name: nextflow
description: >
  Guide for writing and modifying Nextflow projects.
  Use this skill whenever the user asks to add a new process config,
  tune resource labels, set up a new executor profile (local, Google Batch),
  add ext.args overrides for a module, or wire a new profile into
  nextflow.config, create new workflow or process.
---

# Nextflow project structure

## Project layout

Minimal pipeline structure should be defined as follows

```
{name of the nextflow pipeline}/
│── nextflow.config              # top-level: params, profiles, plugin, base configuration
│── conf/
|  |── google-cloud.config           # configuration for google cloud profile (full profile, do not run by agent!)
|  |── test_google-cloud.config      # configuration for test google cloud profile (small chunk, ensuring that google cloud profile works)
│  └── test.config                   # configuration for local testing (use for all developments!)
|── modules/                         # standalone module (runs independently)
|── workflows/                       # standalone subworkflows
|── tools/                           # tools that are used in processes developed specific to the pipeline only
|── Makefile                         # all development commands to run each profile, test, lint, etc.
|── README.md                        # project readme
|── LICENCE.md                       # project licence (MIT by default)
|── docs/                            # documentation pages
└── main.nf                          # pipeline main entrypoint
```

---

## Resource labels (base.config)

Default process configurations

| Label                 | CPUs         | Memory           | Time                                    |
| --------------------- | ------------ | ---------------- | --------------------------------------- |
| `process_single`      | 1            | 6 GB × attempt   | 4 h × attempt                           |
| `process_low`         | 2 × attempt  | 12 GB × attempt  | 4 h × attempt                           |
| `process_medium`      | 6 × attempt  | 36 GB × attempt  | 8 h × attempt                           |
| `process_high`        | 12 × attempt | 72 GB × attempt  | 16 h × attempt                          |
| `process_long`        | (inherits)   | (inherits)       | 20 h × attempt                          |
| `process_high_memory` | (inherits)   | 200 GB × attempt | (inherits)                              |
| `error_ignore`        | —            | —                | errorStrategy = 'ignore'                |
| `error_retry`         | —            | —                | errorStrategy = 'retry', maxRetries = 2 |

Declare the label in the process definition:

```groovy
process MY_PROCESS {
    label 'process_medium'
    ...
}
```

The base retry logic retries on exit codes 130–145 and 104 (OOM / preemption). Spot VMs on Google Batch are likely to hit these, so `maxRetries = 1` is the floor.

---

## Adding ext.args overrides (modules.config)

`conf/modules.config` is where you tune per-process behaviour without touching the process script itself. The pattern:

```groovy
process {
    withName: 'MY_PROCESS' {
        ext.args   = '--some-flag value'
        ext.prefix = { "${meta.id}_custom" }   // optional, overrides default prefix
        publishDir = [
            path: { "${params.outdir}/my_output" },
            mode: params.publish_dir_mode,
            saveAs: { filename -> filename.equals('versions.yml') ? null : filename }
        ]
    }

    // Scoped to a workflow path (useful when same module appears twice)
    withName: 'FINEMAPPING:MY_PROCESS' {
        ext.args = '--different-flag'
    }
}
```

Inside the process script, consume with:

```groovy
def args = task.ext.args ?: ''
"""
mytool ${args} ...
"""
```

---

## Executor profiles

### gentropy module profiles

The gentropy module's `nextflow.config` wires three profiles:

```groovy
profiles {
    test        { includeConfig 'conf/test.config'         }
    googleCloud { includeConfig 'conf/google-batch.config' }
    docker      { docker.enabled = true                    }
}
```

**`conf/local.config`** (default, always loaded):

```groovy
executor.name = 'local'
params.input  = "tests/data/example_sumstats/..."
```

**`conf/google-batch.config`** — override for GCP:

```groovy
executor.name = 'google-batch'

google {
    enableRequesterPaysBuckets = true
    location                   = 'europe-west1'
    project                    = 'open-targets-genetics-dev'
    batch {
        spot            = true
        maxSpotAttempts = 1
    }
}

params.input = "gs://..."   // swap local path for GCS glob
```

To add a **new executor** (e.g., LSF, Slurm), create `conf/lsf.config`:

```groovy
executor.name = 'lsf'
process {
    queue = 'normal'
}
```

Then add to the `profiles` block in `nextflow.config`:

```groovy
lsf { includeConfig 'conf/lsf.config' }
```

### pipeline profiles

The pipeline's `nextflow.config` uses nf-core's standard profile set (docker, singularity, conda, arm, wave, gitpod, gpu). To add an institution profile, create `conf/<institution>.config` and reference it via the `custom_config_base` mechanism, or add a named profile block directly.

---

## Containers

- **gentropy module**: `docker.io/library/gentropy:000`
  — Version is **manually maintained** in `modules/opentargets/gentropy/main.nf` (no CLI version flag). Update the `VERSION` string and container tag together when bumping.
  — Rebuild: `cd modules/opentargets/gentropy && make build-gentropy-image` (delegates to `gentropy/` submodule's `make build-docker`).

- **sushie module**: `docker.io/cameronlloyd/sushie:latest`
  — Built from `modules/sushie/Dockerfile` (pip-installs from GitHub).

- **pipeline modules**: pulled from `quay.io` registry (set in pipeline `nextflow.config`).

---

## Running with a profile

```bash
# gentropy module — local docker
cd modules/opentargets/gentropy
nextflow run main.nf -profile docker

# gentropy module — Google Cloud
nextflow run main.nf -profile googleCloud,docker --input "gs://bucket/path/**/*.csv"

# pipeline — test profile
cd pipeline
nextflow run main.nf -profile test,docker --outdir results/

# Apple Silicon (force linux/amd64)
nextflow run main.nf -profile docker,arm --outdir results/
```

---

## Checklist when adding a new process

1. Add `label 'process_<size>'` in the process definition.
2. Add a `withName: 'MY_PROCESS'` block in `conf/modules.config` for any fixed args or custom `publishDir`.
3. If the process needs a new container, update `container` in the process and note the version string.
4. Add/update a stub block so nf-test can run without a real container.
