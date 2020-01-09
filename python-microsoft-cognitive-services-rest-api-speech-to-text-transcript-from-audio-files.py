#Python code to call the speech-to-text REST API proposed by Microsoft Cognitive services. It will extract the text transcript of a
#bunch of audio files. You need a subscription to this service (that can be free under certain conditions)
#You also need to encode the files under the appropriate .wav format, for instance bit-rate 16000, Mono, 16 bit.

import requests
import os

#List of file names to treat
listOfFiles = os.listdir(r'C:\Users\user\myFiles')

#Personal credentials and endpoints
subscription_key = 'MySubscriptionKey'
api_end_point = 'https://westus.api.cognitive.microsoft.com/sts/v1.0'

#Get the bearer token. Here we get it through a function, because the token expires pretty rapidly, you may need to regenerate it often,
#and a function will make that easier
def get_token():
    fetch_token_url = api_end_point + '/issueToken'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    response = requests.post(fetch_token_url, headers=headers)
    return response.text
bearer_access_token = get_token()

#Call the speech-to-text Microsoft API with the bearer token to extract text from audio files
api_end_point = 'https://westus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-EN' #Here specify the appropriate cultural
headers = {'Authorization': 'Bearer ' + bearer_access_token,
           'Host': 'westus.stt.speech.microsoft.com',}
Text_vs_AudioFileName = []
for fileName in listOfFiles:
    with open(r'C:\\Users\\user\\myFiles\\' + fileName, 'rb') as data:
        r = requests.post(url = api_end_point, data = data, headers=headers).json()     #Send POST request and store the reply in 'r', converted in JSON format
        extracted_text = r['DisplayText']   #Extract text from the JSON reply
        Text_vs_AudioFileName.append([extracted_text, fileName])
print(Text_vs_AudioFileName)
