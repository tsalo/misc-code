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
        self.thresholds = {}
        self.level = {}
        self.count = {}
        self.thresholds["dopamine"] = [0, 25, 75, 100]
        self.thresholds["noradrenaline"] = [0, 25, 75, 100]
        self.thresholds["serotonin"] = [0, 25, 75, 100]
        self.level["dopamine"] = "normal"
        self.level["noradrenaline"] = "normal"
        self.level["serotonin"] = "normal"
        self.count["dopamine"] = 1
        self.count["noradrenaline"] = 1
        self.count["serotonin"] = 1
        self.emotion = "NEUTRAL"

    def adjust_thresholds(self, neurotransmitter):
        if self.count[neurotransmitter] > 3:
            if self.level[neurotransmitter] is "low":
                print(self.name + "'s " + neurotransmitter + " levels have been " + self.level[neurotransmitter] + " lately, resulting in increased sensitivity.")
                self.thresholds[neurotransmitter][1] = self.thresholds[neurotransmitter][1] + 1
                if self.thresholds[neurotransmitter][1] >= self.thresholds[neurotransmitter][2] - 1:
                    self.thresholds[neurotransmitter][2] = self.thresholds[neurotransmitter][2] + 1
            elif self.level[neurotransmitter] is "high":
                print(self.name + "'s " + neurotransmitter + " levels have been " + self.level[neurotransmitter] + " lately, resulting in increased sensitivity.")
                self.thresholds[neurotransmitter][2] = self.thresholds[neurotransmitter][2] - 1
                if self.thresholds[neurotransmitter][2] <= self.thresholds[neurotransmitter][1] - 1:
                    self.thresholds[neurotransmitter][1] = self.thresholds[neurotransmitter][1] - 1
        if self.count[neurotransmitter] > 5:
            if self.level[neurotransmitter] is "normal" and self.thresholds[neurotransmitter][2] < self.thresholds[neurotransmitter][3] - 1 and self.thresholds[neurotransmitter][1] > self.thresholds[neurotransmitter][0] + 1:
                print(self.name + "'s " + neurotransmitter + " levels have been " + self.level[neurotransmitter] + " lately, resulting in increased resilience.")
                self.thresholds[neurotransmitter][2] = self.thresholds[neurotransmitter][2] + 1
                self.thresholds[neurotransmitter][1] = self.thresholds[neurotransmitter][1] - 1

    def add_count(self, neurotransmitter, level):
        if self.level[neurotransmitter] is level:
            self.count[neurotransmitter] = self.count[neurotransmitter] + 1
        else:
            self.count[neurotransmitter] = 1

    def adjust_levels(self, neurotransmitter, level):
        if self.status is "alive":
            if level in range(self.thresholds[neurotransmitter][0], self.thresholds[neurotransmitter][1]):
                self.add_count(neurotransmitter, "low")
                self.level[neurotransmitter] = "low"
                self.adjust_thresholds(neurotransmitter)
            elif level in range(self.thresholds[neurotransmitter][1], self.thresholds[neurotransmitter][2]):
                self.add_count(neurotransmitter, "normal")
                self.level[neurotransmitter] = "normal"
                self.adjust_thresholds(neurotransmitter)
            elif level in range(self.thresholds[neurotransmitter][2], self.thresholds[neurotransmitter][3]):
                self.add_count(neurotransmitter, "high")
                self.level[neurotransmitter] = "high"
                self.adjust_thresholds(neurotransmitter)
            else:
                print("BOOM! " + self.name + " is dead!")
                self.status = "dead"

    def set_levels(self, dopamine, noradrenaline, serotonin):
        self.adjust_levels("dopamine", dopamine)
        self.adjust_levels("noradrenaline", noradrenaline)
        self.adjust_levels("serotonin", serotonin)
        self.determine_emotion()

    def determine_emotion(self):
        """
        This needs emotions for when one or more neurotransmitters are within normal ranges.
        """
        if self.level["dopamine"] is "high" and self.level["noradrenaline"] is "high" and self.level["serotonin"] is "high":
            self.emotion = "INTEREST/EXCITEMENT"
        elif self.level["dopamine"] is "high" and self.level["noradrenaline"] is "high" and self.level["serotonin"] is "low":
            self.emotion = "ANGER/RAGE"
        elif self.level["dopamine"] is "high" and self.level["noradrenaline"] is "low" and self.level["serotonin"] is "high":
            self.emotion = "ENJOYMENT/JOY"
        elif self.level["dopamine"] is "low" and self.level["noradrenaline"] is "high" and self.level["serotonin"] is "high":
            self.emotion = "SURPRISE"
        elif self.level["dopamine"] is "high" and self.level["noradrenaline"] is "low" and self.level["serotonin"] is "low":
            self.emotion = "FEAR/TERROR"
        elif self.level["dopamine"] is "low" and self.level["noradrenaline"] is "high" and self.level["serotonin"] is "low":
            self.emotion = "CONTEMPT/DISGUST"
        elif self.level["dopamine"] is "low" and self.level["noradrenaline"] is "low" and self.level["serotonin"] is "high":
            self.emotion = "DISTRESS/ANGUISH"
        elif self.level["dopamine"] is "low" and self.level["noradrenaline"] is "low" and self.level["serotonin"] is "low":
            self.emotion = "SHAME/HUMILIATION"
        else:
            self.emotion = "NEUTRAL"