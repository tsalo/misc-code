# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 00:34:33 2014
Emotion evaluation based on the Lovheim cube.
@author: taylorsalo
"""

class Emoter:
    """
    Serotonin seems to match affect (positive or negative).
    Noradrenaline seems to match arousal (low or high). Heart rate?
    Dopamine... doesn't seem to have an obvious counterpart.
    """
    def __init__(self, name):
        self.name = name
        self.status = "alive"
        self.nts = {"dopamine": {"thresholds": [0, 25, 75, 100],
                                 "level": "normal",
                                 "count": 1},
                    "noradrenaline": {"thresholds": [0, 25, 75, 100],
                                      "level": "normal",
                                      "count": 1},
                    "serotonin": {"thresholds": [0, 25, 75, 100],
                                  "level": "normal",
                                  "count": 1}}
        self.emotion = "NEUTRAL"


    def __print_statement(self, neurotransmitter, statement):
        """
        Prints a long line filled with info.
        """
        line = "{}'s {} levels have been {} lately, resulting in {}."
        info = [self.name, neurotransmitter, self.nts[neurotransmitter]["level"], statement]
        print(line.format(*info))

    def __adjust_thresholds(self, neurotransmitter):
        """
        Adjusts thresholds for neurotransmitter level evaluations.
        A very rudimentary function meant to reflect the effects of LTP and LTD.
        Sort of.
        """
        min_threshold = self.nts[neurotransmitter]["thresholds"][0]
        low_threshold = self.nts[neurotransmitter]["thresholds"][1]
        high_threshold = self.nts[neurotransmitter]["thresholds"][2]
        max_threshold = self.nts[neurotransmitter]["thresholds"][3]

        if self.nts[neurotransmitter]["count"] > 3:
            if self.nts[neurotransmitter]["level"] == "low":
                self.__print_statement(neurotransmitter, "decreased sensitivity")
                low_threshold = low_threshold + 1
                if low_threshold >= high_threshold - 1:
                    high_threshold = high_threshold + 1
            elif self.nts[neurotransmitter]["level"] == "high":
                self.__print_statement(neurotransmitter, "increased sensitivity")
                high_threshold = high_threshold - 1
                if high_threshold <= low_threshold + 1:
                    low_threshold = low_threshold - 1
        if self.nts[neurotransmitter]["count"] > 5:
            if (self.nts[neurotransmitter]["level"] == "normal" and
                high_threshold < max_threshold - 1 and
                low_threshold > min_threshold + 1):
                self.__print_statement(neurotransmitter, "increased resilience")
                high_threshold = high_threshold + 1
                low_threshold = low_threshold - 1
        
        self.nts[neurotransmitter]["thresholds"][1] = low_threshold
        self.nts[neurotransmitter]["thresholds"][2] = high_threshold

    def __add_count(self, neurotransmitter, level):
        """
        Counts the number of times a subject has been recorded at a given
        neurotransmitter level.
        """
        if self.nts[neurotransmitter]["level"] == level:
            self.nts[neurotransmitter]["count"] = self.nts[neurotransmitter]["count"] + 1
        else:
            self.nts[neurotransmitter]["count"] = 1

    def __adjust_levels(self, neurotransmitter, level):
        """
        Changes neurotransmitter level evaluations based on exact levels.
        Also counts the number of times the subject has recorded being at that
        level and what, if any, changes should be made to their thresholds.
        """
        min_threshold = self.nts[neurotransmitter]["thresholds"][0]
        low_threshold = self.nts[neurotransmitter]["thresholds"][1]
        high_threshold = self.nts[neurotransmitter]["thresholds"][2]
        max_threshold = self.nts[neurotransmitter]["thresholds"][3]
        
        if self.status == "alive":
            if level in range(min_threshold, low_threshold):
                self.__add_count(neurotransmitter, "low")
                self.nts[neurotransmitter]["level"] = "low"
                self.__adjust_thresholds(neurotransmitter)
            elif level in range(low_threshold, high_threshold):
                self.__add_count(neurotransmitter, "normal")
                self.nts[neurotransmitter]["level"] = "normal"
                self.__adjust_thresholds(neurotransmitter)
            elif level in range(high_threshold, max_threshold):
                self.__add_count(neurotransmitter, "high")
                self.nts[neurotransmitter]["level"] = "high"
                self.__adjust_thresholds(neurotransmitter)
            else:
                print("BOOM! {} is dead!".format(self.name))
                self.status = "dead"

    def set_levels(self, dopamine, noradrenaline, serotonin):
        """
        Set neurotransmitter levels. Different levels result in different
        emotions. Consistently high or low levels can lead to increased or
        decreased sensitivity to the neurotransmitter. 
        """
        self.__adjust_levels("dopamine", dopamine)
        self.__adjust_levels("noradrenaline", noradrenaline)
        self.__adjust_levels("serotonin", serotonin)
        self.__determine_emotion()

    def __determine_emotion(self):
        """
        This needs emotions for when one or more neurotransmitters are within
        normal ranges.
        """
        levels_list = [self.nts["dopamine"]["level"],
                       self.nts["noradrenaline"]["level"],
                       self.nts["serotonin"]["level"]]
        if levels_list == ["high", "high", "high"]:
            self.emotion = "INTEREST/EXCITEMENT"
        elif levels_list == ["high", "high", "low"]:
            self.emotion = "ANGER/RAGE"
        elif levels_list == ["high", "low", "high"]:
            self.emotion = "ENJOYMENT/JOY"
        elif levels_list == ["low", "high", "high"]:
            self.emotion = "SURPRISE"
        elif levels_list == ["high", "low", "low"]:
            self.emotion = "FEAR/TERROR"
        elif levels_list == ["low", "high", "low"]:
            self.emotion = "CONTEMPT/DISGUST"
        elif levels_list == ["low", "low", "high"]:
            self.emotion = "DISTRESS/ANGUISH"
        elif levels_list == ["low", "low", "low"]:
            self.emotion = "SHAME/HUMILIATION"
        else:
            self.emotion = "NEUTRAL"

subject = Emoter("Subject 001")

subject.set_levels(20, 80, 20)
print(subject.emotion)
subject.set_levels(20, 20, 20)
print(subject.emotion)
subject.set_levels(20, 80, 80)
print(subject.emotion)
subject.set_levels(20, 20, 80)
print(subject.emotion)
