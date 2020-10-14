import datetime, time
import random

""" Script #1 treating data from j0.py
"""

#Function that treats data sent from j0.py
def treat_data_from_j0(data_from_parent_process):
    output = data_from_parent_process * 3
    return output

#Function that get data that j0.py 'sends'
def stream_data_from_j0(data_from_parent_process=None):
    return treat_data_from_j0(data_from_parent_process)

if __name__ == '__main__':
    #What is herunder is being runned only when the script is explicitly called (through a command line "python script.py" for instance)
    #Else it's ignored (for instance if you import the script, it's ignored)
    pass
