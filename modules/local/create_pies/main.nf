process CREATE_PIES {
    label "process_low"
    conda "${moduleDir}/environment.yml"

    input:
    tuple val(meta), path(processed_data_file)
    val(uns_name)
    val(column1)
    val(column2)

    output:
    path("*.png")

    script:
    def prefix = "${uns_name}_${meta.id}"
    """
    Rscript \
    ${workflow.projectDir}/bin/create_pie_charts.R \
    $processed_data_file \
    "${prefix}" \
    "${column1}" \
    "${column2}" \
    "."
    """
}