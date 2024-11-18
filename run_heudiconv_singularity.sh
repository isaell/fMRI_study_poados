# to be run from /data/isabel/POADOS
# ./BIDS/code/loop_heudiconv_singularity.sh

while read i; do echo "$i"
    singularity run -B $PWD:/curdir -B /data/isabel/POADOS/dicom:/dcminput \
    /data/isabel/singularity/heudiconv-0.8.0.sif \
    -d /dcminput/{session}/{subject}_*/*/*dcm \
    -s "$i" \
    -ss pre \
    -f /curdir/BIDS/code/heuristic.py \
    -c dcm2niix -b \
    -o /curdir/BIDS/ \
    --anon-cmd /curdir/BIDS/code/convertID.py
done < participants_in.txt
