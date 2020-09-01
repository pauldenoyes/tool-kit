import datetime, time
import random

""" Script #1 treating data from j0.py
"""
script_output_frequency = 2.5   #In seconds
script_run_duration = 10        #In seconds

#Function that treats data sent from j0.py
def treat_data_from_j0(data_from_parent_process):
    #Randomly returs 0 or 1 every script_output_frequency seconds
    then = datetime.datetime.now() + datetime.timedelta(seconds=script_run_duration)
    while then > datetime.datetime.now():
        output = random.randint(1,101)
        if output > 50:
            output = 0
        else:
            output = 1000
        yield output
        time.sleep(script_output_frequency)

#Fonction qui récupère les données que fusion_main envoie pour cette modalité
def stream_data_from_j0(data_from_parent_process=None):
    return treat_data_from_j0(data_from_parent_process)

if __name__ == '__main__':
    #What the script does when it's not explicitly called (i.e. not when imported)
    pass
