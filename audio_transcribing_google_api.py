import argparse
import io
from google.oauth2 import service_account

import os 
from google.cloud import speech
# from google.cloud.speech import enums
from google.cloud.speech_v1 import types  


def audio_transcribe_gtts(speech_file):
    
    credentials = service_account.Credentials.from_service_account_file('api-key-new.json')
    dict1=dict()
    print("Start")
    
    #speech_file='/content/drive/MyDrive/stt and time stamp/out0.wav'
    language='en'

    print("checking credentials")
        
    client = speech.SpeechClient(credentials=credentials)


    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()
                
    print("audio file read")    
        
    audio = speech.RecognitionAudio(content=content)



    
    a = wave.open(speech_file,"rb")
    print('Frame Rate:',a.getframerate())      
    
    
    print("config start")
    # return 0
    # config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,language_code=language,enable_word_time_offsets=True)
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                                    language_code=language,
                                    enable_word_time_offsets=True,
                                    enable_automatic_punctuation=True,
                                    max_alternatives=1)

    print("Recognizing:")
    response = client.recognize(config=config, audio=audio) 
    print("Recognized")

    # streaming_config = speech.StreamingRecognitionConfig(
    #         config=config, interim_results=True)

    for result in response.results:
        #print('inside')
        alternative = result.alternatives[0]
        print('Transcript: {}'.format(alternative.transcript))
        transcript=alternative.transcript

