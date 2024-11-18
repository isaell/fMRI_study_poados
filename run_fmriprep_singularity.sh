
# current version 20.2.0
# run as ./BIDS/code/run_fmriprep.sh from /data/isabel/POADOS

while read i; do echo "$i"
  singularity run --cleanenv -B /data/isabel/POADOS:/base \
  /data/isabel/singularity/fmriprep-20.2.0.sif \
  /base/BIDS /base/BIDS/derivatives \
  participant --participant_label "$i" \
  --nthreads 20 --omp-nthreads 10 \
  -w /base/fmriprep_work_20_2_0 \
  --ignore slicetiming --use-aroma \
  --fs-license-file /base/BIDS/license.txt
done < participants_out.txt

# note: it seems like the ability to pass arguments to the singularity folder with -B will be
# removed at some point with another possibility to do that. Get that currently as a warning.
# Can then go back to using direct complete folder and file names

# possible adaptations:
# --skull-strip-template  # in ANTs, select template for skull-striping with antsBrainExtraction
# --fd-spike-threshold    # estimating confounds
# --dvars-spike-threshold # both threshold for flagging a frame as outlier based on FD or stand. DVARS
# --use-aroma             # option for running ICA-aroma
