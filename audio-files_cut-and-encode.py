import os
import soundfile as sf

####################################################
##      ENCODE AUDIO AS EXPECTED FOR THE API      ##
####################################################

suffix = '_BR16000_Mono_16BitPCM'

listOfFiles = os.listdir(r"C:\Users\user\Desktop\audios")

for k in range (0, len(listOfFiles)):
    data, samplerate = sf.read("C:\\Users\\user\\Desktop\\audios\\" + listOfFiles[k])
    #Comme on divise le samplerate par 3, si on ne veut pas qu'à la lecture on entende le fichier au ralenti, on ne va garder qu'un point sur 3
    data2 = [[data[i*3][0]] for i in range(0, (len(data)//3) - 3)]
    sf.write("C:\\Users\\user\\Desktop\\audios\\" + listOfFiles[k][:-4] + suffix + '.wav', data2, 16000, subtype = 'PCM_16')
    for i in range(0, (len(data2)//150000)):
        #150000 frames pour environ 10 secondes
        sf.write("C:\\Users\\user\\Desktop\\audios\\transformed\\" + listOfFiles[k][:-4] + suffix + str(i) + '.wav', data2[150000*i:150000*(i+1)], 16000, subtype = 'PCM_16')
    os.remove("C:\\Users\\user\\Desktop\\audios\\" + listOfFiles[k][:-4] + suffix + '.wav')
