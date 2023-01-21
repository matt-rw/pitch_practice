import numpy as np
import simpleaudio as sa
import matplotlib.pyplot as plt

A_FOUR = 440
T = 2 # duration
SR = 44100 # sample rate

class Note:
	def __init__(self, name, octave, sfcf, num_channels):
		self.name = name
		self.octave = octave
		# semitones from C4
		self.sfcf = sfcf
		self.frequency = self.getFrequency()
		self.t, self.sine = self.getSine()
		self.num_channels = num_channels
		
		# audio is a byte array object
		self.audio = self.getAudio24(pan_l=1, pan_r=1)

	def getFrequency(self):
		f = A_FOUR * 2 ** ((self.sfcf-9)/12)
		return f

	def getSine(self):
		# time domain
		t = np.linspace(0, T, T * SR, False)
		sine = np.sin(self.frequency * t * 2 * np.pi)
		return t, sine
	
	def getAudio16(self):
		pass

	""" Creates stereo bytearray object in 24-bit format as audio
		Slower to create and play audio """ 
	def getAudio24(self, pan_l=1, pan_r=1):
		# pan [0..1]
		audio = np.zeros((T * SR, self.num_channels))
		n = len(self.t)
		audio[0: n, 0] += pan_l * self.sine
		if (self.num_channels == 2):
			audio[0: n, 1] += pan_r * self.sine
		
		# normalize audio to 24-bit range
		# 16-bit multiplies by 32767
		audio *= 8388607 / np.max(np.abs(audio))

		# convert to 32-bit data
		audio = audio.astype(np.int32)
		
		# attempt to prevent clipping at end of audio
		#audio[n-1,0] = 0

		# convert from 32-bit to 24-bit
		i = 0
		byte_array = []
		for b in audio.tobytes():
			if i % 4 != 3:
				byte_array.append(b)
			i += 1
		audio = bytearray(byte_array)

		return audio

	def playAudio(self):
		play = sa.play_buffer(audio_data=self.audio, num_channels=self.num_channels, bytes_per_sample=3, sample_rate=SR)
		play.wait_done()
		play.stop()
	
	def displaySineWave(self):
		plt.figure(figsize=(10,10))
		plt.subplot(211)
		plt.plot(self.linspace, self.sine, 'b')
		plt.show()

	def __str__(self):
		return f"Note({self.name}{self.octave}, {self.frequency})"

class Notes:
	# note enumeration
	NOTES = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']
	OCTAVES = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

	# initialize dataset of notes
	def __init__(self):
		self.notes = self.getNotes()
		#self.notes = np.load('notes.npy', None, True)
		# uncomment to generate frequency table
		#self.frequencies = self.getFrequencies()
	
	def getNotes(self):
		notes = np.empty(shape=(12,12), dtype=object)
		# octave counter from -1 to 10
		oi = -1
		#semitone counter from C4: C-1 (-60), ..., B10 (83)
		si = -60
		for i in range(notes.shape[0]):
			 for j in range(notes.shape[1]):
				 # initialize Note object
				 note = Note(name=self.NOTES[j], octave=(i-1), sfcf=si, num_channels=1)
				 notes[j,i] = note
				 si += 1
		return notes

	def getFrequencies(self):
		frequencies = np.zeros(shape=(12,12))
		for i in range(12):
			for j in range(12):
				frequencies[j,i] = self.notes[j,i].frequency
		return frequencies
		
	def getNote(self, name, octave):
		idx = self.NOTES.index(name)
		note = self.notes[idx, octave+1]
		return note

	def display(self):
		for i in range(12):
			for j in range(12):
				print(self.notes[i,j])


test = False
if test:
	data = Notes()
	frequencies = data.frequencies

	with np.printoptions(precision=3, linewidth=200, suppress=True):
		print(frequencies)

	c4 = data.getNote('C', 4)
	print(c4)
	c4.playSineWave()
