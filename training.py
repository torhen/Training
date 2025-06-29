import pygame
from gtts import gTTS
import tkinter as tk 
from tkinter import Tk, Label, Button
from tkinter import scrolledtext
import time, pathlib

data_as_text = """
5 Start
30 Rechtes Knie vorbereiten
30 Noch 30 Sekunden
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
30 Im Sitzen nach vorn beugen
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


class ScrollText(tk.scrolledtext.ScrolledText):
        def __init__(self, parent, data):
            self.parent = parent
            self.data = data
            super().__init__()
            self.bind("<Double-Button-1>", self.jump_to_line)

        def set_data(self, data):
            self.data = data


        def draw(self, data_as_text):
            l = data_as_text.split('\n')

            l = [s for s in l if len(s) > 0]

            res = ''
            for entry in l:
                res = res + entry + '\n'

            self.insert(tk.INSERT, res)


        def jump_to_line(self, event):
            # Get the index of the clicked position
            index = self.index(tk.CURRENT)  # Get the index of the current cursor position
            line_number = int(index.split('.')[0]) - 1  # Extract the line number
            print(f"Double-clicked on line: {line_number}")


            # set timer back, enabmle all entries
            ts, dur, excercise, flag = self.data[line_number]
            self.parent.sec = ts
            for i in range(len(self.data)):
                if i < line_number:
                    self.data[i][3] = 0
                else:
                    self.data[i][3] = 1

            if self.parent.running == False:
                self.parent.toggle()


        def highlight(self, line):
            # Define a bold font
            bold_font = ("Arial", 10, "bold")

            # Apply a tag to the second line
            bold_line = line

            # Define a tag with bold font and red color
            self.tag_add("bold", f"{bold_line}.0", f"{bold_line}.end")
            self.tag_config("bold", font=bold_font, foreground="white", background='black')


class Root(Tk):
    def __init__(self):
        super().__init__()
        self.title('Training')
        self.geometry('800x800')

        self.sec = 0
        self.running = False
        self.count_down = 0

        self.data = self.prepare_data(data_as_text)

        self.speech = Speech()

        self.l1 = Label(font=('', 30))
        self.l1.pack()

        self.button1 = Button(self, text='Start', command=self.toggle)
        self.button1.pack()

        self.text1 = ScrollText(self, self.data)
        self.text1.pack(expand=True, fill='both')
        self.text1.draw(data_as_text)

        self.t_old = time.time()

        #create all samples if needed
        flag_path = 'tmp/finished.txt'
        if not pathlib.Path(flag_path).is_file():
            self.create_all_samples()
            with open(flag_path,'w') as fin:
                fin.write('finished the speech samples')

        self.update()

    def create_all_samples(self):
        pathlib.Path('tmp').mkdir(exist_ok=True)
        for i, entry in enumerate(self.data):
            ts, dur, excercise, flag = entry
            sample_file = 'tmp/sample_' + str(i).zfill(3) + '.mp3'
            print('creating sample', sample_file)
            self.speech.make_sample(excercise, sample_file)
        print('all samples created', sample_file)

    def prepare_data(self, data_as_text):
        l = data_as_text.split('\n')
        l = [s for s in l if len(s) > 0]
        sec_cum = 0
        res = []
        for entry in l:
            dur, txt = entry.split(maxsplit=1)
            res.append([sec_cum, int(dur), txt, 1])
            sec_cum += int(dur)
        return res
    
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
                self.text1.highlight(i + 1)
                self.count_down = dur
                sample_file = 'tmp/sample_' + str(i).zfill(3) + '.mp3'
                self.speech.output_sample(sample_file)

if __name__ == '__main__':
    root = Root()
    root.mainloop()





