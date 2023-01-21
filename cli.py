from note import *
import time
import random
import user
#import keyboard


STATES = [
	0, # exit
	1, # menu
	2, # practice
	3, # analyze
	4, # listen
	]

class CLI:
	def __init__(self, notes):
		self.state = 1
		self.notes = notes

	def startup(self):
		if False:
			first_name = input('Please enter your first name: ')
			last_name = input('And your last name: ')
			print(f'Welcome, {first_name}, to the Pitch Perception Trainer.\n')
		else:
			print('\n\nSKYLAB Pitch Trainer\n\n')
			time.sleep(1)

	def menu(self):
		print('Menu:\n')
		print('0 -- Exit\n1 -- Menu\n2 -- Practice\n3 -- Listen')
		self.state = int(input('\nEnter mode number: '))
		print('\n')

	def practice(self):
		self.practiceMenu()

	def anaylze(self):
		pass
	
	def listen(self):
		pass	

	def practiceMenu(self):
		response = input('Practice Menu\n\n0 -- Back\n1 -- Start\n2 -- Options\n\nEnter mode number: ')
		if response == '1':
			self.practiceSession()
		elif response == '2':
			self.practiceOptions()
		else:
			self.state = 1

	def practiceSession(self):
		note_pred = True
		octave_pred = False
		
		note_set = Notes.NOTES
		note_set = ['C','D','E']#,'F','G','A','B']	
		octave_set = Notes.OCTAVES[3:4]
		trials = 20

		# session_data = user.SessionData(trials, note_pred, octave_pred, note_set, octave_set)
		
		correct_note = 0
		
		print('\n\nPractice Session\n')	
		print('Directions: use options in Practice Menu to change the possible notes and octaves played. You can also change whether you want to practice note perception, octave perception, or both.\n\n')

		note_str = ''
		octave_str = ''
		for i in range(len(note_set)):
			note_str += note_set[i]
			if i != len(note_set)-1:
				note_str += ', '

		for i in range(len(octave_set)):
			octave_str += str(octave_set[i])
			if i != len(octave_set)-1:
				octave_str += ', '

		print(f'Possible notes: {note_str}')
		print(f'In octaves: {octave_str}')

		print(f'\nStarting trial 1 of {trials}\n')
		
		for i in range(trials):
			print(f'\nTrial {i}...\n')
			time.sleep(4)
			rand_note = note_set[random.randint(0, len(note_set)-1)]
			#print(rand_note)
			rand_octave = octave_set[random.randint(0, len(octave_set)-1)]
			note = self.notes.getNote(name=rand_note, octave=rand_octave)
			
			# option to ask to play audio, or time interval
			note.playAudio()
			
			if note_pred:
				note_response = input('Note: ')
				note_compare = (rand_note == note_response)

			if octave_pred:
				octave_response = input('Octave: ')
				octave_compare = (rand_octave == octave_response)
	
			if note_pred and note_compare:
				print(f'\nCorrect, the note is {rand_note}.\n')
				correct_note += 1
			elif note_pred and not note_compare:
				print(f'\nIncorrect, the note is {rand_note}.\n')
			if octave_pred and octave_compare: 
				print('Correct octave.')
			
			# if show frequency:
			print(f'Frequency: {note.frequency}\n')
			#session_data.saveTrial(
		
		print(f'Score: {correct_note} / {trials}\n\n')
		
		time.sleep(5)
		self.practiceMenu()

	def practiceOptions(self):
		# choose number of trials
		# choose to predict notes or octaves
		# choose what notes and octaves to listen to
		# choose duration of sine wave
		# choose to show frequency for each trial
		self.state = input()
