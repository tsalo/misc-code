# -*- coding: utf-8 -*-
"""
Created on Thu Oct 30 11:17:39 2014
Searches FEAT design.fsf files for a list (really a dict) of settings.
Returns "True" if the settings match and the actual value if they don't.
@author: tsalo
"""

import os
from glob import glob
import csv
import re
import collections as cl


def string_check(text_file, string_dict):
    out = []
    for i_string in string_dict.keys():
        if i_string in open(text_file).read():
            out.append("True")
        else:
            search_term = re.compile(string_dict.get(i_string))
            search_results = re.findall(search_term, open(text_file).read())
            out.append(search_results[0])

    return out

search_path = "/whatever/feat_dirs/"
out_file = "/whatever/output.csv"

# Ensure that search term keys are listed in alphabetical order.
search_dict = {"set fmri(mc) 1": "set fmri\(mc\) (\d)",
               "set fmri(paradigm_hp) 200": "set fmri\(paradigm_hp\) (\d+)",
               "set fmri(reghighres_dof) 6": "set fmri\(reghighres_dof\) (\d+)",
               "set fmri(regstandard_dof) 12": "set fmri\(regstandard_dof\) (\d+)",
               "set fmri(regunwarp_yn) 1": "set fmri\(regunwarp_yn\) (\d)",
               "set fmri(smooth) 7": "set fmri\(smooth\) (\d+)",
               "set fmri(st) 0": "set fmri\(st\) (\d)",
               "set fmri(temphp_yn) 1": "set fmri\(temphp_yn\) (\d)",
               "set fmri(unwarp_dir) y": "set fmri\(unwarp_dir\) (\w)",
               }
search_odict = cl.OrderedDict(sorted(search_dict.items(),
                                     key=lambda t: t[0]))

# Make this as specific as necessary to get a list of subjects with design.fsf
# files.
all_subject_files = glob(search_path + "C4*/design.fsf")
all_subject_dirs = [os.path.split(i)[0] for i in all_subject_files]
all_subjects = [os.path.split(i)[-1] for i in all_subject_dirs]

# Code to randomly sample a subset. Not really necessary here.
#sample_size = 50
#rand_subject_files = [all_subject_files[i] for i in
#                      sorted(random.sample(xrange(len(all_subject_files)),
#                                           sample_size))]
#rand_subject_dirs = [os.path.split(i)[0] for i in rand_subject_files]
#rand_subjects = [os.path.split(i)[-1] for i in rand_subject_dirs]

out_list = [["Subject", "MC 1", "Paradigm_Hp 200", "RegHighRes_DOF 6",
             "RegStandard_DOF 12", "RegUnwarp 1", "Smooth 7", "ST 0",
             "TempHp 1", "Unwarp_Dir y"
             ]]

for i, i_subj in enumerate(all_subjects):
    design_file = all_subject_dirs[i] + "/design.fsf"
    check = string_check(design_file, search_odict)
    out_check = [i_subj] + check
    out_list.append(out_check)

with open(out_file, "wb") as f:
    writer = csv.writer(f)
    writer.writerows(out_list)
