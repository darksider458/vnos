#!/usr/bin/python3

from picamera import PiCamera
from time import gmtime, strftime
from guizero import App, PushButton, Text, Picture
import webbrowser
import pyaudio
import wave

audio = pyaudio.PyAudio()

form_1 = pyaudio.paInt16
chans = 1
samp_rate = 44100
chunk = 4096
record_secs = 4
dev_index = 2 
wav_outpu_filename = 'test.wav'



record = False

camera = PiCamera()
camera.resolution = (800,400)
camera.hflip = True

def start_cam():
    camera.start_preview(fullscreen=False, window = (300, 100, 600, 400))
def stop_cam():
    camera.stop_preview()

output = ""

def take_pictuere():
    global output
    output = strftime("/home/pi/Desktop/Vnos/image-%d-%m %H:%M:-%S.png", gmtime())
    camera.capture(output)

def open_file():
    path = "/home/pi/Desktop/Vnos"
    webbrowser.open(path)

def playFile():
    CHUNK = 1024


    wf = wave.open('test.wav', 'rb')

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()


     
def talk():
    
    stream = audio.open(format = form_1, rate = samp_rate,channels = 1, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer = chunk)
    
    frames = []
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        try:
            data = stream.read(chunk,exception_on_overflow = False)
            frames.append(data)
            
        except IOError:
            pass

    wavefile = wave.open(wav_outpu_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    ##############################
    stream.stop_stream()
    stream.close()
    audio.terminate()

    playFile()
    
app = App("Purge",800,400,layout="grid")
starts_cam = PushButton(app, start_cam, text="Start Camera",grid=[0,0])
stops_cam = PushButton(app, stop_cam, text="stop Camera",grid=[0,1])
picture = PushButton(app, take_pictuere, text="Take Screens",grid=[0,2])
folder = PushButton(app, open_file, text="open photo folder",grid=[0,3])
talk = PushButton(app, talk, text = "talk", grid=[0,4])
app.display()





