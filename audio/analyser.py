# code that is 100% responsible for handling computer audio
# accessed from audio and visual scripts

import pyaudio
import numpy as np


from scipy.fftpack import fft, fftfreq

class analyzer:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100  # (sampling rate) number of frames per second
        self.AMPLITUDE = 2 ** 16 / 2

        # Initialize PyAudio
        self.p = pyaudio.PyAudio()
        self.dev_index = 0

        # make sure stereo mixer is @ 50
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if (dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0):
                self.dev_index = dev['index'];
                print('dev_index', self.dev_index)
                break

        # Open stream - check stereo mixer
        self.stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        input_device_index = self.dev_index,
                        frames_per_buffer=self.CHUNK)

    def analyse(self):
        data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        samples = np.frombuffer(data, dtype=np.int16)

        # AMPLITUDE
        blockLogRms = 20 * np.log10(np.max(np.abs(samples)) / 32767.0)

        fft_result = fft(samples)
        freq_spectrum = fftfreq(len(data), 1/self.RATE)
        bass_freq_range = [20, 100]

        bass_indices = np.where((freq_spectrum >= bass_freq_range[0]) & (freq_spectrum <= bass_freq_range[1]))[0]
        
        # Calculate the bass amplitude as the sum of magnitudes in the bass frequency range
        bass_amplitude = np.sum(np.abs(fft_result[bass_indices]))
        normalized_bass_energy = bass_amplitude / len(bass_indices)

        peak_freq_range = [800, 10000]
        peak_indices = np.where((freq_spectrum >= peak_freq_range[0]) & (freq_spectrum <= peak_freq_range[1]))[0]
        
        # Calculate the bass amplitude as the sum of magnitudes in the bass frequency range
        peak_amplitude = np.sum(np.abs(fft_result[peak_indices]))
        peak_frequency = peak_amplitude / len(peak_indices)
        mapped_frequency = max(1,min(((peak_frequency - 1000) / (100000 - 1000)) * 359 + 1, 360))
        #peak_index = np.argmax(np.abs(fft_result))
        #peak_frequency = peak_index * RATE / len(samples)
        
        #y_fft = fft(data)
        #print(np.mean(np.abs(data)))
        #print(math.sqrt(sum_squares/count))
            
        return abs(blockLogRms), mapped_frequency, normalized_bass_energy
    
    def close(self):
        # Close the audio stream
        self.stream.stop_stream()
        self.stream.close()

        # Terminate PyAudio
        self.p.terminate()

a = analyzer()