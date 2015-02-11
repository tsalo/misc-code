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

Dependencies: Tkinter, csv, pickle, sys, psutil, os, subprocess, random, and
inspect.
@author: tsalo
"""
import Tkinter
import csv
import pickle
import sys
import psutil
import os
import subprocess
import random
import inspect


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

        self.mainloop()

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
    and No. Each sets response attribute to respective string.
    """
    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.wm_title("Duplicate")
        self.response = False

        overwrite_label = Tkinter.Label(self,
                                        text="Duplicate ID and TP given. " +
                                             "Overwrite?")
        overwrite_label.grid(row=1, column=1, columnspan=5)

        yes_button = Tkinter.Button(self, text="Yes", command=self.respond_yes)
        yes_button.grid(row=2, column=2, columnspan=1)

        no_button = Tkinter.Button(self, text="No", command=self.respond_no)
        no_button.grid(row=2, column=4, columnspan=1)

        self.mainloop()

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
    Each sets response attribute to respective string.
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

        self.mainloop()

    def restart(self):
        """ Closes the GUI window and sets response to Restart."""
        self.response = True
        self.destroy()

    def quit_(self):
        """ Closes the GUI window and sets response to Quit."""
        self.response = False
        self.destroy()


class Subject():
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


def get_curr_order(task_order_csv, task_order, curr_subj,
                   col_beg, col_end, overwrite):
    """
    Takes subject ID, timepoints, organization of task counterbalancing, and
    current list of task counterbalances (from csv) and returns correct order
    for given subject and timepoint, as well as updates list of lists (from
    csv).
    """
    with open(task_order_csv, "r") as file_:
        task_file = list(csv.reader(file_, delimiter=','))

    subjects = [row[0] for row in task_file]

    if curr_subj.tp in curr_subj.tp_dict.keys():
        curr_order_list = task_order[curr_subj.tp_dict.get(curr_subj.tp)]
    else:
        if RetryWindow(str(curr_subj.tp) +
                       " is not an acceptable timepoint.").response:
            run_script()
            sys.exit()
        else:
            sys.exit()

    # Find row corresponding to subject in csv. If subject is new, append an
    # empty row to fill in.
    try:
        subj_pos = subjects.index(curr_subj.id)
    except Exception:
        subj_pos = len(subjects)
        task_file.append([""] * len(task_file[0]))

    # If correct position in spreadsheet is empty, fill in with correct list.
    # Else, offer option to overwrite or quit.
    curr_order = curr_order_list[(subj_pos-1) % len(curr_order_list)]
    if not task_file[subj_pos][col_beg[curr_subj.tp_dict.get(curr_subj.tp)]]:
        task_file[subj_pos][0] = curr_subj.id
        task_file[subj_pos][col_beg[curr_subj.tp_dict.get(curr_subj.tp)]:
                            col_end[curr_subj.tp_dict.get(
                                    curr_subj.tp)]] = curr_order
        if curr_subj.all_tasks:
            message = MessageWindow("Order", "The current order is: " +
                                    ", ".join(curr_order))
            message.mainloop()
        return curr_order, task_file, overwrite
    else:
        if overwrite == 0:
            if OverwriteWindow().response:
                overwrite = 1
                if curr_subj.all_tasks:
                    message = MessageWindow("Order", "The current order is: " +
                                            ", ".join(curr_order))
                    message.mainloop()
                return curr_order, task_file, overwrite
            else:
                sys.exit()
        else:
            return curr_order, task_file, overwrite


def run_script():
    """
    Runs full script (opens GUI windows, updates csvs, and opens E-Run files).
    """
    code_dir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    par_dir = os.path.dirname(code_dir)
    task_order_csv = par_dir + "\\task_order.csv"
    overwrite = 0
    input_window = MainWindow()
    input_window.mainloop()

    with open(par_dir + "\\task_order.pickle") as file_:
        [task_order, tp_dict, col_beg, col_end] = pickle.load(file_)

    with open(par_dir + "\\each_order.pickle") as file_:
        each_order = pickle.load(file_)

    with open(par_dir + "\\task_info.pickle") as file_:
        task_info = pickle.load(file_)

    with open(par_dir + "\\file_dict.pickle") as file_:
        file_dict = pickle.load(file_)

    curr_subj = Subject(input_window.sub_input.get(),
                        input_window.tp_input.get(),
                        input_window.handed.get(),
                        tp_dict, True)
    curr_order, task_file, overwrite = get_curr_order(task_order_csv,
                                                      task_order,
                                                      curr_subj,
                                                      col_beg,
                                                      col_end,
                                                      overwrite)
    with open(task_order_csv, "wb") as file_:
        file_ = csv.writer(file_)
        for row in task_file:
            file_.writerow(row)

    # Loop through tasks, reading csv/getting current task type for each and
    # adding to lists of lists ind_ord (task order or type), ind_file (read-in
    # csv as list of lists), and run_file (E-Run file corresponding to specific
    # task order or type).
    ind_ord = [[] for _ in curr_order]
    ind_file = [[] for _ in curr_order]
    run_file = [[] for _ in curr_order]
    curr_subj.all_tasks = False

    for a, task in enumerate(curr_order):
        task_order_csv = task_info.get(task).get("file")
        task_order = each_order.get(task)
        col_beg = task_info.get(task).get("col_beg")
        col_end = task_info.get(task).get("col_end")
        ind_ord[a], ind_file[a], overwrite = get_curr_order(task_order_csv,
                                                            task_order,
                                                            curr_subj,
                                                            col_beg,
                                                            col_end,
                                                            overwrite)
        with open(task_order_csv, "wb") as file_:
            file_ = csv.writer(file_)
            for row in ind_file[a]:
                file_.writerow(row)

        run_file[a] = search_dict(file_dict, task, ind_ord[a][0])

    message = MessageWindow("Order", "The current order is: " +
                            ", ".join("\t".join(map(str, l)) for l in ind_ord))
    message.mainloop()

    # Loop through tasks and execute files in order. Ask to continue after each
    # task finishes.
    for iTask in range(len(run_file)):
        response = "Restart"
        while response == "Restart":
            if type(run_file[iTask]) == dict:
                execute_file(run_file[iTask].get("Part1"))
                execute_file(run_file[iTask].get("Part2"))
            else:
                execute_file(run_file[iTask])

            # When run_file is closed, move on to next file.
            if iTask < (len(curr_order) - 1):
                response = ContinueWindow(curr_order[iTask] + " " + 
                                          str(ind_ord[iTask]) +
                                          " is complete.\n" +
                                          curr_order[iTask+1] + " " +
                                          str(ind_ord[iTask+1]) + 
                                          " is next.").response
            else:
                response = ContinueWindow(curr_order[iTask] + " " +
                                          str(ind_ord[iTask]) +
                                          " is complete.").response

            if response == "Quit":
                sys.exit()

    message = MessageWindow("Congrats!",
                            "You're done. Your random number is " +
                            str(random.randint(1, 63)))
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
    for iKey, Key in enumerate(args):
        if Key in dictionary.keys():
            if type(dictionary.get(Key)) is dict:
                dictionary = dictionary.get(Key)
                if iKey == len(args) - 1:
                    return dictionary
            else:
                return dictionary.get(Key)
        else:
            return dictionary


if __name__ == "__main__":
    run_script()
