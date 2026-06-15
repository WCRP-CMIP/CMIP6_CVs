# CMIP6 Controlled Vocabulary

The **CMIP6 controlled vocabularies (CVs)** repository defines the controlled vocabulary for the Coupled Model Intercomparison Project Phase 6. It specifies which terms from the [WCRP Universe](https://github.com/WCRP-CMIP/WCRP-universe) are used in CMIP6, adds project-specific metadata, and defines CMIP6 data specifications (DRS, NetCDF attributes, STAC catalog).

## How It Works: Linking to the Universe

Terms in this repository are **not self-contained** — they are lightweight references that link back to the [WCRP Universe](https://github.com/WCRP-CMIP/WCRP-universe), the shared source of truth for all WCRP vocabulary.

Each term file contains only the project-specific fields. The full definition (description, units, standard names, etc.) lives in the universe and is resolved through the JSON-LD context.

**Example — a CMIP6 variable (`variable_id/tas.json`):**
```json
{
    "@context": "000_context.jsonld",
    "id": "tas",
    "type": "variable"
}
```

The corresponding `000_context.jsonld` maps the `id` to the universe:
```json
{
    "@context": {
        "id": "@id",
        "type": "@type",
        "@base": "https://esgvoc.ipsl.fr/resource/universe/variable/"
    }
}
```

The `@base` URI tells esgvoc to resolve the full term definition from the universe. This means:
- The universe holds the **canonical definition** (description, units, standard name, etc.)
- The CMIP6 CVs declare **which terms are used** in CMIP6 and add any project-specific fields

## Repository Structure

```
CMIP6_CVs/
├── activity_id/           # MIP activities (24 terms)
├── experiment_id/         # CMIP6 experiment definitions (322 terms)
├── variable_id/           # Variables (1320 terms)
├── institution_id/        # Participating institutions (49 terms)
├── source_id/             # Model sources (134 terms)
├── frequency/             # Output frequencies
├── realm/                 # Model realms
├── grid_label/            # Grid labels
├── ...                    # 30 collections in total
├── project_specs.yaml     # Project identity and DRS name
├── drs_specs.yaml         # Data Reference Syntax specifications
├── attr_specs.yaml        # NetCDF global attribute specifications
├── catalog_specs.yaml     # STAC catalog specifications
├── esgvoc_manifest.yaml   # Version and release metadata
└── _archive/              # Archived legacy files
```

Each collection directory contains:
- `000_context.jsonld` — JSON-LD context that links terms back to the universe
- One `.json` file per term, named by its identifier

## Viewing the CVs

### esgvoc (authoritative)

[esgvoc](https://esgf.github.io/esgf-vocab/) is the authoritative tool for accessing the CVs.

```sh
# Install esgvoc
pip install esgvoc

# Get the latest release of the CMIP6 CVs
esgvoc use cmip6@latest

# Look up a specific term
esgvoc get cmip6:experiment_id:historical
```

### Quick lookup via the CLI (no install required)

```sh
# Install uv (macOS and Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Fetch the latest CMIP6 snapshot
uvx esgvoc use cmip6@latest

# Check a term
uvx esgvoc get cmip6:experiment_id:historical
```

Note: term IDs are always lowercase.

### Via the web API

- **All collections:** [https://esgvoc.ipsl.fr/api/v1/projects/cmip6/collections](https://esgvoc.ipsl.fr/api/v1/projects/cmip6/collections)
- **All terms in a collection:** `https://esgvoc.ipsl.fr/api/v1/projects/cmip6/collections/{collection_id}/terms`
- **A specific term:** `https://esgvoc.ipsl.fr/api/v1/projects/cmip6/collections/{collection_id}/terms/{term_id}`

Full API documentation: [esgvoc.ipsl.fr/api/v1/docs](https://esgvoc.ipsl.fr/api/v1/docs)

### Via the Python API

```python
import esgvoc.api as ev

cmip6_experiments = ev.get_all_terms_in_collection("cmip6", "experiment_id")
```

See the [esgvoc Python API docs](https://esgf.github.io/esgf-vocab/) for full details.

## Versioning

Version information is tracked in `esgvoc_manifest.yaml`:

```yaml
project:
  id: "cmip6"
  name: "CMIP6 Controlled Vocabulary"
cv_version: "1.0.0"
universe_version: "1.0.11"
esgvoc:
  min_version: "4.0.0"
```

The `universe_version` field indicates which version of the WCRP Universe this CV is aligned with.

## License

This work is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
