# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 14:50:17 2015

@author: tsalo
"""
import os

directory = "C:/Users/tsalo/Documents/TCANLab/MRI-tools/"
repository_name = "MRI-tools"
remove_string = "tree/master/"

for root, dirs, files in os.walk(directory):
    for file_ in files:
        if file_ == "README.md":
            with open(root + "/" + file_, "r") as fo:
                readme_data = [line.rstrip('\n') for line in fo]
                
            repo_name_index = root.index(repository_name)
            folder_name = os.path.normpath(root[repo_name_index:]).replace("\\", "/")
            new_path = folder_name.replace(remove_string, "")
            del(readme_data[0])
            readme_data[0:0] = [new_path]

            with open(root + "/" + file_, "w") as fo:
                for item in readme_data:
                    fo.write("%s\n" % item)
