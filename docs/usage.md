# SENTRY: Usage

## Running the pipeline

```bash
nextflow run nerettilab/SENTRY \
   -profile conda \
   --input samplesheet.csv \
   --threshold_combinations threshold_combinations.json \
   --column1 age \
   --column2 cell_type \
   --sample_column orig.ident \
   --outdir results
```

To repeat a run with the same settings, put the parameters in a YAML or JSON file and pass it
with `-params-file`:

```yaml
# params.yaml
input: "samplesheet.csv"
threshold_combinations: "threshold_combinations.json"
column1: "age"
column2: "cell_type"
sample_column: "orig.ident"
outdir: "results"
```

```bash
nextflow run nerettilab/SENTRY -profile conda -params-file params.yaml
```

> [!WARNING]
> Pass pipeline parameters on the command line or with `-params-file`, not in a config file
> given with `-c`. Use `-c` only for resource and executor settings.

Use `-r <release tag>` to pin a release so results can be reproduced,
and `-resume` to continue a run from cached steps.

## Profiles

| Profile | Use |
| --- | --- |
| `conda` | Create the software environments with conda. Recommended. |
| `mamba` | Like `conda`, using mamba to create the environments. With mamba 2, set `MAMBA_ALWAYS_YES=true` so environment creation does not wait for confirmation. |
| `test` | Run on the bundled synthetic data in `assets/test`. Combine with `conda`: `-profile test,conda`. |
| `debug` | Keep work files and print extra diagnostics. |

The `docker`, `singularity`, `podman` and similar profiles come from the nf-core template.
The pipeline does not yet provide container images, so they do not supply the required software.

## Samplesheet

`--input` is a CSV file with a header and two columns:

| Column | Description |
| --- | --- |
| `sample` | Sample name, without spaces. Used in output file names. |
| `sc_object` | Path to an AnnData `.h5ad` file, or a Seurat `.rds` file with `--seurat_input`. Relative paths are resolved from the samplesheet's folder. |

```csv
sample,sc_object
young_lung,/data/young_lung.h5ad
old_lung,old_lung.h5ad
```

Each object should contain:

- **Raw counts** in `adata.X`, `adata.raw.X` (`--use_raw`) or a layer (`--layer_name counts`).
  Model inputs, gene thresholds and signature scores are all computed from these counts.
- **Gene symbols** as `var_names`, or in an `adata.var` column given with `--var_colname`.
  Duplicate symbols are averaged into one gene.
- The `adata.obs` columns named by `--column1`, `--column2` and, if used, `--sample_column`.

If `--column1` is `age` or `development_stage`, the first number in each value is used, so
`"18m"` becomes `18` and `"3-month-old"` becomes `3`. Units are not converted, so all values
should use the same unit.

## Threshold combinations file

`--threshold_combinations` is a JSON file with two keys:

- `definitions`: named criteria, each with a `type` and its options.
- `combinations`: lists of criterion names. Each list becomes one analysis.

```json
{
  "definitions": {
    "senescence": { "type": "model", "path": "models/senescence.pkl", "taxon": 9606 },
    "cell_cycle": { "type": "cell_cycle" }
  },
  "combinations": [["senescence"], ["senescence", "cell_cycle"]]
}
```

For each combination, every cell gets one label made by joining its criteria labels with `_`
in the order listed, for example `Senescent_G1`. The labels are stored in a column named
`combination_<name1>_<name2>...`. Cells that get no label (see `model_select`) are left out of
that combination's tables and charts.

File paths inside the JSON (`path`, `gene_set_file`, `filepath`) can be absolute, or relative
to the JSON file's folder. A combination that uses a gene missing from a sample is skipped for
that sample with a warning. Each criterion is computed once per sample, even if several
combinations use it.

The older format, a list of `{ "<name>": { ...config } }` objects with one object per
combination, is still accepted.

### `model`: machine learning predictions

Applies a pickled scikit-learn classifier, such as the [SENTRY models](../models/README.md).

| Option | Required | Description |
| --- | --- | --- |
| `path` | yes | Pickled classifier with `predict` and `feature_names_in_`. |
| `taxon` | yes | NCBI taxon of the model's genes: `9606` or `10090`. If it differs from `--sample_taxon`, the data are converted through one-to-one human–mouse orthologs. |
| `rename_classes` | no | Map of predicted class to label, e.g. `{"Senescent": "Sen"}`. Unlisted classes keep their name. |
| `overwrite_classes` | no | Map of predicted class to label. Cells predicted as a listed class have the label built so far in the combination **replaced** with this label; other cells are unchanged. Useful for overriding an earlier model's call. |
| `gene_set_file` | no | Tab-separated file listing the model's features, if the model has no `feature_names_in_`. The genes must be in the order the model was trained on. |
| `gene_set_file_header` | no | Header row of `gene_set_file` (default `0`, the first row); `null` if there is none. |
| `gene_set_gene_column` | no | Column of `gene_set_file` that holds the genes (default: the first). |

The data are subset to the model's genes, with missing genes set to 0, then normalized to
10,000 counts per cell and log2-transformed (`log2(x + 1)`). Your model must be trained on data
prepared the same way, with normalization after subsetting to its genes.

> [!CAUTION]
> Pickle files can run arbitrary code when loaded. Only use models from sources you trust.

### `model_select`: keep cells of selected classes

