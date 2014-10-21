# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 23:01:20 2014
A function to print time elapsed in a user-friendly string.
Example usage:
    from datetime import datetime
    import time_elapsed
    start_time = datetime.now()
    # Code here
    time_elapsed.main(start_time)
@author: taylorsalo
"""
from datetime import datetime

def main(start_time):
    time_elapsed = datetime.now() - start_time
    seconds_elapsed = time_elapsed.total_seconds()
    if seconds_elapsed >= 3600:
        hours_elapsed = seconds_elapsed / 3600
        seconds_left = seconds_elapsed % 3600
        minutes_elapsed = seconds_left / 60
        seconds_left = seconds_left % 60
        print("%d hours, %d minutes, and %d seconds elapsed." %
              (hours_elapsed, minutes_elapsed, seconds_left))
    elif seconds_elapsed >= 60:
        minutes_elapsed = seconds_elapsed / 60
        seconds_left = seconds_elapsed % 60
        print("%d minutes and %d seconds elapsed." % (minutes_elapsed,
                                                      seconds_left))
    else:
        print("%d seconds elapsed." % seconds_elapsed)
