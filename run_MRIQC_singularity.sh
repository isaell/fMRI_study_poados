# copy into shell from data/isabel/POADOS/

while read i; do echo "$i"
  singularity run --cleanenv \
  -B /data/isabel/POADOS/BIDS:/bidsdata:ro \
  -B /data/isabel/POADOS/BIDS/derivatives/mriqc:/out \
  /data/isabel/singularity/mriqc-0.15.2.sif \
  /bidsdata /out \
  participant --no-sub --participant_label "$i" \
  --n_procs 3 --ants-nthreads 2 --mem_gb 10 --verbose-reports
done < participants_out.txt

# if all mriqc have been run in individual subjects and now we only want to extract IQMs and generate group output
singularity run --cleanenv \
-B /data/isabel/POADOS/BIDS:/bidsdata:ro \
-B /data/isabel/POADOS/BIDS/derivatives/mriqc:/out \
/data/isabel/singularity/mriqc-0.15.2.sif \
/bidsdata /out \
group --no-sub \
--n_procs 24 --ants-nthreads 10 --mem_gb 50 --verbose-reports

# output html files can be openend using eg firefox

# possibly adapt thread usuage, e.g.
# --n_procs 3 --ants-nthreads 2 --mem_gb 10
# --cleanenv  #  That argument specifies that we want to remove the host environment from the container, e.g. use everything (python etc) from inside the container
