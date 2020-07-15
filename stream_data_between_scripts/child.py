import sys
import datetime

#Fonction qui va traiter la data
def treat_data_from_parent(data_from_parent_process):
    return data_from_parent_process.replace('0', '1')

#Fonction par laquelle va passer la data depuis fichier pilote
def data_stream_parent_to_child(data_from_parent_process):
    print('From child.py : ' 
          + str(treat_data_from_parent(data_from_parent_process)) #Ici on envoie la data en traîtement
          + ' Timestamp : ' 
          + str(datetime.datetime.now()))
    return "String pour illustrer la sortie de la fonction - sinon retourne 'None'"

#Code to be run when the script is explicitly called, but NOT when it's
#imported as a module in parent.py
if __name__ == '__main__':
    print('Je suis explicitement appelée avec les arguments '
          + sys.argv[1] + ' - ' + sys.argv[2])
