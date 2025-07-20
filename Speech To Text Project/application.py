import speech_recognition as sr
from pydub import AudioSegment

def audio_to_text(audio_file):
    audio=AudioSegment.from_file(audio_file)
    wav_file="temp.wav"
    audio.export(wav_file,format="wav")
    recognizer=sr.Recognizer()
    with sr.AudioFile(wav_file)as file:
        audio_data=recognizer.record(file)
        try:
            text=recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "sorry, i could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request result:{e}"
        
if __name__=="__main__":
    audio_file="C:/Users/dipse/OneDrive/Desktop/data science/5th sem/Speech To Text Project/temp.wav"
    result=audio_to_text(audio_file)
    print(result)