# Create a new Base definition

Create one new `.base` definition file at an exact path. This is one file-creation mutation.

## Preconditions

- The caller supplies `vault=<name>` or `vault=<id>` first.
- The caller has already established that the exact destination path does not exist.
- The destination has a `.base` extension.
- The upstream workflow supplies the complete Base content and has validated its schema.

## Command

```bash
obsidian vault="My Vault" create path="Bases/Projects.base" content="filters:\n  'status == \\\"active\\\"'\nviews:\n  - type: table\n    name: Projects\n    order:\n      - file.name\n      - tags\n"
```

Do not use `overwrite`. Do not use `base:create`: that command creates an item in an existing Base rather than a new `.base` definition.

## Out of scope

This operation does not design or validate Base content, discover a destination, create a Base item, update an existing Base, or delete a Base.
