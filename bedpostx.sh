#!/bin/bash

# bedpostx: local modelling of diffusion parameters

# run BEDPOSTX ~isabel/POADOS/BIDS/code/bedpostx.sh

pth="/data/isabel/POADOS/BIDS"

process(){

for i in ${pth}/sub-${1}/ses-${2}/dwi/ ; do

  cd $i
  # rename files for BEDPOSTX specification requirements
  cp eddy_corr_data.eddy_rotated_bvecs bvecs
  cp sub-${1}_ses-${2}_dir-PA_dwi.bval bvals
  cp eddy_corr_data.nii.gz data.nii.gz

  echo BEDPOSTX for sub-${1}
  bedpostx_gpu $i    # bedpostx (without gpu)

done
}

# process subject session
# process 1001 pre
# process 1003 pre
# process 1004 pre
# process 1005 pre
# process 1007 pre
# process 1008 pre
# process 1010 pre
# process 1011 pre
# process 1013 pre
# process 1014 pre
# process 1015 pre
# process 1017 pre
# process 1018 pre
# process 1019 pre
# process 1020 pre
# process 1021 pre
# process 1022 pre
# process 2001 pre
# process 2002 pre
# process 2003 pre
# process 2004 pre
# process 2009 pre
# process 4101 pre
# process 4102 pre
# process 4103 pre
# process 4104 pre
# process 4105 pre
# process 4106 pre
# process 4108 pre
# process 4109 pre
# process 4110 pre
# process 4111 pre
# process 4112 pre
# process 4113 pre
# process 4114 pre
# process 4115 pre
# process 4116 pre
# process 4117 pre
# process 4118 pre
# process 4119 pre
# process 4120 pre
# process 4121 pre
