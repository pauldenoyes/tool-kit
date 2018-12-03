#Example in two(2) steps :
# - Get the Bearer token
# - Then post a file to be treated by a remote API

##Imports
import http.client, urllib.request, urllib.parse, urllib.error, requests

##Get the Bearer token:
headersGetBearerToken = {
                # Request headers
                'Ocp-Apim-Subscription-Key': 'myKey',
                }
paramsGetToken = urllib.parse.urlencode({
                })
try:
    conn = http.client.HTTPSConnection('end.point.url')
    conn.request("POST", "/complete/the/url/evenWithParameters", "{body}", headersGetBearerToken)
    response = conn.getresponse()
    bearer = response.read().decode('utf-8') #Car la réponse est un byte array de base (genre b'somethingHereLookingLikeAString'), for the following step you have to turn this into an utf-8 string with .decode('utf-8')
    bearerToken = str(bearer) #Not usefull anymore, could be removed
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

##Call the API that will treat the file, with the generated Bearer token
endpoint = "https://end.point.url?paramIwantToPassHardcoded=paramValue"
data = ({'files': open(r'C:\\Users\\user\\myFiles\\' + fileName, 'rb'),
        })
headers = {'Stuff-for-header': 'stuff1'; param2=stuff2/stuff2bis; param3=stuff3',
           "Authorization": "Bearer " + bearerToken,}
reponse = requests.post(endpoint,data['files'],headers=headers).json()
print(reponse['nameOfTheJsonObjectYouWantToPrint'])
data['files'].close() #Sans utilisation du "with", et dans le doute, mieux vaut fermer proprement le fichier envoyé à l'API
