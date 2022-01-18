import os
import sys
import wave
import json

from vosk import Model, KaldiRecognizer, SetLogLevel

# Call fuction sent path to speech file as parameter
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


#     for x in results[0]['result']:
#         print(x)
#         break

    return 0
