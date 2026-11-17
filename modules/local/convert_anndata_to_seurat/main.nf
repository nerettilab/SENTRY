process CONVERT_ANNDATA_TO_SEURAT{
    label "process_low"
    label "process_high_memory"
    conda "${moduleDir}/environment.yml"

    input:
    tuple val(meta), val(original_input_file)

    output:
    tuple val(meta), path("*.rds"), emit: converted_rds_file

    script:
    """
    Rscript \
    '${moduleDir}/convert_anndata_seurat_sceasy.R' \
    '${original_input_file}' \
    \$CONDA_PREFIX
    """
}