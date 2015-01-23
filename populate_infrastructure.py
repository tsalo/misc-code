# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 21:40:45 2015
Copies new infrastructure string from INFRASTRUCTURE.md in specified folder and
populates changes across all README.md files in folder and subfolders.
@author: taylorsalo
"""

import os

infrastructure_file = "C:/Users/tsalo/Documents/TCANLab/MRI-tools/INFRASTRUCTURE.md"
start_line = "<!-- Start infrastructure -->"
end_line = "<!-- End infrastructure -->"

with open(infrastructure_file, "r") as fo:
    infrastructure = [line.rstrip('\n') for line in fo]

folder, _ = os.path.split(infrastructure_file)

for root, dirs, files in os.walk(folder):
    for file_ in files:
        if file_ == "README.md":
            with open(root + "/" + file_, "r") as fo:
                readme_data = [line.rstrip('\n') for line in fo]

            start_index = readme_data.index(start_line)
            end_index = readme_data.index(end_line)
            del(readme_data[start_index:end_index + 1])
            readme_data[start_index:start_index] = infrastructure

            with open(root + "/" + file_, "w") as fo:
                for item in readme_data:
                    fo.write("%s\n" % item)
