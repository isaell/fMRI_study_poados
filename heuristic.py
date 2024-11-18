import os

def create_key(template, outtype=('nii.gz',), annotation_classes=None):

    if template is None or not template:
            raise ValueError ('Template must be a valid format string')
    return template, outtype, annotation_classes

def infotodict(seqinfo):

    print(seqinfo)

    t1w = create_key('sub-{subject}/{session}/anat/sub-{subject}_{session}_T1w')
    dwi1 = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_dir-PA_dwi')
    dwi2 = create_key('sub-{subject}/{session}/dwi/sub-{subject}_{session}_dir-AP_dwi')
    ExpPain1 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-ExpPain_run-1_bold')
    ExpPain2 = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-ExpPain_run-2_bold')
    SponPain = create_key('sub-{subject}/{session}/func/sub-{subject}_{session}_task-SponPain_bold')

    info = {t1w: [], dwi1: [], dwi2: [], ExpPain1: [], ExpPain2: [], SponPain: []}

    for s in seqinfo:
        if (s.dim3 == 176) and ('T1' in s.series_description) and not s.is_derived:
            info[t1w] = [s.series_id] # assign if a single series meets criteria

        # this is the main DWI data (phase encoding P>>A)
        if (s.dim3 == 4620) and (s.dim4 == 1) and ('DWI' in s.series_description):
            info[dwi1] = [s.series_id] # append if multiple series meet criteria
        # this is the short sequence that acquires data in reverse phase encoding (A>>P)
        if (s.dim3 == 140) and (s.dim4 == 1) and ('DWI' in s.series_description):
            info[dwi2] = [s.series_id]

        # in ExpPain paradigm, participants may have aborted scans that we do not want but also different durations of real scans
        if (s.dim3 >= 15000) and ('fmri_ExpPain-1' in s.series_description):   # (s.dim3 == 16716) would be currently entire duration
            info[ExpPain1] = [s.series_id]

        if (s.dim3 >= 15000) and ('fmri_ExpPain-2' in s.series_description):
            info[ExpPain2] = [s.series_id]

        if (s.dim3 == 11508) and ("fmri_SponPain" in s.series_description):
            info[SponPain] = [s.series_id]

    return info
