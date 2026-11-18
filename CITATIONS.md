# SENTRY: Citations

## SENTRY

> Hinthorn S, Rocha A, Neretti N. SENTRY: An AI Framework for Identifying and Characterizing Primary and Secondary Senescence. (in preparation)

## [Nextflow](https://pubmed.ncbi.nlm.nih.gov/28398311/)

> Di Tommaso P, Chatzou M, Floden EW, Barja PP, Palumbo E, Notredame C. Nextflow enables reproducible computational workflows. Nat Biotechnol. 2017 Apr 11;35(4):316-319. doi: 10.1038/nbt.3820. PubMed PMID: 28398311.

## [nf-core](https://pubmed.ncbi.nlm.nih.gov/32055031/)

The pipeline is built on the nf-core template.

> Ewels PA, Peltzer A, Fillinger S, Patel H, Alneberg J, Wilm A, Garcia MU, Di Tommaso P, Nahnsen S. The nf-core framework for community-curated bioinformatics pipelines. Nat Biotechnol. 2020 Mar;38(3):276-278. doi: 10.1038/s41587-020-0439-x. PubMed PMID: 32055031.

## Pipeline tools

- [Scanpy](https://doi.org/10.1186/s13059-017-1382-0)

  > Wolf FA, Angerer P, Theis FJ (2018). "Scanpy: large-scale single-cell gene expression data analysis." Genome Biology, 19(1):15. doi:10.1186/s13059-017-1382-0.

- [scikit-learn](https://jmlr.org/papers/v12/pedregosa11a.html)

  > Pedregosa F, Varoquaux G, Gramfort A, Michel V, Thirion B, Grisel O, Blondel M, Prettenhofer P, Weiss R, Dubourg V, Vanderplas J, Passos A, Cournapeau D, Brucher M, Perrot M, Duchesnay É (2011). "Scikit-learn: Machine Learning in Python." Journal of Machine Learning Research, 12:2825-2830.

- [pandas](https://doi.org/10.25080/Majora-92bf1922-00a)

  > McKinney W (2010). "Data Structures for Statistical Computing in Python." Proceedings of the 9th Python in Science Conference, 56-61. doi:10.25080/Majora-92bf1922-00a.

- [seaborn](https://doi.org/10.21105/joss.03021)

  > Waskom ML (2021). "seaborn: statistical data visualization." Journal of Open Source Software, 6(60):3021. doi:10.21105/joss.03021.

- [ggplot2](https://ggplot2.tidyverse.org)

  > Wickham H (2016). ggplot2: Elegant Graphics for Data Analysis. Springer-Verlag New York. ISBN 978-3-319-24277-4.

- [MultiQC](https://pubmed.ncbi.nlm.nih.gov/27312411/)

  > Ewels P, Magnusson M, Lundin S, Käller M. MultiQC: summarize analysis results for multiple tools and samples in a single report. Bioinformatics. 2016 Oct 1;32(19):3047-8. doi: 10.1093/bioinformatics/btw354. Epub 2016 Jun 16. PubMed PMID: 27312411; PubMed Central PMCID: PMC5039924.

## Seurat input conversion (`--seurat_input`)

- [sceasy](https://github.com/cellgeni/sceasy)

  > Cakir B, Prete M, Huang N, van Dongen S, Pir P, Kiselev VY (2020). "Comparison of visualization tools for single-cell RNAseq data." NAR Genomics and Bioinformatics, 2(3):lqaa052. doi:10.1093/nargab/lqaa052.

- [Seurat](https://doi.org/10.1038/s41587-023-01767-y)

  > Hao Y, Stuart T, Kowalski MH, Choudhary S, Hoffman P, Hartman A, Srivastava A, Molla G, Madad S, Fernandez-Granda C, Satija R (2023). "Dictionary learning for integrative, multimodal and scalable single-cell analysis." Nature Biotechnology. doi:10.1038/s41587-023-01767-y.

## Methods and bundled resources

- Mouse–human homology table (`resources/HOM_MouseHumanSequence.rpt`), from the [Mouse Genome Informatics (MGI)](https://www.informatics.jax.org/downloads/reports/index.html#homology) database, The Jackson Laboratory. Used to convert genes between human and mouse.

  > Baldarelli RM, Smith CL, Ringwald M, Richardson JE, Bult CJ; Mouse Genome Informatics Group (2024). "Mouse Genome Informatics: an integrated knowledgebase system for the laboratory mouse." Genetics, 227(1):iyae031. doi:10.1093/genetics/iyae031.

- Cell cycle genes (`resources/regev_lab_cell_cycle_genes.txt`), used for the `cell_cycle` criterion.

  > Tirosh I, Izar B, Prakadan SM, et al. (2016). "Dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq." Science, 352(6282):189-196. doi:10.1126/science.aad0501.

- Senescence signature (SenSig) scores, used for the `sensig_score` and `comparative_score` criteria.

  > Cherry C, Andorko JI, Krishnan K, et al. (2023). "Transfer learning in a biomaterial fibrosis model identifies in vivo senescence heterogeneity and contributions to vascularization and matrix production across species and diverse pathologies." GeroScience. doi:10.1007/s11357-023-00785-7.

## Software packaging

- [Bioconda](https://pubmed.ncbi.nlm.nih.gov/29967506/)

  > Grüning B, Dale R, Sjödin A, Chapman BA, Rowe J, Tomkins-Tinch CH, Valieris R, Köster J; Bioconda Team. Bioconda: sustainable and comprehensive software distribution for the life sciences. Nat Methods. 2018 Jul;15(7):475-476. doi: 10.1038/s41592-018-0046-7. PubMed PMID: 29967506.

- [conda-forge](https://doi.org/10.5281/zenodo.4774216)

  > conda-forge community (2015). The conda-forge Project: Community-based Software Distribution Built on the conda Package Format and Ecosystem. Zenodo. doi:10.5281/zenodo.4774216.
