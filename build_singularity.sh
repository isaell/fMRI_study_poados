# heudiconv
singularity build ./singularity/heudiconv.sif docker://nipy/heudiconv:latest
singularity run singularity/heudiconv.sif --version
mv singularity/heudiconv.sif singularity/heudiconv-X.Y.Z.sif  # add version # currently 0.8.0

# mriqc
singularity build ./singularity/mriqc.sif docker://poldracklab/mriqc:latest
singularity run singularity/mriqc.sif --version
mv singularity/mriqc.sif singularity/mriqc-X.Y.Z.sif  # add version # currently v0.15.2

# fmriprep
singularity build ./singularity/fmriprep.sif docker://poldracklab/fmriprep:latest
singularity run singularity/fmriprep.sif --version
mv singularity/fmriprep.sif singularity/fmriprep-X.Y.Z.sif  # add version # currently 20.2.0
