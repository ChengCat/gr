import wave, pyaudio
import numpy
import gr

SAMPLES = 2048

wf = wave.open('Monty_Python.wav', 'rb')
pa = pyaudio.PyAudio()
stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                 channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
 
gr.setwindow(0, SAMPLES, -30000, 30000)
gr.setviewport(0.05, 0.95, 0.05, 0.95)
gr.setlinecolorind(218)
gr.setfillintstyle(1)
gr.setfillcolorind(208)

data = wf.readframes(SAMPLES)
while data != '' and len(data) == SAMPLES * wf.getsampwidth():
    stream.write(data)
    amplitudes = numpy.fromstring(data, dtype=numpy.short)
    power = abs(numpy.fft.fft(amplitudes / 512.0))[:SAMPLES/2:2] - 30000

    gr.clearws()
    gr.fillrect(0, SAMPLES, -30000, 30000)
    gr.grid(40, 1200, 0, 0, 5, 5)
    gr.polyline(SAMPLES/4, range(SAMPLES)[0::4], amplitudes[0::4])
    gr.polyline(SAMPLES/8, range(SAMPLES)[0::8], power)
    gr.updatews()

    data = wf.readframes(SAMPLES)