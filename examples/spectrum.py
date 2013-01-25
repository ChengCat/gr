#!/usr/bin/env python

import pyaudio
import numpy
import gr

FS=44100		# Sampling frequency
SAMPLES=1024

mic = None
def get_spectrum():
    global mic
    if mic is None:
        pa = pyaudio.PyAudio()
        mic = pa.open(format=pyaudio.paInt16, channels=1, rate=FS,
                      input=True, frames_per_buffer=SAMPLES)
    amplitudes = numpy.fromstring(mic.read(SAMPLES), dtype=numpy.short)
    return abs(numpy.fft.fft(amplitudes / 32768.0))[:SAMPLES/2]

f = [FS/float(SAMPLES)*t for t in range(1, SAMPLES/2+1)]

gr.setviewport(0.1, 0.95, 0.1, 0.95)
gr.setwindow(50, 25000, 0, 100)
gr.setscale(1)
gr.setmarkersize(1)
gr.setmarkertype(4)

while (True):
    try:
        power = get_spectrum()
    except (IOError):
        continue
    gr.clearws()
    gr.setlinecolorind(1)
    gr.axes(1, 5, 50, 0, 1, 2, -0.008)
    gr.grid(1, 5, 50, 0, 1, 2)
    gr.setcharheight(0.020)
    gr.text(0.15, 0.965, '100Hz')
    gr.text(0.47, 0.965, '1kHz')
    gr.text(0.79, 0.965, '10kHz')
    gr.setlinecolorind(4)
    gr.polyline(SAMPLES/2, f, power)
    gr.updatews()
