# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 10:09:49 2014
A GUI to run the behavioral appointment computer tasks.
There are currently four tasks that are performed in a counterbalanced order
based on subject ID and timepoint (baseline, 12 month follow-up, or 24 month
follow-up): RISE, AX, Delayed Discounting- Decimal, and Delayed Discounting-
Kirby. Furthermore, there are multiple versions of the RISE (A, B, C) and the
Delayed Discounting- Decimal (Messy first, Rounded first). These different
versions are also counterbalanced according to their own spreadsheets (saved in
the main folder). Necessary information about these tasks is stored as
dictionaries in several pickle files in the main folder. For readability
and easy updating, the dictionaries and pickling procedures are also stored in
a script ("behav_order.py").

To test the GUI, you need a csv file for each task matching the files defined
by task_info in behav_order.py, a csv file named task_order.csv, and files
matching the contents of file_dict in behav_order.py. If the files you want to
open are not E-Prime scripts (such as subtituting text files for an easy test),
you need to alter the function execute_file to hold while your default text
editor is open.

Dependencies: Tkinter, pandas, numpy, pickle, sys, psutil, os, subprocess, and
random.
@author: tsalo
"""
import Tkinter
import pandas as pd
import numpy as np
import pickle
import sys
import psutil
import os
import subprocess
import random


class ContinueWindow(Tkinter.Tk):
    """
    Creates a window with inputted label and three buttons, Continue, Restart,
    and Quit. Each sets response attribute to respective string.
    """
    def __init__(self, label):
        Tkinter.Tk.__init__(self)
        self.wm_title("Continue")
        self.response = "Quit"

        input_label = Tkinter.Label(self, text=label)
        input_label.grid(row=1, column=1, columnspan=5)

        continue_label = Tkinter.Label(self, text="Do you wish to move on?")
        continue_label.grid(row=2, column=1, columnspan=5)

        continue_button = Tkinter.Button(self, text="Continue",
                                         command=self.continue_)
        continue_button.grid(row=3, column=1, columnspan=1)

        restart_button = Tkinter.Button(self, text="Restart",
                                        command=self.restart)
        restart_button.grid(row=3, column=3, columnspan=1)

        quit_button = Tkinter.Button(self, text="Quit",
                                     command=self.close_window)
        quit_button.grid(row=3, column=5, columnspan=1)

    def continue_(self):
        """ Closes the GUI window."""
        self.response = "Continue"
        self.destroy()

    def restart(self):
        """ Closes the GUI window."""
        self.response = "Restart"
        self.destroy()

    def close_window(self):
        """ Closes the GUI window."""
        self.response = "Quit"
        self.destroy()


class MainWindow(Tkinter.Tk):
    """
    Main graphical user interface for behav_gui. Used to input subject ID,
    timepoint, and handedness.
    """
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.wm_title("GUI")

        id_label = Tkinter.Label(self, text="Complete Subject ID")
        id_label.grid(row=1, column=1)
        self.sub_input = Tkinter.StringVar(self)
        id_entry = Tkinter.Entry(self, bd=5, textvariable=self.sub_input)
        id_entry.grid(row=1, column=2)

        tp_label = Tkinter.Label(self, text="Timepoint")
        tp_label.grid(row=2, column=1)
        self.tp_input = Tkinter.StringVar(self)
        self.tp_input.set("")
        tp_option = Tkinter.OptionMenu(self, self.tp_input, "", "1- 00 Month",
                                       "3- 12 Month", "4- 24 Month")
        tp_option.grid(row=2, column=2)

        handed_label = Tkinter.Label(self, text="Handedness")
        handed_label.grid(row=3, column=1)
        self.handed = Tkinter.StringVar(self)
        self.handed.set("Right")
        handedness_option = Tkinter.OptionMenu(self, self.handed,
                                               "Right", "Left")
        handedness_option.grid(row=3, column=2)

        empty_label = Tkinter.Label(self, text="")
        empty_label.grid(row=4, column=2)

        done_button = Tkinter.Button(self, text="Done",
                                     command=self.close_window)
        done_button.grid(row=5, column=1, columnspan=2)

    def close_window(self, *args):
        """ Closes the GUI window."""
        del args
        if self.tp_input.get() and self.sub_input.get():
            self.destroy()
        else:
            error_message = MessageWindow("ERROR", "You need to enter a " +
                                          "subject ID and choose a timepoint.")
            error_message.mainloop()


class MessageWindow(Tkinter.Tk):
    """
    Creates a window with an inputted title and label and a close button
    labeled "Okay".
    """
    def __init__(self, title, label):
        Tkinter.Tk.__init__(self)
        self.wm_title(title)
        input_label = Tkinter.Label(self, text=label)
        input_label.grid(row=1, column=1, columnspan=5)

        okay_button = Tkinter.Button(self, text="Okay",
                                     command=self.close_window)
        okay_button.grid(row=2, column=3, columnspan=1)

    def close_window(self):
        """ Closes the GUI window."""
        self.destroy()


class OverwriteWindow(Tkinter.Tk):
    """
    Creates a window with query (Do you wish to overwrite) and two buttons, Yes
    and No. Each sets response attribute to corresponding boolean.
    """
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.wm_title("Duplicate")
        self.response = False

        overwrite_label = Tkinter.Label(self,
                                        text="Duplicate ID and TP given. Overwrite?")
        overwrite_label.grid(row=1, column=1, columnspan=5)

        yes_button = Tkinter.Button(self, text="Yes", command=self.respond_yes)
        yes_button.grid(row=2, column=2, columnspan=1)

        no_button = Tkinter.Button(self, text="No", command=self.respond_no)
        no_button.grid(row=2, column=4, columnspan=1)

    def respond_yes(self):
        """ Closes the GUI window and sets response to Yes."""
        self.response = True
        self.destroy()

    def respond_no(self):
        """ Closes the GUI window and sets response to No."""
        self.response = False
        self.destroy()


class RetryWindow(Tkinter.Tk):
    """
    Creates a window with one inputted label and two buttons- Restart and Quit.
    Each sets response attribute to corresponding boolean.
    """
    def __init__(self, label):
        Tkinter.Tk.__init__(self)
        self.wm_title("Problem")
        self.response = True

        input_label = Tkinter.Label(self, text=label)
        input_label.grid(row=1, column=1, columnspan=5)

        restart_button = Tkinter.Button(self, text="Restart",
                                        command=self.restart)
        restart_button.grid(row=2, column=1, columnspan=1)

        quit_button = Tkinter.Button(self, text="Quit", command=self.quit_)
        quit_button.grid(row=2, column=5, columnspan=1)

    def restart(self):
        """ Closes the GUI window and sets response to Restart."""
        self.response = True
        self.destroy()

    def quit_(self):
        """ Closes the GUI window and sets response to Quit."""
        self.response = False
        self.destroy()


class Subject():
    """
    Class to store subject information.
    """
    def __init__(self, subject_id, timepoint, handedness, tp_dict, all_tasks):
        self.id = subject_id
        self.tp = timepoint
        self.handed = handedness
        self.tp_dict = tp_dict
        self.all_tasks = all_tasks


def execute_file(run_file):
    """
    Opens E-Run (or other specified) file and waits for E-Run to no longer be
    in current processes before continuing.
    For debugging on a Linux machine, it is set to open the files specified and
    wait for gedit to close for the user tsalo.
    """
    if os.name == "nt":
        subprocess.call(run_file, shell=True)
    elif os.name == "posix":
        subprocess.call(("xdg-open", run_file))
        open_proc = True
        while open_proc:
            data = list(psutil.process_iter())
            open_proc = any(["gedit" in safe_name(proc) and "tsalo" in
                             safe_user(proc) for proc in data])


def get_curr_order(task_order_csv, task_order, curr_subj, overwrite):
    """
    Takes subject ID, timepoints, organization of task counterbalancing, and
    current list of task counterbalances (from csv) and returns correct order
    for given subject and timepoint, as well as updates list of lists (from
    csv).
    """
    if curr_subj.tp in curr_subj.tp_dict.keys():
        curr_order_list = task_order[curr_subj.tp_dict.get(curr_subj.tp)]
    else:
        retry_ = RetryWindow("{0} is not an acceptable timepoint.".format(curr_subj.tp))
        retry_.mainloop()
        if retry_.response:
            main()
            sys.exit()
        else:
            sys.exit()
    
    df = pd.read_csv(task_order_csv)
    df2 = df.set_index("Subject")
    
    subject_position = np.where(df2.index==curr_subj.id)[0]
    if not subject_position:
        subject_position = len(df2.index)
        df2.loc[curr_subj.id] = np.nan
    curr_order = curr_order_list[subject_position % len(curr_order_list)]
    
    if np.isnan(df2.loc[curr_subj.id,
                        "Task1_{0}".format(curr_subj.tp_dict.get(curr_subj.tp))]):
        for i_task, task in enumerate(curr_order):
            df2.loc[curr_subj.id,
                    "Task{0}_{1}".format(i_task+1,
                                         curr_subj.tp_dict.get(curr_subj.tp))] = task
        if curr_subj.all_tasks:
            message = MessageWindow("Order", "The current order is: " +
                                    ", ".join(curr_order))
            message.mainloop()
        return curr_order, df2, overwrite
    else:
        if not overwrite:
            overwrite_ = OverwriteWindow()
            overwrite_.mainloop()
            if overwrite_.response:
                overwrite = True
                if curr_subj.all_tasks:
                    message = MessageWindow("Order", "The current order is: " +
                                            ", ".join(curr_order))
                    message.mainloop()
                return curr_order, df2, overwrite
            else:
                sys.exit()
        else:
            return curr_order, df2, overwrite


def main(file_dir=None):
    """
    Runs full script (opens GUI windows, updates csvs, and opens E-Run files).
    """
    if not file_dir:
        file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    overwrite = False
    input_window = MainWindow()
    input_window.mainloop()

    with open(os.path.join(file_dir, "task_order.pickle"), "r") as file_:
        [task_order_csv, task_order, tp_dict] = pickle.load(file_)

    with open(os.path.join(file_dir, "each_order.pickle"), "r") as file_:
        each_order = pickle.load(file_)

    with open(os.path.join(file_dir, "file_dict.pickle"), "r") as file_:
        file_dict = pickle.load(file_)

    curr_subj = Subject(input_window.sub_input.get(),
                        input_window.tp_input.get(),
                        input_window.handed.get(),
                        tp_dict, True)
    curr_order, task_file, overwrite = get_curr_order(task_order_csv,
                                                      task_order,
                                                      curr_subj,
                                                      overwrite)
    task_file.to_csv(task_order_csv)

    # Loop through tasks, reading csv/getting current task type for each and
    # adding to lists of lists ind_ord (task order or type), ind_file (read-in
    # csv as list of lists), and run_file (E-Run file corresponding to specific
    # task order or type).
    ind_ord = [[] for _ in curr_order]
    ind_file = [[] for _ in curr_order]
    run_file = [[] for _ in curr_order]
    curr_subj.all_tasks = False

    for a, task in enumerate(curr_order):
        task_version_csv = file_dict.get(task).get("csv_file")
        task_version = each_order.get(task)
        ind_ord[a], ind_file[a], overwrite = get_curr_order(task_version_csv,
                                                            task_version,
                                                            curr_subj,
                                                            overwrite)
        ind_file[a].to_csv(task_version_csv, na_rep="")
        run_file[a] = search_dict(file_dict, task, ind_ord[a][0])

    message = MessageWindow("Order", "The current order is: " +
                            ", ".join("\t".join(map(str, l)) for l in ind_ord))
    message.mainloop()

    # Loop through tasks and execute files in order. Ask to continue after each
    # task finishes.
    for i_task in range(len(run_file)):
        response = "Restart"
        while response == "Restart":
            if type(run_file[i_task]) == dict:
                execute_file(run_file[i_task].get("Part1"))
                execute_file(run_file[i_task].get("Part2"))
            else:
                execute_file(run_file[i_task])

            # When run_file is closed, move on to next file.
            window_string = "{0} {1} is complete.".format(curr_order[i_task],
                                                          ind_ord[i_task])
            if i_task < (len(curr_order) - 1):
                window_string = "{0}\n{1} {2} is next.".format(window_string,
                                                               curr_order[i_task+1],
                                                               ind_ord[i_task+1])
            continue_ = ContinueWindow(window_string)
            continue_.mainloop()
            response = continue_.response

            if response == "Quit":
                sys.exit()

    message = MessageWindow("Congrats!", ("You're done. Your random number " +
                                          "is {0}").format(random.randint(1, 63)))
    message.mainloop()


def safe_name(process):
    """
    Check for names of processes in psutil.process_iter and, if
    permission denied, returns "None".
    """
    try:
        return process.name
    except Exception:
        return "None"


def safe_user(process):
    """
    Check for names of users in psutil.process_iter and, if
    permission denied, returns "None".
    """
    try:
        return process.username
    except Exception:
        return "None"


def search_dict(dictionary, *args):
    """
    Given an arbitrary number of keys, looks through nested dictionaries for
    value. Last key can be a dummy.
    """
    for i_key, key in enumerate(args):
        if key in dictionary.keys():
            if type(dictionary.get(key)) is dict:
                dictionary = dictionary.get(key)
                if i_key == len(args) - 1:
                    return dictionary
            else:
                return dictionary.get(key)
        else:
            return dictionary


if __name__ == "__main__":
    main()
