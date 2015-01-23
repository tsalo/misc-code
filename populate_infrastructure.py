# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 21:40:45 2015
Copies new infrastructure string from INFRASTRUCTURE.md in specified folder and
populates changes across all README.md files in folder and subfolders.
Also updates the first header of each README with the correct path in case the
README has been moved recently.

Caveat: INFRASTRUCTURE.md must be in the base folder of the repository.
@author: taylorsalo
"""

import os

infrastructure_file = "C:/Users/tsalo/Documents/TCANLab/MRI-tools/INFRASTRUCTURE.md"
repository_name = os.path.basename(os.path.normpath(os.path.dirname(infrastructure_file)))

start_line = "<!-- Start infrastructure -->"
end_line = "<!-- End infrastructure -->"

remove_string = "tree/master/"

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
            
            repo_name_index = root.index(repository_name)
            folder_name = os.path.normpath(root[repo_name_index:]).replace("\\", "/")
            new_path = folder_name.replace(remove_string, "")
            del(readme_data[0])
            readme_data[0:0] = [new_path]

            with open(root + "/" + file_, "w") as fo:
                for item in readme_data:
                    fo.write("%s\n" % item)
