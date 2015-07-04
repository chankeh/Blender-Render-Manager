#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage rendering output path'''
import xml.etree.ElementTree as xmlMod
import os
from usefullFunctions import indexPrintList

class Output:
	'''class to manage rendering output path'''
	
	
	def __init__(self, xml= None):
		'''initialize output path with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize output path with default value'''
		
		if not os.path.exists('/home/'+os.getlogin()+'/.BlenderRenderManager/render'):
			os.mkdir('/home/'+os.getlogin()+'/.BlenderRenderManager/render')
		self.path = '/home/'+os.getlogin()+'/.BlenderRenderManager/render/'
		self.pattern = '%N - %S/%L - %F'
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize output path with values extracted from an xml object'''
		self.path = xml.get('path')
		self.pattern = xml.get('pattern')
	
	
	
	
	
	def toXml(self):
		'''export output path into xml syntaxed string'''
		return '<output path="'+self.path+'" pattern="'+self.pattern+'" />\n'
	
	
	
	
	
	def see(self, log):
		'''method to see output path and access edition menu'''
		change = False
		log.menuIn('Output')
		
		while True:
			os.system('clear')
			log.print()
			
			print('\n')
			self.print()
			
			print('''\n\n        \033[4mMenu :\033[0m
1- Edit path
2- Edit patterns
0- Quit

''')
			choice = input().strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				# edit output path
				change = (self.editPath(log) or change)
			elif choice == '2':
				# edit output pattern
				change = (self.editPattern(log) or change)
			else:
				log.write('\033[31mError : unvalid menu index!\033[0m\n')
	
	
	
	
	
	def print(self, index = False, std = True):
		'''a method to display the output path settings'''
		
		print('\033[4mOutput path :\033[0m')
		print('      '+self.path)
		print('\n\033[4mOutput pattern :\033[0m')
		print('      '+self.pattern)
	
	
	
	
	
	def editPath(self, log):
		'''method to manually edit output path'''
		return False
	
	
	
	
	
	def editPattern(self, log):
		'''method to manually edit output pattern'''
		log.menuIn('Edit Pattern')
		
		patterns = [
					'%N/%S/%L/%F',
					'%N/%S/%L - %F',
					'%N - %S/%L/%F',
					'%N - %S/%L - %F',
					'%N - %S - %L/%F',
					
					'%N/%S/%F/%L',
					'%N/%S/%F - %L',
					'%N - %S/%F/%L',
					'%N - %S/%F - %L',
					'%N - %S - %F/%L',
					
					'%S/%N/%L/%F',
					'%S/%N/%L - %F',
					'%S - %N/%L/%F',
					'%S - %N/%L - %F',
					'%S - %N - %L/%F'
					]
		
		
		while True:
			os.system('clear')
			log.print()
			print('\n\n')
			indexPrintList(patterns)
			
			choice = input('\n\nwhat\'s the pattern to use?(h for help)').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			if choice == 'h':
				print('''        \033[4mPatern Help\033[0m
				
Choose a pattern for output file naming and directory tree. part separate by '/' will be directory and final part will be the output file name. part separate by '-' will be in the same directory/file name.

%N will be replace by the file name
%S will be replace by the scene name
%L will be replace by the renderlayer group alias
%F will be replace by the number of the frame

Press enter to continue''')
				input()
				continue
			
			try:
				choice = int(choice)
			except ValueError:
				log.write('\033[31mError : unvalid pattern choice\033[0m\n')
				continue
			
			if choice < 0 or choice >= len(patterns):
				log.write('\033[31mError : out of range pattern choice\033[0m\n')
				continue
			
			self.pattern = patterns[choice]
			log.write('pattern set to : '+patterns[choice]+'\n')
			log.menuOut()
			return True
	
	
	
	
	
	
	
	
