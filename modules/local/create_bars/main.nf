process CREATE_BARS{
    label "process_low"
    conda "${moduleDir}/environment.yml"

    input:
    tuple val(meta), path(processed_data_file)
    val(uns_name)
    val(column1)
    val(column2)

    output:
    path("*.{png,pdf,svg}")

    script:
    def prefix = "${uns_name}_${meta.id}"
    """
    python \
    ${workflow.projectDir}/bin/create_bar_charts.py \
    $processed_data_file \
    "${prefix}" \
    "${column1}" \
    "${column2}" \
    "."
    """
}