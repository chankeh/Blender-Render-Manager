#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage resolution settings'''
import xml.etree.ElementTree as xmlMod
from settingMod.Size import *
import os

class Resolution:
	'''class to manage resolution settings'''
	
	
	def __init__(self, xml= None):
		'''initialize resolution settings with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize resolution settings with default value'''
		self.pourcent = 100
		self.size = Size('1920x1080')
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize resolution settings with values extracted from an xml object'''
		self.pourcent = int(xml.get('pourcent'))
		self.size = Size(xml = xml)
	
	
	
	
	
	def toXml(self):
		'''export resolution settings into xml syntaxed string'''
		return '<resolution pourcent="'+str(self.pourcent)+'" '+self.size.toXmlAttr()+' />\n'
	
	
	
	
	
	def see(self, log):
		'''menu to explore and edit resolution settings settings'''
		change = False
		log.menuIn('Resolution')
		
		while True:
			os.system('clear')
			log.print()
			
			self.print()
			
			print('''\n\n        Menu :
1- Edit Resolution Size
2- Edit Pourcent setting
0- Save and quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.size.edit(log, 'Resolution Size') or change)
			elif choice == '2':
				change = (self.edit(log) or change)
			else:
				log.error('Unvalid menu choice', False)
		
	
	
	
	
	
	def print(self):
		'''a method to print preset'''
		print('Resolution : '+self.size.toStr()+'@'+str(self.pourcent))
	
	
	
	
	def edit (self, log):
		'''A method to edit pourcent setting'''
		log.menuIn('Edit Resolution Pourcent')
		
		while True:
			os.system('clear')
			log.print()
			
			print('\n\n        Edit Pourcent :\nCurrent Pourcent : '+str(self.pourcent)+'\n')
			
			choice = input('New pourcent setting?').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return False
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('pourcent setting must be an integer.')
				continue
			
			if choice < 0:
				log.error('pourcent setting must be a positive integer.')
				continue
			
			self.pourcent = choice 
			log.menuOut()
			log.write('Resolution pourcent setting is set to : '+str(self.pourcent)+'%\n')
			return True
		
	
	
	
	
	
	
	
	
	
