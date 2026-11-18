#!/usr/bin/env python
# coding: utf-8
"""
Utility functions with no uncommon library dependencies
"""
import os

class KeyDict(dict):
    """
    A dictionary that returns its key if the key is not present
    """
    def __missing__(self, key):
        return key

def str2bool(v):
    """Parse boolean string arguments for use by argparse command line inputs."""
    return str(v).lower() in ("yes", "true", "t", "y", "1")

def filter_threshold_combinations(threshold_combinations, adata, var_colname=None):
    """
    Filter threshold combinations based on gene presence in var_names.
    Args:
    threshold_combinations (dict): Dictionary of threshold combinations.
    adata (list): adata for which we want to verify contains the necessary variable names.
    var_colname (str, optional): Column name to use for var names. Defaults to None.
    Returns:
    list: Filtered threshold combinations.
    """
    if var_colname:
        var_names = set(adata.var[var_colname])  # Get variable names from var column
    else:
        var_names = set(adata.var_names)
    filtered_combinations = []
    for criteria in threshold_combinations:
        # A combination is kept only if every gene it references is present in the data
        missing_genes = []
        for criteria_name, criteria_config in criteria.items():
            if criteria_config["type"] == "gene":
                gene = criteria_name
            elif criteria_config["type"] == "bins":
                gene = criteria_config["gene"]
            else:
                continue
            if gene not in var_names:
                missing_genes.append(gene)
        if missing_genes:
            print(f"Warning: gene(s) {missing_genes} not found in the input data, "
                  f"skipping combination {list(criteria)}")
            continue
        filtered_combinations.append(criteria)
    return filtered_combinations

def convert_new_to_old_threshold_combinations(new_form_threshold_combinations):
    """
    Convert new format threshold combinations to the old format.

    The new format consists of a dictionary with two keys: 'definitions' and 'combinations'.
    'definitions' contains the configuration details for each criteria, and 'combinations'
    contains a list of lists, where each inner list represents a combination of criteria
    names.

    The old format is a list of dictionaries, where each dictionary represents a combination
    of criteria with their respective configurations.

    Args:
    new_form_threshold_combinations (dict): A dictionary in the new format with keys 'definitions' and 'combinations'.

    Returns:
    list: A list of dictionaries in the old format, where each dictionary represents a combination of criteria.
    """
    # Extract definitions and combinations from the new threshold combinations format
    definitions = new_form_threshold_combinations['definitions']
    combinations = new_form_threshold_combinations['combinations']
    
    # Initialize the old format list
    old_format = []
    
    # Iterate through each combination
    for combination in combinations:
        # Create a new dictionary for this combination
        combination_dict = {}
        
        # Add each definition to the combination dictionary
        for config_name in combination:
            combination_dict[config_name] = definitions[config_name]
        
        # Add the combination dictionary to the old format list
        old_format.append(combination_dict)
    
    return old_format

# Keys in a criteria config that hold file paths, and nested parameter blocks that can hold them
_PATH_KEYS = ("path", "gene_set_file", "filepath")
_NESTED_KEYS = ("params", "main_params", "competitor_params")


def resolve_config_paths(threshold_combinations, base_dir):
    """
    Make relative file paths in threshold combination configs absolute, relative to base_dir.

    Works on the old (list of dicts) format, after convert_new_to_old_threshold_combinations.
    Absolute paths and paths starting with "~" are left as they are, apart from expanding "~".
    """
    def resolve(config):
        for key in _PATH_KEYS:
            if isinstance(config.get(key), str):
                path = os.path.expanduser(config[key])
                config[key] = path if os.path.isabs(path) else os.path.normpath(os.path.join(base_dir, path))
        for key in _NESTED_KEYS:
            if isinstance(config.get(key), dict):
                resolve(config[key])

    for criteria in threshold_combinations:
        for criteria_config in criteria.values():
            resolve(criteria_config)
    return threshold_combinations
