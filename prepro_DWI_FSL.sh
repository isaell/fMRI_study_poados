#!/bin/bash

# preprocessing diffusion-weighted data

# dir-PA: main data (phase encoding P>>A)
# dir-AP: cor. data (phase encoding A>>P)

# requirement: use > FSL 6 (here, v 6.0.4)

# Isabel Ellerbrock, 2020

pth="/data/isabel/POADOS/BIDS"

process(){

for i in ${pth}/sub-${1}/ses-${2}/dwi/ ; do
  echo Preprocessing sub-${1}
  cd $i

  # # running preparations for movement and distortion corrections: topup and eddy

  # for topup, create merged b0 file (from both blip up and blip down runs)
  # here, I use the first vols (b0) to separate them from the rest
  fslroi sub-${1}_ses-${2}_dir-PA_dwi nodif 0 1
  fslroi sub-${1}_ses-${2}_dir-AP_dwi nodif_AP 0 1

  # then, merge the two b0 files into one and call them PA_AP_b0
  fslmerge -t PA_AP_b0.nii.gz nodif nodif_AP

  # if neccessary, check header info or number of vols etc, e.g.
  # fslinfo PA_AP_b0.nii.gz

  # create acquisition parameter file:
  # Number of lines equals the number of volumes used for field map calc. (here, 2, as 1 b0 per sequence was used)
  # 0 1 0 ETL # main data (phase encoding P>>A)
  # 0 -1 0 ETL # cor. data (phase encoding A>>P)
  # Where ETL (seconds) is the EPI echo train length that is calculated as follows:
  # DWI: ETL=(((ny*0.5 + num.overscan)/R) -1)*esp
  # look into json files to get information needed, e.g.
  # vi sub-2001_ses-pre_dir-PA_dwi.json
  # ny - AcquisitionMatrix PE
  # esp - Effective Echo Spacing (s)
  # R - acceleration factor ( default = 2)
  # num.overscan - partial FT imaging (default = 16)
  # here, ETL=0.023736.

  # print ETL matrix to file.for POADOS,that is: .
  printf "0 1 0 0.023736\n0 -1 0 0.023736" > acq.txt

  # running topup
  echo Running topup for sub-${1}
  topup --imain=PA_AP_b0 --datain=acq.txt --config=b02b0.cnf --out=topup_PA_AP_b0 --iout=topup_PA_AP_b0_iout

  # preparations for eddy current correction:
  # generate a brain mask using the corrected b0. We compute the average image of the corrected b0 volumes
  fslmaths topup_PA_AP_b0_iout -Tmean nodif
  # run BET on the averaged b0, creating a binary brain mask, with a fraction intensity threshold of 0.2/0.3/0.4
  bet2 nodif nodif_brain -m -f 0.3
  echo Brain mask created for sub-${1}

  # create index file for eddy which line/of the lines in the acq.txt file (from topup) are relevant for data passed into eddy
  # here, 66 is the number of vols in the main data set. See above on how to determine number of vols.
  indx=""
  for ((j=1; j<=66; j+=1)); do indx="$indx 1"; done
  echo $indx > index.txt

  ## run eddy current correction
  echo Running eddy for sub-${1}
  eddy_cuda9.1 --imain=sub-${1}_ses-${2}_dir-PA_dwi --mask=nodif_brain_mask --acqp=acq.txt --index=index.txt \
               --bvecs=sub-${1}_ses-${2}_dir-PA_dwi.bvec --bvals=sub-${1}_ses-${2}_dir-PA_dwi.bval  \
               --topup=topup_PA_AP_b0 --repol --estimate_move_by_susceptibility --out=eddy_corr_data

  # run eddy current correction QC for data quality control
  echo Running eddy QC for sub-${1}
  eddy_quad eddy_corr_data -idx index.txt -par acq.txt -m nodif_brain_mask -b sub-${1}_ses-${2}_dir-PA_dwi.bval

  ## fitting diffusion tensors
  # input: distortion-corrected data, bvals, bvecs that are rotated by motions, and a brain mask
  echo Fitting diffusion tensors for sub-${1}
  dtifit --data=eddy_corr_data --mask=nodif_brain_mask --bvecs=eddy_corr_data.eddy_rotated_bvecs \
         --bvals=sub-${1}_ses-${2}_dir-PA_dwi.bval --out=sub-${1} --wls

  echo Preprocessing done for sub-${1}

done
}

# process subject session
process 1001 pre
process 1003 pre
process 1004 pre
process 1005 pre
process 1007 pre
process 1008 pre
process 1010 pre
process 1011 pre
process 1013 pre
process 1014 pre
process 1015 pre
process 1017 pre
process 1018 pre
process 1019 pre
process 1020 pre
process 1021 pre
process 1022 pre
process 2001 pre
process 2002 pre
process 2003 pre
process 2004 pre
process 4101 pre
process 4102 pre
process 4103 pre
process 4104 pre
process 4105 pre
process 4106 pre
process 4108 pre
process 4109 pre
process 4110 pre
process 4111 pre
process 4112 pre
process 4113 pre
process 4114 pre
process 4115 pre
process 4116 pre
process 4117 pre
process 4118 pre
process 4119 pre
process 4120 pre
process 4121 pre
