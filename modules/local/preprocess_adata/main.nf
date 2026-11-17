process PREPROCESS_ADATA {
    label "process_high"
    label "process_high_memory"
    // Uncomment below to send to bigmem slurm partition or increase maxRetries
    // clusterOptions '-p bigmem'
    // maxRetries 3
    conda "${moduleDir}/environment.yml"

    input:
    tuple val(meta), val(original_input_file)
    val(threshold_combinations)
    val(uns_name)
    val(sample_taxon)
    val(column2)
    val(homolog_table_path)
    val(cell_cycle_genes_path)
    val(use_raw)
    val(var_colname)
    val(layer_name)
    val(save_h5ad)

    output:
    tuple val(meta), path("*_processed_data.tsv.gz"), emit: processed_tsv
    tuple val(meta), path("*_processed_data.h5ad"), emit: processed_data_file, optional: true

    script:
    def prefix = "${uns_name}_${meta.id}"
    """
    python \
    '${workflow.projectDir}/bin/preprocess_adata.py' \
    --input-file='${original_input_file}' \
    --threshold-combinations='${threshold_combinations}' \
    --output-file='${prefix}_processed_data.h5ad' \
    --name-to-add='${uns_name}' \
    --sample-taxon='${sample_taxon}' \
    --column2='${column2}' \
    --homolog-table-path='${homolog_table_path}' \
    --cell-cycle-genes-path='${cell_cycle_genes_path}' \
    --use-raw='${use_raw}' \
    --var-colname='${var_colname}' \
    --layer-name='${layer_name}' \
    --save-h5ad='${save_h5ad}'
    """
}