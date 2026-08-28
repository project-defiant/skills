# Project Bases

An Obsidian Base is a `.base` file containing YAML. Create one Base at `Projects/{project}/project.base` for every new project.

## Required behaviour

- Scope project-local notes with `file.inFolder()` using the path relative to the actual Obsidian vault root.
- Include external source and topic notes through their normalised `project` or `projects` metadata.
- Provide these views: Project documents, PRDs, Meetings, and Research.
- Show file name, kind, project, tags, and date fields relevant to the selected view.
- Do not create an issue or issue-status view.
- Use filters rather than manually adding each new file. New requirements, PRDs, meetings, and correctly tagged research notes must appear automatically.

## Validation

Before writing, check all referenced metadata keys and formula names. Quote YAML strings containing operators or special characters. After writing, validate the YAML, then open the Base in Obsidian and confirm that every view renders. If rendering fails, report the error and do not claim the Base is ready.

Use formulas only when they improve navigation; a simple, reliable view is preferred to a clever formula.
