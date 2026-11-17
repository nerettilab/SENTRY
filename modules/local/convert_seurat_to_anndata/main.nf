process CONVERT_SEURAT_TO_ANNDATA{
    label "process_low"
    label "process_high_memory"
    conda "${moduleDir}/environment.yml"

    input:
    tuple val(meta), val(original_input_file)

    output:
    tuple val(meta), path("*.h5ad"), emit: converted_h5ad_file

    script:
    """
    Rscript \
    '${moduleDir}/convert_seurat_anndata_sceasy.R' \
    '${original_input_file}' \
    \$CONDA_PREFIX
    """
}