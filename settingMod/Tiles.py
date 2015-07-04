#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage tiles sizes'''
import xml.etree.ElementTree as xmlMod
import os

class Tiles:
	'''class to manage tiles sizes'''
	
	
	def __init__(self, xml= None):
		'''initialize tiles sizes with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize tiles sizes with default value'''
		
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize tiles sizes with values extracted from an xml object'''
		
	
	
	
	
	
	def toXml(self):
		'''export tiles sizes into xml syntaxed string'''
		
	
	
	
	
	
	def see(self, log):
		'''method to see tiles sizes and access edition menu'''
		change = False
		log.menuIn('Tiles Sizes')
		
		while True:
			os.system('clear')
			log.print()
			
			print('\n')
			self.print()
			
			print('''\n\n        \033[4mMenu :\033[0m
1- Edit Cycles GPU Tiles Size
1- Edit Cycles CPU Tiles Size
1- Edit Blender Internal Tiles Size
0- Quit

''')
			choice = input().strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				# edit Cycles GPU Tiles Size
				change = (self.editGPU(log) or change)
			elif choice == '2':
				# edit Cycles CPU Tiles Size
				change = (self.editCPU(log) or change)
			elif choice == '3':
				# edit Blender Internal Tiles Size
				change = (self.editBI(log) or change)
			else:
				log.error('Unvalid menu index!', False)
	
	
	
	
	
	def print(self):
		'''a method to display the tiles sizes settings'''
		
	
	
	
	
	
	
	
	
	
	
