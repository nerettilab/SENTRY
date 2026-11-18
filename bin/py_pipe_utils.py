#!/usr/bin/env python
# coding: utf-8
"""
Module for useful python functions/classes used in the pipeline
"""
import pickle
import scanpy as sc
import anndata
import pandas as pd
import convert_species
from simple_py_utils import KeyDict, str2bool, filter_threshold_combinations

HUMAN_TAXON = 9606
MOUSE_TAXON = 10090

def apply_model(adata: anndata.AnnData,
                model_config: str,
                homolog_table_path: str,
                return_proba: bool=False,
                return_data: bool=False):
    """
    Apply a machine learning model to the given AnnData object.

    Parameters:
        adata (AnnData): The input AnnData object.
        model_config (dict): Configuration for the machine learning model.
        homolog_table_path (str): Path to the homolog table file.
        return_proba (bool): Whether to return the predicted probabilities.
        return_data (bool): Whether to return the input AnnData object and classifier.

    Returns:
        pd.Series: The predicted values for each cell.
    """
    # Load the machine learning model from the configuration
    with open(model_config['path'], 'rb') as model_file:
        clf = pickle.load(model_file)

    # Get the taxon ID from the model configuration
    model_taxon = model_config['taxon']
    if "gene_set_file" in model_config:
        if "gene_set_file_header" in model_config:
            gene_set_header = model_config['gene_set_file_header']
        else:
            gene_set_header = 0
        # Load the gene set file
        if "gene_set_gene_column" in model_config:
            target_gene_set = pd.read_csv(model_config['gene_set_file'], sep="\t", header=gene_set_header)[model_config['gene_set_gene_column']].tolist()
        else:
            target_gene_set = pd.read_csv(model_config['gene_set_file'], sep="\t", header=gene_set_header).iloc[:, 0].tolist()
    else:
        target_gene_set = clf.feature_names_in_
    sample_taxon = adata.uns['sample_taxon']
    # Check if the model taxon matches the sample taxon
    if model_taxon != sample_taxon:
        print("Warning: model taxon is not the same as the sample taxon, converting sample taxon to model taxon for prediction")

        # Load the homolog table
        homolog_table = pd.read_csv(homolog_table_path, sep="\t")

        # Get the ID-to-symbols dictionary and compatible genes
        id2symbols, _, _ = convert_species.get_id2symbols_dict(homolog_table)
        compatible_genes, reverse_translate_dict = convert_species.get_compatible_genes(id2symbols)

        # compatible_genes maps human -> mouse symbols, reverse_translate_dict maps mouse -> human.
        # Build the one-to-one dictionary in the sample -> model direction.
        if (sample_taxon, model_taxon) == (MOUSE_TAXON, HUMAN_TAXON):
            one2one_dict = convert_species.get_one_to_one_only(reverse_translate_dict, compatible_genes)
        elif (sample_taxon, model_taxon) == (HUMAN_TAXON, MOUSE_TAXON):
            one2one_dict = convert_species.get_one_to_one_only(compatible_genes, reverse_translate_dict)
        else:
            raise ValueError(
                f"Cannot convert genes from taxon {sample_taxon} to taxon {model_taxon}; "
                f"only human ({HUMAN_TAXON}) and mouse ({MOUSE_TAXON}) are supported.")

        # Convert the AnnData object to the model taxon
        adata = convert_species.convert_species_one2one_adata(adata, one2one_dict, target_genes=target_gene_set)
    else:
        # Subset to the model's genes in the model's order, filling genes missing from the data with 0
        adata_df = adata.to_df().reindex(columns=target_gene_set, fill_value=0)
        adata = anndata.AnnData(adata_df)

    # Normalize and log-transform the AnnData object
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata, base=2)

    # Make predictions using the machine learning model
    if return_proba:
        if return_data:
            return pd.DataFrame(clf.predict_proba(adata.to_df()), index=adata.obs_names.copy()), adata, clf
        return pd.DataFrame(clf.predict_proba(adata.to_df()), index=adata.obs_names.copy())
    if return_data:
        return pd.Series(clf.predict(adata.to_df()), index=adata.obs_names.copy()), adata, clf
    return pd.Series(clf.predict(adata.to_df()), index=adata.obs_names.copy())