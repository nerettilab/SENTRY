#!/usr/bin/env python
"""
Generate the small synthetic AnnData files used by `-profile test`.

The data are simulated counts, not real cells. They only exist to exercise every pipeline
step with the real SENTRY models, so predictions on them carry no biological meaning.

Run from the repository root with scanpy, anndata and scikit-learn 1.2.2 installed:

    python assets/test/make_test_data.py
"""
import pickle
from pathlib import Path

import anndata
import numpy as np
import pandas as pd
from scipy import sparse

REPO = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
N_MODEL_GENES = 1500  # most important genes of the senescence model to include
N_CELLS = {"sampleA": 300, "sampleB": 240}

rng = np.random.default_rng(2024)

with open(REPO / "models/sentry_senescent_vs_nonsenescent_rf.pkl", "rb") as f:
    model = pickle.load(f)
importance = pd.Series(model.feature_importances_, index=model.feature_names_in_).sort_values(ascending=False)
cell_cycle_genes = [g.strip() for g in open(REPO / "resources/regev_lab_cell_cycle_genes.txt", encoding="utf-8")]
genes = list(dict.fromkeys(cell_cycle_genes + ["CDKN1A", "IL6"] + list(importance.index[:N_MODEL_GENES])))

# Baseline expression per gene, plus a "program" that shifts the most important model genes
# in a subset of cells so that both model classes appear in the test output.
base_mean = rng.lognormal(mean=0.0, sigma=1.0, size=len(genes))
program_genes = [genes.index(g) for g in importance.index[:200]]


def senescent_probability(profiles: np.ndarray) -> np.ndarray:
    df = pd.DataFrame(profiles, columns=genes).reindex(columns=model.feature_names_in_, fill_value=0)
    df = np.log2(df.div(df.sum(axis=1), axis=0) * 1e4 + 1)
    return model.predict_proba(df)[:, list(model.classes_).index("Senescent")]


# For each program gene, keep whichever direction (5x up or 5x down) moves a typical cell
# further towards the model's "Senescent" class. All variants are scored in one batch.
trials = np.tile(base_mean, (2 * len(program_genes), 1))
for i, idx in enumerate(program_genes):
    trials[2 * i, idx] *= 0.2
    trials[2 * i + 1, idx] *= 5.0
proba = senescent_probability(trials).reshape(-1, 2)
program_fold_change = np.where(proba[:, 1] >= proba[:, 0], 5.0, 0.2)
program_genes.append(genes.index("CDKN1A"))
program_fold_change = np.append(program_fold_change, 5.0)


def make_sample(name: str, n_cells: int) -> anndata.AnnData:
    obs = pd.DataFrame(index=[f"{name}_cell{i}" for i in range(n_cells)])
    obs["age"] = rng.choice(["3m", "12m", "24m"], n_cells)
    obs["cell_type"] = rng.choice(["fibroblast", "endothelial/vascular"], n_cells)
    obs["orig.ident"] = rng.choice([f"{name}_rep{i}" for i in range(1, 4)], n_cells)
    # Older cells are more likely to carry the program
    p_program = obs["age"].map({"3m": 0.2, "12m": 0.4, "24m": 0.6}).to_numpy()
    in_program = rng.random(n_cells) < p_program

    library_size = rng.lognormal(mean=0.0, sigma=0.3, size=(n_cells, 1))
    mean = np.tile(base_mean, (n_cells, 1)) * library_size
    mean[np.ix_(in_program, program_genes)] *= program_fold_change
    counts = rng.negative_binomial(n=2, p=2 / (2 + mean)).astype(np.float32)
    return anndata.AnnData(X=sparse.csr_matrix(counts), obs=obs, var=pd.DataFrame(index=genes))


def predict(adata: anndata.AnnData) -> pd.Series:
    """Predict the way the pipeline does: subset to model genes, then normalize and log2."""
    df = adata.to_df().reindex(columns=model.feature_names_in_, fill_value=0)
    df = np.log2(df.div(df.sum(axis=1).replace(0, 1), axis=0) * 1e4 + 1)
    return pd.Series(model.predict(df), index=adata.obs_names)


for sample, n in N_CELLS.items():
    adata = make_sample(sample, n)
    adata.write_h5ad(OUT_DIR / f"{sample}.h5ad", compression="gzip")
    print(f"{sample}: {adata.n_obs} cells x {adata.n_vars} genes, predictions {predict(adata).value_counts().to_dict()}")
