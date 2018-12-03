import pyodbc 
myConnexion = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=MyInstance;"
                      "Database=MyDataBaseName;"
                      "Trusted_Connection=yes;") #Trusted_Connection a 'yes' va utiliser mon compte Windows (plus sécure que de passe mes credentials en clair).
                                                 #Ceci-dit on peut passer ses log/pass à la place, avec 'UID=user;PWD=password'.

cursor = myConnexion.cursor()

cursor.execute("SELECT TOP 2 * FROM MyTable WHERE myFirstColummn = ? AND mySecondColumn = ?", myFirstValue, mySecondValue)

for row in cursor: #Prendra les lignes une par une
  r = row
  print(r)    #Toute la ligne actuellement prise
  print(r[1]) #Colonne 1 de la ligne actuellement prise

#Documentation here : https://github.com/mkleehammer/pyodbc/wiki

##-----------------------------------------------------
## Marche aussi avec :

import pymssql
myConnexion = pymssql.connect(server='MyInstance', user='userName', password='myPassword', database='MyDataBaseName')
Le reste est idem
