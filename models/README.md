# SENTRY pretrained models

These are the random forest classifiers used in the SENTRY paper. Both are scikit-learn
`RandomForestClassifier` objects saved with `pickle` under **scikit-learn 1.2.2**, the version
pinned in `modules/local/preprocess_adata/environment.yml`. Other scikit-learn versions may fail
to load them or give different predictions.

| File | Predicts | Classes | Trees | Max depth | SHA-256 |
| --- | --- | --- | --- | --- | --- |
| `sentry_senescent_vs_nonsenescent_rf.pkl` | Senescent vs. non-senescent | `NonSenescent`, `Senescent` | 74 | 26 | `09132d248f00b2ba7cfcbd7d82684de3081473437dbf851d27ee15ed77d18aa2` |
| `sentry_primary_vs_secondary_rf.pkl` | Primary vs. secondary senescence | `primary`, `secondary` | 382 | 24 | `9c937e417be5d93ccd2aac035aac0f998514d145f080e9504fcacac907e09bc3` |

The first model was originally saved as `binary_sen_upgraded_pie_7810947.pkl`, and the second as
`rf_full_secondary_vs_primary_classifier_sklearn_1.2.pkl`.

## Input expected by the models

- **Genes:** both models use the same 14,086 features: human gene symbols (NCBI taxon `9606`)
  that have a one-to-one mouse ortholog. Mouse data are converted automatically when you run the
  pipeline with `--sample_taxon 10090`. Genes absent from your data are filled with zeros.
- **Values:** start from raw counts. If `adata.X` is not raw counts, use `--use_raw` or
  `--layer_name`. The pipeline subsets the data to the model's genes, *then* applies
  `normalize_total(target_sum=1e4)` and `log1p(base=2)`. The models were trained with the same
  steps in the same order, so do not normalize over the whole transcriptome first.

## Using the models in the pipeline

Reference the models in your `--threshold_combinations` file, by absolute path or relative to
the JSON file's folder. If you ran the pipeline with `nextflow run nerettilab/SENTRY`, Nextflow
keeps a copy of this repository at `~/.nextflow/assets/nerettilab/SENTRY/`.
[`assets/test/threshold_combinations.json`](../assets/test/threshold_combinations.json) uses
both models with relative paths.

```json
{
  "definitions": {
    "senescence": {
      "type": "model",
      "path": "/path/to/SENTRY/models/sentry_senescent_vs_nonsenescent_rf.pkl",
      "taxon": 9606
    },
    "senescence_type": {
      "type": "model",
      "path": "/path/to/SENTRY/models/sentry_primary_vs_secondary_rf.pkl",
      "taxon": 9606
    }
  },
  "combinations": [["senescence"], ["senescence", "senescence_type"]]
}
```

Within a combination, each model's predicted label is appended in order. For example, the
second combination gives labels such as `Senescent_primary`. The primary/secondary model labels
every cell, so read its output only for cells the first model calls senescent.

## Security

`pickle` files can run arbitrary code when loaded. Only load models from sources you trust.
