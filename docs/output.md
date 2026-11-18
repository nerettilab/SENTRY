# SENTRY: Output

All paths below are relative to `--outdir`. In file names, `<prefix>` is `--uns_name`
(default `analyzed_data`), `<sample>` is the `sample` column of the samplesheet, and
`<combination>` is the criterion names of a combination joined with `_`.

## `preprocessed/`

- `<prefix>_<sample>_processed_data.tsv.gz`: one row per cell. Contains the original
  `adata.obs` columns, the cell cycle scores (`S_score`, `G2M_score`, `phase`), any signature
  score columns, and one `combination_<combination>` column per combination holding each
  cell's label. Cells excluded from a combination (for example by `model_select`) are empty.
- `<prefix>_<sample>_processed_data.h5ad`: the same annotations added to the full AnnData
  object. Only written with `--save_h5ad`.

## `group/`

Two tab-separated tables per sample and combination, used to draw the charts.

- `<prefix>_<sample>_<combination>_gene_combinations.tsv`: one row per `column1` value ×
  `column2` value × label.
- `<prefix>_<sample>_<combination>_gene_combinations_with_sample.tsv`: the same, also split by
  `--sample_column`. Without `--sample_column` it is identical to the first table.

| Column | Meaning |
| --- | --- |
| `<column1>`, `<column2>` | The two grouping variables. |
| `<combination>` | The cell label. |
| `<sample_column>` | Sample ID (`_with_sample` table only). |
| `count` | Number of cells in the row's group with this label. |
| `Proportion_<column2>_Per_<column1>` | Fraction of the `column1` group's cells that belong to this `column2` group. Computed over all samples together. |
| `Proportion_<combination>_Per_<column1>_AND_<column2>_Combination` | Fraction of the `column1` × `column2` group's cells with this label. In the `_with_sample` table this is computed within each sample. |

## `pie_charts/`

- `<prefix>_<sample>_<combination>_pie.png`: a grid with one pie per `column1` × `column2`
  group (columns: `column1`, rows: `column2`). Slices show the proportion of each label. A
  pie's size grows with the share of the `column1` group's cells in that `column2` group, on a
  log scale.

## `bar_charts/`

- `<prefix>_<sample>_<column2 value>_<combination>_bar_chart.svg`: one chart per `column2`
  value. Bars show the proportion of each label (colour) at each `column1` value (x axis).
  With `--sample_column`, bar heights are means across samples and error bars are 95%
  confidence intervals across samples. Characters that are unsafe in file names, such as `/`,
  are replaced with `_` in `<column2 value>`.

## `multiqc/`

- `multiqc_report.html`: a run summary with the parameters used, software versions and a
  suggested methods description.

## `pipeline_info/`

- Nextflow's `execution_report_*.html`, `execution_timeline_*.html`, `execution_trace_*.txt`
  and `pipeline_dag_*.html`, which show run times, resource use and the workflow graph.
- `nf_core_pipeline_software_mqc_versions.yml`: software versions collected during the run.
- `params_*.json`: the parameters used.
