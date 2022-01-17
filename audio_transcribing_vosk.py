import argparse
import io
from google.oauth2 import service_account
#from pydub import AudioSegment
import os 
from google.cloud import speech
# from google.cloud.speech import enums
from google.cloud.speech_v1 import types  
import os
import sys
import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel

#import Word

import wave

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



def audio_transcribe_vosk(speech_file):

    # path to vosk model downloaded from
    # https://alphacephei.com/vosk/models
    model_path = "/home/ikom/projects/i18_messages/vosk-model-en-us-0.22-lgraph"
    model = Model(model_path)

    # name of the text file to write recognized text
    # text_filename = "/content/speech_recognition_systems_vosk_with_timestamps.txt"

    wf = wave.open(speech_file, "rb")

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []

    # recognize speech using vosk model
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)

    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    print(results)

    # forming a final string from the words
    text = ''
    for r in results:
        text += r['text'] + ' '

    print("\tVosk thinks you said:\n")
    print(text)


    for x in results[0]['result']:
        print(x)
        break

    return 0