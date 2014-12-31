# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 00:34:33 2014
Emotion evaluation based on the Lovheim cube.
@author: taylorsalo
"""


class Transmitter:
    def __init__(self, name, host_name, thresholds):
        self.name = name
        self.host = host_name
        self.thresholds = thresholds
        self.level = "normal"
        self.count = 1
    
    def __adjust_thresholds(self):
        """
        Adjusts thresholds for neurotransmitter level evaluations.
        A very rudimentary function meant to reflect the effects of LTP and LTD.
        Sort of.
        """
        min_threshold = self.thresholds[0]
        low_threshold = self.thresholds[1]
        high_threshold = self.thresholds[2]
        max_threshold = self.thresholds[3]

        if self.count > 3:
            if self.level == "low":
                self.__print_statement("decreased sensitivity")
                low_threshold += 1
                if low_threshold >= high_threshold - 1:
                    high_threshold += 1
            elif self.level == "high":
                self.__print_statement("increased sensitivity")
                high_threshold -= 1
                if high_threshold <= low_threshold + 1:
                    low_threshold -= 1

        if self.count > 5:
            if (self.level == "normal" and
                high_threshold < max_threshold - 1 and
                low_threshold > min_threshold + 1):
                self.__print_statement("increased resilience")
                high_threshold += 1
                low_threshold -= 1
        
        self.thresholds[1] = low_threshold
        self.thresholds[2] = high_threshold

    def __add_count(self, level):
        """
        Counts the number of times a subject has been recorded at a given
        neurotransmitter level.
        """
        if self.level == level:
            self.count += 1
        else:
            self.count = 1

    def __print_statement(self, statement):
        """
        Prints a long line filled with info.
        """
        line = "{}'s {} levels have been {} lately, resulting in {}."
        info = [self.host, self.name, self.level, statement]
        print(line.format(*info))

    def adjust_levels(self, level):
        """
        Changes neurotransmitter level evaluations based on exact levels.
        Also counts the number of times the subject has recorded being at that
        level and what, if any, changes should be made to their thresholds.
        """
        min_threshold = self.thresholds[0]
        low_threshold = self.thresholds[1]
        high_threshold = self.thresholds[2]
        max_threshold = self.thresholds[3]

        if min_threshold <= level < low_threshold:
            self.__add_count("low")
            self.level = "low"
            self.__adjust_thresholds()
        elif low_threshold <= level < high_threshold:
            self.__add_count("normal")
            self.level = "normal"
            self.__adjust_thresholds()
        elif high_threshold<= level <= max_threshold:
            self.__add_count("high")
            self.level = "high"
            self.__adjust_thresholds()
        else:
            return False
        return True


class Emoter:
    """
    Serotonin seems to match affect (positive or negative).
    Noradrenaline seems to match arousal (low or high). Heart rate?
    Dopamine... doesn't seem to have an obvious counterpart.
    """
    def __init__(self, name):
        self.name = name
        self.is_alive = True
        transmitter_list = ["dopamine", "noradrenaline", "serotonin"]
        self.transmitters = {nt: Transmitter(nt, self.name, [0, 25, 75, 100])
                             for nt in transmitter_list}
        self.emotion = "NEUTRAL"

    def set_levels(self, values):
        """
        Set neurotransmitter levels. Different levels result in different
        emotions. Consistently high or low levels can lead to increased or
        decreased sensitivity to the neurotransmitter. 
        """
        if self.is_alive:
            for nt, level in values.iteritems():
                if not self.transmitters[nt].adjust_levels(level):
                    print("BOOM! " + self.name + " is dead!")
                    self.is_alive = False
                    break
            self.__determine_emotion()
        else:
            print("No emotion possible. Subject is dead.")
            self.emotion = "NONE"

    def __determine_emotion(self):
        """
        This needs emotions for when one or more neurotransmitters are within
        normal ranges.
        """
        levels = (self.transmitters["dopamine"].level,
                  self.transmitters["noradrenaline"].level,
                  self.transmitters["serotonin"].level)

        emotion_dict = {
            ("high", "high", "high"): "INTEREST/EXCITEMENT",
            ("high", "high", "low") : "ANGER/RAGE",
            ("high", "low",  "high"): "ENJOYMENT/JOY",
            ("low",  "high", "high"): "SURPRISE",
            ("low",  "high", "low") : "CONTEMPT/DISGUST",
            ("low",  "low",  "high"): "DISTRESS/ANGUISH",
            ("low",  "low",  "low") : "SHAME/HUMILIATION",
        }
        self.emotion = emotion_dict.get(levels, "NEUTRAL")

subject = Emoter("Subject 001")

levels_list = [[20, 80, 20],
               [20, 20, 20],
               [20, 80, 80],
               [20, 20, 80]]

for i_levels in levels_list:
    subject.set_levels({"dopamine": i_levels[0], "noradrenaline": i_levels[1], "serotonin": i_levels[2]})
    print(subject.emotion)
