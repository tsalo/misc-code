# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 12:20:21 2014

@author: tsalo
"""
import pickle
import inspect
import os

code_dir = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
par_dir = os.path.dirname(code_dir)

task_order = [[['AX', 'RISE', 'Kirby', 'Decimal'],
               ['AX', 'RISE', 'Decimal', 'Kirby'],
               ['AX', 'Kirby', 'RISE', 'Decimal'],
               ['AX', 'Kirby', 'Decimal', 'RISE'],
               ['AX', 'Decimal', 'RISE', 'Kirby'],
               ['AX', 'Decimal', 'Kirby', 'RISE'],
               ['RISE', 'AX', 'Kirby', 'Decimal'],
               ['RISE', 'AX', 'Decimal', 'Kirby'],
               ['RISE', 'Kirby', 'AX', 'Decimal'],
               ['RISE', 'Kirby', 'Decimal', 'AX'],
               ['RISE', 'Decimal', 'AX', 'Kirby'],
               ['RISE', 'Decimal', 'Kirby', 'AX'],
               ['Kirby', 'AX', 'RISE', 'Decimal'],
               ['Kirby', 'AX', 'Decimal', 'RISE'],
               ['Kirby', 'RISE', 'AX', 'Decimal'],
               ['Kirby', 'RISE', 'Decimal', 'AX'],
               ['Kirby', 'Decimal', 'AX', 'RISE'],
               ['Kirby', 'Decimal', 'RISE', 'AX'],
               ['Decimal', 'AX', 'RISE', 'Kirby'],
               ['Decimal', 'AX', 'Kirby', 'RISE'],
               ['Decimal', 'RISE', 'AX', 'Kirby'],
               ['Decimal', 'RISE', 'Kirby', 'AX'],
               ['Decimal', 'Kirby', 'AX', 'RISE'],
               ['Decimal', 'Kirby', 'RISE', 'AX']],
              [['RISE', 'AX', 'Kirby', 'Decimal'],
               ['RISE', 'AX', 'Decimal', 'Kirby'],
               ['RISE', 'Kirby', 'AX', 'Decimal'],
               ['RISE', 'Kirby', 'Decimal', 'AX'],
               ['RISE', 'Decimal', 'AX', 'Kirby'],
               ['RISE', 'Decimal', 'Kirby', 'AX'],
               ['Kirby', 'AX', 'RISE', 'Decimal'],
               ['Kirby', 'AX', 'Decimal', 'RISE'],
               ['Kirby', 'RISE', 'AX', 'Decimal'],
               ['Kirby', 'RISE', 'Decimal', 'AX'],
               ['Kirby', 'Decimal', 'AX', 'RISE'],
               ['Kirby', 'Decimal', 'RISE', 'AX'],
               ['Decimal', 'AX', 'RISE', 'Kirby'],
               ['Decimal', 'AX', 'Kirby', 'RISE'],
               ['Decimal', 'RISE', 'AX', 'Kirby'],
               ['Decimal', 'RISE', 'Kirby', 'AX'],
               ['Decimal', 'Kirby', 'AX', 'RISE'],
               ['Decimal', 'Kirby', 'RISE', 'AX'],
               ['AX', 'RISE', 'Kirby', 'Decimal'],
               ['AX', 'RISE', 'Decimal', 'Kirby'],
               ['AX', 'Kirby', 'RISE', 'Decimal'],
               ['AX', 'Kirby', 'Decimal', 'RISE'],
               ['AX', 'Decimal', 'RISE', 'Kirby'],
               ['AX', 'Decimal', 'Kirby', 'RISE']],
              [['Kirby', 'AX', 'RISE', 'Decimal'],
               ['Kirby', 'AX', 'Decimal', 'RISE'],
               ['Kirby', 'RISE', 'AX', 'Decimal'],
               ['Kirby', 'RISE', 'Decimal', 'AX'],
               ['Kirby', 'Decimal', 'AX', 'RISE'],
               ['Kirby', 'Decimal', 'RISE', 'AX'],
               ['Decimal', 'AX', 'RISE', 'Kirby'],
               ['Decimal', 'AX', 'Kirby', 'RISE'],
               ['Decimal', 'RISE', 'AX', 'Kirby'],
               ['Decimal', 'RISE', 'Kirby', 'AX'],
               ['Decimal', 'Kirby', 'AX', 'RISE'],
               ['Decimal', 'Kirby', 'RISE', 'AX'],
               ['AX', 'RISE', 'Kirby', 'Decimal'],
               ['AX', 'RISE', 'Decimal', 'Kirby'],
               ['AX', 'Kirby', 'RISE', 'Decimal'],
               ['AX', 'Kirby', 'Decimal', 'RISE'],
               ['AX', 'Decimal', 'RISE', 'Kirby'],
               ['AX', 'Decimal', 'Kirby', 'RISE'],
               ['RISE', 'AX', 'Kirby', 'Decimal'],
               ['RISE', 'AX', 'Decimal', 'Kirby'],
               ['RISE', 'Kirby', 'AX', 'Decimal'],
               ['RISE', 'Kirby', 'Decimal', 'AX'],
               ['RISE', 'Decimal', 'AX', 'Kirby'],
               ['RISE', 'Decimal', 'Kirby', 'AX']]]

tp_dict = {"1- 00 Month": 0,
           "3- 12 Month": 1,
           "4- 24 Month": 2,
           }

col_beg = [1, 5, 9]
col_end = [5, 9, 13]

with open(code_dir + '/task_order.pickle', 'w') as file_:
    pickle.dump([task_order, tp_dict, col_beg, col_end], file_)

each_order = {"RISE": [[['A'], ['A'], ['B'], ['B'], ['C'], ['C']],
                       [['B'], ['C'], ['A'], ['C'], ['A'], ['B']],
                       [['C'], ['B'], ['C'], ['A'], ['B'], ['A']]],
              "AX": [[['1']],
                     [['1']],
                     [['1']]],
              "Kirby": [[['1']],
                        [['1']],
                        [['1']]],
              "Decimal": [[['Messy first'], ['Rounded first']],
                          [['Rounded first'], ['Messy first']],
                          [['Messy first'], ['Rounded first']]],
              }

with open(code_dir + '/each_order.pickle', 'w') as file_:
    pickle.dump(each_order, file_)

task_info = {"RISE": {"file": code_dir + "\\rise_trialsheet.csv",
                      "col_beg": [1, 2, 3],
                      "col_end": [2, 3, 4],
                      },
             "AX": {"file": code_dir + "\\ax_trialsheet.csv",
                    "col_beg": [1, 2, 3],
                    "col_end": [2, 3, 4]},
             "Kirby": {"file": code_dir + "\\kirby_trialsheet.csv",
                       "col_beg": [1, 2, 3],
                       "col_end": [2, 3, 4]},
             "Decimal": {"file": code_dir + "\\decimal_trialsheet.csv",
                         "col_beg": [1, 2, 3],
                         "col_end": [2, 3, 4]},
             }

with open(code_dir + '/task_info.pickle', 'w') as file_:
    pickle.dump(task_info, file_)

file_dict = {"RISE": {"A": {"Part1": par_dir + "\\RISE1_2_7.2010\RISE1_2_VersionA\\RISE1_2_PART1_VersionA.ebs2",
                            "Part2": par_dir + "\\RISE1_2_7.2010\RISE1_2_VersionA\\RISE1_2_PART2_VersionA.ebs2",
                            },
                      "B": {"Part1": par_dir + "\\RISE1_2_7.2010\RISE1_2_VersionB\\RISE1_2_PART1_VersionB.ebs2",
                            "Part2": par_dir + "\\RISE1_2_7.2010\RISE1_2_VersionB\\RISE1_2_PART2_VersionB.ebs2",
                            },
                      "C": {"Part1": par_dir + "\\RISE1_2_7.2010\RISE1_2_VersionC\\RISE1_2_PART1_VersionC.ebs2",
                            "Part2": par_dir + "\\RISE1_2_7.2010\RISE1_2_VersionC\\RISE1_2_PART2_VersionC.ebs2",
                            },
                      },
             "AX": {"1": par_dir + "\\AXCPT_CNTRACS\\EP2-AXCPT_rev3_6.24.14.ebs2",
                    },
             "Kirby": {"1": par_dir + "\\DelayDiscount\\Kirby\\KirbyDiscounting_CarterEP2_v1.ebs2",
                       },
             "Decimal": {"Messy first": par_dir + "\\DelayDiscount\\Decimal\\chooserewardSSB_Short_MessyFirst_CarterEP2_v2.ebs2",
                         "Rounded first": par_dir + "\\DelayDiscount\\Decimal\\chooserewardSSB_Short_RoundedFirst_CarterEP2_v2.ebs2",
                         },
             }

with open(code_dir + '/file_dict.pickle', 'w') as file_:
    pickle.dump(file_dict, file_)
