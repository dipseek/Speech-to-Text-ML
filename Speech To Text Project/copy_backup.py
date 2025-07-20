import tkinter as tk
import tkinter.messagebox as messagebox
import speech_recognition as sr
import threading
import pyaudio
import wave
import os
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sentence_transformers import SentenceTransformer,util
model=SentenceTransformer('paraphrase-MiniLM-L6-v2')

class SpeechToTextApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Eval System")
        ds=pickle.load(open("preprocess_data.pkl","rb"))
        self.question=ds['question']

        self.question_text=tk.Text(self,height=10,width=100)
        self.question_text.insert(tk.END,"\n".join(f"{i+1}.{q}" for i,q in enumerate(self.question)))
        self.question_text.pack(pady=20)

        self.question_label=tk.Label(self,text="Enter Question Number:")
        self.question_label.pack()
        self.question_number=tk.Entry(self)
        self.question_number.pack(pady=10)

        self.record_button=tk.Button(self,text="Start Recording",command=self.start_recording)
        self.record_button.pack(pady=20)

        self.stop_button=tk.Button(self,text="Stop Recording",command=self.stop_recording,state=tk.DISABLED)
        self.stop_button.pack(pady=20)

        self.play_button=tk.Button(self,text="Play Recording",command=self.play_recording,state=tk.DISABLED)
        self.play_button.pack(pady=20)

        self.convert_button=tk.Button(self,text="Convert to Text",command=self.convert_audio_to_text,state=tk.DISABLED)
        self.convert_button.pack(pady=20)

        self.output_text=tk.Text(self,height=15,width=100)
        self.output_text.pack(pady=20)

        self.audio_file_path="recorded_audio.wav"
        self.recording=False

    def preprocess_text(self,text):
        text=text.lower()
        words=word_tokenize(text)
        stop_word=set(stopwords.words('english'))
        words=[i for i in words if i not in stop_word]
        stemmer=PorterStemmer()
        words=[stemmer.stem(i) for i in words]
        preprocessed_text=' '.join(words)
        return preprocessed_text

    def suggest_sections(self,ans,ds,question_number,min_suggestions=1):
        preprocessed_ans=self.preprocess_text(ans)
        ans_embedding=model.encode(preprocessed_ans)
        section_embedding=model.encode(ds['ans1'].tolist())
        similarities=util.pytorch_cos_sim(ans_embedding,section_embedding)[0]
        suggestion=None
        if question_number>=0 and question_number<len(ds):
            suggestion={
                'index':question_number,
                'question':ds.iloc[question_number]['question'],
                'ans':ds.iloc[question_number]['ans'],
                'similarity_score':similarities[question_number].item()

            }
        return suggestion
    
    def start_recording(self):
        self.recording=True
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.play_button.config(state=tk.DISABLED)
        self.convert_button.config(state=tk.DISABLED)

        self.audio=pyaudio.PyAudio()
        self.stream=self.audio.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
        self.frames=[]
        self.recording_thread=threading.Thread(target=self.record)
        self.recording_thread.start()

    def record(self):
        while self.recording:
            data=self.stream.read(1024)
            self.frames.append(data)
    def stop_recording(self):
        self.recording=False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        wf=wave.open(self.audio_file_path,'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b"".join(self.frames))
        wf.close()
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.NORMAL)
        self.convert_button.config(state=tk.NORMAL)

    def play_recording(self):
        os.system(f"start{self.audio_file_path}")

    def convert_audio_to_text(self):
        r=sr.Recognizer()
        with sr.AudioFile(self.audio_file_path)as source:
            audio_data=r.record(source)
            try:
                text=r.recognize_google(audio_data)
                question_number=int(self.question_number.get())-1
                ds=pickle.load(open('preprocess_data.pkl','rb'))
                if 0<=question_number<len(ds):
                    suggestion=self.suggest_sections(text,ds,question_number)
                    if suggestion:
                        output=(
                            f"Question: {suggestion['question']}\n"
                            f"Your answer:{text}\n"
                            f"Expected answer:{suggestion['ans']}\n"
                            f"Similarity score:{round(suggestion['similarity_score']*100,2)}"
                        )
                        self.output_text.insert(tk.END,output)
                    else:
                        self.output_text.insert(tk.END,"No relevent suggestion found.\n")
                else:
                    self.output_text.insert(tk.END,"Invalid question number.\n")
            except sr.UnknownValueError:
                messagebox.showwarning("Speech to text","Could not understand the audio")
            except sr.RequestError as e:
                messagebox.showwarning("Speech to text",f"Error occured:{e}")
            except ValueError:
                messagebox.showwarning("InputError","Please enter a valid question number.")

if __name__=="__main__":
    app=SpeechToTextApp()
    app.mainloop()


