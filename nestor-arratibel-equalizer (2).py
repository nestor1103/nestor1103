import sys
import os
import numpy as np
import pyaudio
import pygame
from pygame.locals import *
from scipy.fftpack import fft

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nestor Arratibel: 40-Band Musical Equalizer")

# Load and set the icon
icon = pygame.image.load(resource_path('icon.png'))
pygame.display.set_icon(icon)

# Audio settings
CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

# Function to get the frequency spectrum
def get_spectrum(data):
    fft_data = fft(data)
    freq = np.fft.fftfreq(len(fft_data))
    return np.abs(fft_data[:len(fft_data)//2])

# Function to map frequency to color
def freq_to_color(freq):
    r = int(255 * (freq / (RATE/2)))
    g = int(255 - r)
    b = int(128)
    return (r, g, b)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Read audio data
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    
    # Get frequency spectrum
    spectrum = get_spectrum(data)
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the equalizer bars
    bar_width = WIDTH // 40
    for i in range(40):
        bar_height = int(spectrum[i * len(spectrum) // 40] / 100)
        color = freq_to_color(i * RATE / 80)
        pygame.draw.rect(screen, color, (i * bar_width, HEIGHT - bar_height, bar_width - 2, bar_height))
    
    # Update the display
    pygame.display.flip()

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()
sys.exit()
