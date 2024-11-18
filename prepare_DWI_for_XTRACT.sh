# register diffusion (native) space to standard space for XTRACT

# Isabel Ellerbrock, April 2021

# https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/XTRACT

pth="/data/isabel/POADOS/BIDS"

process(){

for T1_file in ${pth}/sub-${1}/ses-${2}/anat/sub-${1}_ses-${2}_T1w.nii.gz; do
  cp -n $T1_file ${pth}/sub-${1}/ses-${2}/dwi.bedpostX/

  cd ${pth}/sub-${1}/ses-${2}/dwi.bedpostX

  # skull-strip T1w image
  bet2 sub-${1}_ses-${2}_T1w T1w_brain -f 0.3
  echo T1 brain mask created for sub-${1}

# Registration from diffusion space to standard space is a two-step process,
# using a mid-point reference of a structural T1 image and concatenating the two steps to minimize resampling
#    Step 1: Brain-extracted B0 images (nodif_brain) are transformed into structural space.
#    Step 2: Same as structural registration - FLIRT + FNIRT from structural to standard

  # Diff to T1 (linear registration)
  flirt -in nodif_brain -ref T1w_brain -omat xfms/diff2str.mat # -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12 -cost corratio
  convert_xfm -omat xfms/str2diff.mat -inverse xfms/diff2str.mat

  # T1 to standard (linear registration)
  flirt -in T1w_brain -ref ${FSLDIR}/data/standard/MNI152_T1_2mm_brain -omat xfms/str2standard.mat  # -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12 -cost corratio
  convert_xfm -omat xfms/standard2str.mat -inverse xfms/str2standard.mat

  # concatenate and create inverse
  convert_xfm -omat xfms/diff2standard.mat -concat xfms/str2standard.mat xfms/diff2str.mat
  convert_xfm -omat xfms/standard2diff.mat -inverse xfms/diff2standard.mat
  echo linear registration mats produced for sub-${1}

  # T1 to standard (nonlinear registration)
  fnirt --in=sub-${1}_ses-${2}_T1w --aff=xfms/str2standard.mat --cout=xfms/str2standard_warp --config=T1_2_MNI152_2mm
  invwarp -w xfms/str2standard_warp -o xfms/standard2str_warp -r T1w_brain
  echo inverse warp done for sub-${1}

  convertwarp -o xfms/diff2standard -r ${FSLDIR}/data/standard/MNI152_T1_2mm -m xfms/diff2str.mat -w xfms/str2standard_warp
  convertwarp -o xfms/standard2diff -r nodif_brain_mask -w xfms/standard2str_warp --postmat=xfms/str2diff.mat
  echo convert warp done for sub-${1}

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