Applies a model like `model`, but adds nothing to the label. Cells predicted as one of
`keep_classes` stay in the combination and all others are dropped. Use it to restrict the rest
of a combination to, for example, senescent cells.

| Option | Required | Description |
| --- | --- | --- |
| `path`, `taxon` | yes | As for `model`. |
| `keep_classes` | yes | List of predicted classes to keep. |

### `gene`: expression threshold

The criterion name is the gene symbol. Cells are labelled `<GENE>_pos` if their raw count is
above `threshold`, and `<GENE>_neg` otherwise.

```json
"CDKN1A": { "type": "gene", "threshold": 2 }
```

### `bins`: expression levels

Splits a gene's normalized expression (counts per 10,000, not log-transformed) into levels,
separately within each `--column2` group.

| Option | Description |
| --- | --- |
| `gene` | Gene symbol. |
| `lower_limit_percentile`, `upper_limit_percentile` | Percentiles (0–100) of the gene's expression within the group that set the lowest and highest bin edges. If the upper percentile is 0, the maximum is used. If the lower percentile is 0, the smallest non-zero value is used. |
| `num_bins` | Number of evenly spaced bin edges between the two limits. |

Labels are `<name>_lvl_<k>`, where `k` runs from `0` (below the lowest edge) to `num_bins`
(at or above the highest edge).

### `cell_cycle`: cell cycle phase

Labels cells `G1`, `S` or `G2M` with Scanpy's `score_genes_cell_cycle`, using the Tirosh et al.
(2016) S and G2/M gene lists. Expression is normalized, log-transformed and scaled first.
For mouse data (`--sample_taxon 10090`), the human genes are converted to their mouse
orthologs. No options.

### `sensig_score`: senescence signature score

Scores each cell against a gene signature from a differential expression table, following the
SenSig method (Cherry et al., 2023). Each signature gene is z-scored across cells, multiplied
by the sign of its log fold change, and the results are summed. The scores are then binned
within each `--column2` group as for `bins`, and cells are labelled `sensig_score<k>`.

| Option | Description |
| --- | --- |
| `params.filepath` | Tab-separated differential expression table. |
| `params.gene_symbol_column` | Column with gene symbols. |
| `params.log_fc_column` | Column with log fold changes. |
| `params.filter_column`, `params.threshold` | Keep genes with `filter_column < threshold`, e.g. `"FDR"` and `0.05`. Set `threshold` to `null` to keep all genes. |
| `params.new_score_column` | Name for the score column. |
| `num_bins`, `lower_limit_percentile`, `upper_limit_percentile` | Binning, as for `bins`. |

### `comparative_score`: signature score relative to another signature

Like `sensig_score`, but only uses genes of the main signature that are absent from a
competing signature or have the opposite sign there. Both tables are read with their first
column as the index.

| Option | Description |
| --- | --- |
| `main_params` | Signature options, as `params` for `sensig_score`. Its `new_score_column` is also the label prefix: cells are labelled `<new_score_column><k>`. |
| `competitor_params` | Options for the competing signature (`new_score_column` not needed). |
| `num_bins`, `lower_limit_percentile`, `upper_limit_percentile` | Binning, as for `bins`. |

## Parameters

### Required

| Parameter | Description |
| --- | --- |
| `--input` | Samplesheet CSV. |
| `--outdir` | Output directory. |
| `--threshold_combinations` | Criteria and combinations JSON. |
| `--column1` | `adata.obs` column for the first grouping level, usually a phenotype such as age. |
| `--column2` | `adata.obs` column for the second grouping level, usually cell type or tissue. |

### Optional

| Parameter | Default | Description |
| --- | --- | --- |
| `--sample_column` | none | `adata.obs` column with sample or replicate IDs. Adds per-sample tables and bar chart error bars. |
| `--sample_taxon` | `9606` | Taxon of the input data: `9606` (human) or `10090` (mouse). |
| `--use_raw` | `false` | Read counts from `adata.raw.X`. |
| `--layer_name` | none | Read counts from this layer of the object. |
| `--var_colname` | none | `adata.var` column with gene symbols. |
| `--seurat_input` | `false` | Convert Seurat `.rds` inputs to AnnData first. |
| `--save_h5ad` | `false` | Also save each annotated AnnData object. |
| `--uns_name` | `analyzed_data` | Prefix for output file names. |
| `--max_cpus`, `--max_memory`, `--max_time` | `16`, `256.GB`, `240.h` | Upper limits for any single task. |
| `--publish_dir_mode` | `link` | How results are placed in `--outdir`. Use `copy` if the work directory is on a different file system. |

Run `nextflow run nerettilab/SENTRY --help --validationShowHiddenParams` for every parameter.

## Resources

`PREPROCESS_ADATA` loads each object into memory as a dense matrix, so its memory use grows
with cells × genes. It requests up to `--max_memory` (256 GB by default) and retries with more
memory once if it runs out. Lower `--max_memory` to fit your machine, or see the
[Nextflow configuration docs](https://www.nextflow.io/docs/latest/config.html) to set resources
for individual processes with `-c`.

## Seurat input

With `--seurat_input`, each `.rds` file is converted to AnnData with
[sceasy](https://github.com/cellgeni/sceasy), using the counts of the `RNA` assay. Seurat v5
objects are converted to the v3 assay format first.
