import subprocess
import datetime
from child import data_stream_parent_to_child

#On streame les lignes du fichier de données 5 par 5 (ici un bout d'image BMP)
#Le input sert seulement à temporiser pour voir ce qu'il se passe
with open('file_to_stream_line_by_line.txt') as f:
    lines = f.readlines()
    for i in range(0, len(lines), 5):
        print('In parent.py - i = ' + str(i) + ' - Sending : ' + str(lines[i:i+5]) 
              + ' Timestamp : ' + str(datetime.datetime.now()))
        print(data_stream_parent_to_child(str(lines[i:i+5])))
        input("Press key to continue")

