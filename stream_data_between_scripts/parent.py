import subprocess
import datetime
from child import data_stream_parent_to_child

command = ['python', 'child.py', '2525', '5252']

#On lance l'execution du script qui traitera la data dans un sous-process
process_1 = subprocess.Popen(command, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             universal_newlines=True)

#On streame les lignes du fichier de données 5 par 5 (ici un bout d'image BMP)
#Le input sert seulement à temporiser pour voir ce qu'il se passe
with open('fichier_a_streamer_ligne_a_ligne.txt') as f:
    lines = f.readlines()
    for i in range(0, len(lines), 5):
        print('In parent.py - i = ' + str(i) + ' - Sending : ' + str(lines[i:i+5]) 
              + ' Timestamp : ' + str(datetime.datetime.now()))
        print(data_stream_parent_to_child(str(lines[i:i+5])))
        input("Press key to continue")

#Close process
process_1.terminate()
