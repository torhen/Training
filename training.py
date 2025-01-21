import pygame
from gtts import gTTS
import tkinter as tk 
from tkinter import Tk, Label, Button
from tkinter import scrolledtext
import time, pathlib

data = """
5 Start
15 Training beginnt
30 Rechtes Bein zum Po
30 Noch 30 Sekunden
15 Rechtes Bein nach hinten
15 Noch 15 Sekunden
15 Linkes Bein zum Po
15 Noch 15 Sekunden
15 Linkes Bein nach hinten
15 Noch 15 Sekunden
15 Rechtes Bein anwinkeln und Fuss bewegen
15 Noch 15 Sekunden
15 Rechtes Bein nach hinten
15 Noch 15 Sekunden
15 Linkes Bein anwinkeln und Fuss bewegen
15 Noch 15 Sekunden
15 Linkes Bein nach hinten
15 Noch 15 Sekunden
15 Rechtes Bein Spinne
15 Noch 15 Sekunden
15 Linkes Bein Spinne
15 Noch 15 Sekunden
15 Langsame Kniebeugen
15 Noch 15 Sekunden
15 Rumpfbeugen
15 Noch 15 Sekunden
15 Kniebeugen
15 Noch 15 Sekunden
15 Rumpfbeugen
15 Noch 15 Sekunden
15 Rumpfkreisen rechts herum
15 Rumpfkreisen links herum
15 Am Türrahmen abstützen und hoch und runter
15 Noch 15 Sekunden
15 Armkreisen rechts
15 Noch 15 Sekunden
15 Armkreisen links
15 Noch 15 Sekunden
15 Rechte Hand an Türrahmen drücken
15 Noch 15 Sekunden
15 Linke Hand an Türrahmen drücken
15 Noch 15 Sekunden
15 Kopfkreisen rechts herum
15 Kopfkreisen links herum
30 Auf alle viere gehen und langsam absitzen
30 Noch 30 Sekunden
15 Gewicht nach hinten verlagern
15 Noch 15 Sekunden
15 Auf allen vieren Rücken nach oben und unten
60 Rückentraining beginnen
60 noch 3 Minuten
60 noch 2 Minuten
60 noch 1 Minute
60 auf Stuhl setzen und Rücken hängen lassen
45 Meditation vorbereiten
300 Meditation beginnen
300 noch 5 min
10  Ende der Übung
"""
class Speech:
    def __init__(self):
        self.count = 0
        pygame.mixer.init()  # Reinitialize

    def make_sample(self, text, file):
        tts = gTTS(text=text, lang="de")
        tts.save(file)

    def output_sample(self, sample_path):
        pygame.mixer.music.load(sample_path)
        pygame.mixer.music.play()


    # def speak(self, text):
    #     tts = gTTS(text=text, lang="de")
    #     self.count += 1
    #     file = f"output{self.count % 2}.mp3"
    #     tts.save(file)

    #     pygame.mixer.music.load(file)
    #     pygame.mixer.music.play()


        # while pygame.mixer.music.get_busy():
        #     continue




class Root(Tk):
    def __init__(self):
        super().__init__()

        self.sec = 0
        self.running = False
        self.count_down = 0

        self.data = []
        self.prepare_data()

        self.speech = Speech()

        self.l1 = Label(font=('', 30))
        self.l1.pack()

        self.button1 = Button(self, text='Start', command=self.toggle)
        self.button1.pack()

        self.text1 = scrolledtext.ScrolledText(self, height = 40)
        self.draw()
        self.text1.bind("<Double-Button-1>", self.jump_to_line)

        self.text1.pack()
        self.t_old = time.time()

        # create all samples
        self.create_all_samples()

        self.update()

    def create_all_samples(self):
        pathlib.Path('tmp').mkdir(exist_ok=True)
        for i, entry in enumerate(self.data):
            ts, dur, excercise, flag = entry
            sample_file = 'tmp/sample_' + str(i).zfill(3) + '.mp3'
            print('creating sample', sample_file)
            self.speech.make_sample(excercise, sample_file)
        print('all samples created', sample_file)

    def jump_to_line(self, event):
        # Get the index of the clicked position
        index = self.text1.index(tk.CURRENT)  # Get the index of the current cursor position
        line_number = int(index.split('.')[0]) - 1  # Extract the line number
        print(f"Double-clicked on line: {line_number}")


        # set timer back, enabmle all entries
        ts, dur, excercise, flag = self.data[line_number]
        self.sec = ts
        for i in range(len(self.data)):
            if i < line_number:
                self.data[i][3] = 0
            else:
                self.data[i][3] = 1


    def draw(self):
        l = data.split('\n')
        l = [s for s in l if len(s) > 0]

        res = ''
        for entry in l:
            res = res + entry + '\n'

        self.text1.insert(tk.INSERT, res)


    def highlight(self, line):
        # Define a bold font
        bold_font = ("Arial", 10, "bold")

        # Apply a tag to the second line
        bold_line = line

        # Define a tag with bold font and red color
        self.text1.tag_add("bold", f"{bold_line}.0", f"{bold_line}.end")
        self.text1.tag_config("bold", font=bold_font, foreground="white", background='black')

    def prepare_data(self):
        l = data.split('\n')
        l = [s for s in l if len(s) > 0]
        sec_cum = 0
        for entry in l:
            dur, txt = entry.split(maxsplit=1)
            self.data.append([sec_cum, int(dur), txt, 1])
            sec_cum += int(dur)
        # print(self.data)

    def toggle(self):
        if self.running == True:
            self.running = False
            self.button1.config(text='Continue')
        else:
            self.running = True
            self.button1.config(text='Pause')


    def update(self):
        self.t_new = time.time()
        dt = self.t_new - self.t_old 
        self.t_old = self.t_new
        self.action(dt)
        self.after(100, self.update)

    def action(self, dt):

        # Schnelldurchlauf
        # dt = dt * 10

        if self.running == False:
            return
        self.sec = self.sec + dt

        # update counter display
        self.count_down = self.count_down - dt
        if self.count_down >= 0:
            self.l1.config(text=f"{self.count_down:.0f}")
        else:
            self.l1.config(text="0")


        # run through list, if entry is over time and not unflagged then play sample
        for i in range(len(self.data)):
            ts, dur, excercise, flag = self.data[i]

            if self.sec > ts and flag > 0:
                print(self.data[i])
                self.data[i][3] = 0 # flag to avoid retransmission
                self.highlight(i + 1)
                self.count_down = dur
                sample_file = 'tmp/sample_' + str(i).zfill(3) + '.mp3'
                self.speech.output_sample(sample_file)


root = Root()
root.mainloop()





