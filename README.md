# My Latex CV

Resume built from a single YAML source of truth.

## Usage

```sh
make build        # regenerates main.tex from data.yaml and compiles main.pdf
make generate     # only regenerates main.tex
```

Both targets run the generator via `uv run`, which installs the `PyYAML`
dependency declared in `pyproject.toml` on first use. `generate` runs
`generate.py`; `build` additionally compiles `main.tex` with `pdflatex`.
Just have `uv` (and a LaTeX distribution) installed.

## Structure

- `data.yaml` — the resume content. This is the file to edit.
- `generate.py` — renders `data.yaml` into a single `main.tex` with the preamble and every section.
- `main.tex` — generated artifact, committed so the repo compiles without Python.
- `Makefile` — `generate` / `build` targets.

## Section schema

| YAML key               | Rendered section          |
| ---------------------- | ------------------------- |
| `intro`                | header / contact table    |
| `experience`           | Experience                |
| `projects`             | Projects                  |
| `education`            | Education                 |
| `leadership_awards`    | Leadership and Awards     |
| `skills`               | Technical Skills          |

Omit a top-level key to skip generating that section. LaTeX macros (e.g. `\href`,
`\bullet`) are written directly into YAML string values.