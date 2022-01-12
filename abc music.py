from pydub import AudioSegment

from pydub.utils import make_chunks

import wavio

import numpy as np

from math import log2, pow

 

 

file = AudioSegment.from_file("flute.wav" , "wav")

chunk_length_ms = 250 # pydub calculates in millisec

parts = make_chunks(file, chunk_length_ms) #Partition the wav file into windows of 1/4 sec

 

#empty lists

n = []

p = []

notes = []

temp = []

empty= []

abc=[]

s=[]

#Export all of the individual chunks as wav files

for i, t in enumerate(parts):

    filename = "chunk{0}.wav".format(i)

    a = n.append(filename)

    t.export(filename, format="wav")

 

for i in n:

    wa = wavio.read(i)

    data = wa.data[:,0]

    w = np.fft.fft(data)

    freqs = np.fft.fftfreq(len(w))

    i = np.argmax(np.abs(w))

    freq = freqs[i]

    freq_in_hertz = abs(freq*wa.rate)

    p.append(freq_in_hertz)

    i = i+1

 

for i in p:

    A4 = 440

    C0 = A4*pow(2,-4.75)

    name = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

    h = round(12*log2(i/C0))

    octave = (h//12)

    n = round(h%12)

    s.append(name[n])

    s.append(str(octave))

    notes.append(s)

    s=[]

           

    

c=1

for i in range(len(notes)-1):

    if notes[i] == notes[i+1]:#adds to base number which reps quarter note value, and then repeats for every instance

        c+=1

    else:

        empty.append(notes[i])#add next note

        temp.append(c)

        c=1

empty.append(notes[-1])#last note

temp.append(c)#last note value

 

h=temp[0]

 

for i in range(len(empty)):

    if temp[i] == h:

        s.append(str(empty[i][0])+"'"*(int(empty[i][1])-4))

    if temp[i] < h:

        s.append(str(empty[i][0])+"'"*(int(empty[i][1])-4)+"/"+str(temp[i]))

    if temp[i] > h:

        s.append(str(empty[i][0])+"'"*(int(empty[i][1])-4)+str(temp[i])+"/4")

see=0

for i in range(len(s)):

    abc.append(s[i])

    see+=1

    if see == 3:

        abc.append("|")

        see=0

final = (' '.join(abc))

print('''

X:1

T:flute

M:3/4

L:1/4

R:flute

K:C

''',

final,)

 

print("Copy and past this into https://www.mandolintab.net/abcconverter.php to view sheet music")
