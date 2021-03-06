#!/usr/bin/python3.4
# -*-coding:Utf-8 -*
'''module to manage metapreset'''
import xml.etree.ElementTree as xmlMod
from usefullFunctions import *
import os

class Metapreset:
	'''class to manage metapreset'''
	
	def __init__(self, xml= None):
		'''initialize metapreset with default value or values extracted from an xml object'''
		if xml is None:
			self.defaultInit()
		else:
			self.fromXml(xml)
	
	
	
	
	
	def defaultInit(self):
		'''initialize metapreset with default value'''
		self.default = None
		self.groups = {}
		self.animation = {}
		
	
	
	
	
	
	def fromXml(self, xml):
		'''initialize metapreset with values extracted from an xml object'''
		self.default = xml.get('default')
		
		self.groups = {}
		self.animation = {}
		for node in xml.findall('group'):
			self.groups[node.get('name')] = node.get('preset')
			self.animation[node.get('name')] = int(node.get('animation', 0))
		
	
	
	
	
	
	def toXml(self, alias = ''):
		'''export metapreset into xml syntaxed string'''
		if self.default is None:
			txt = '<metapreset alias="'+alias+'" >\n'
		else:
			txt = '<metapreset alias="'+alias+'" default="'+self.default+'" >\n'
		
		for group, preset in self.groups.items():
			txt += '  <group name="'+group+'" preset="'+preset\
					+'" animation="'+str(self.animation[group])+'" />\n'
		
		txt += '</metapreset>\n'
		return txt
	
	
	
	
	
	def menu(self, log, alias, presets):
		'''menu to explore and edit metapreset settings'''
		change = False
		log.menuIn(alias+' Metapreset')
		
		while True:
			log.print()
			
			print('\n\n        «'+alias+'» Metapreset')
			
			self.print()
			
			print('''\n\n        Menu :
1- Add Group
2- Change Group Preset
3- Set Group Animation
4- Unset/Remove Group
5- Set Default Preset
9- Unset Default Preset
0- Quit

''')
			
			choice = input('Action?').strip().lower()
			
			if choice in ['0', 'q', 'quit', 'cancel']:
				log.menuOut()
				return change
			elif choice == '1':
				change = (self.add(log, alias, presets) or change)
			elif choice == '2':
				change = (self.edit(log, alias, presets) or change)
			elif choice == '3':
				change = (self.setAnim(log, alias) or change)
			elif choice == '4':
				change = (self.remove(log, alias) or change)
			elif choice == '5':
				change = (self.setDefault(log, alias, presets) or change)
			elif choice == '9':
				if input('Do you really want to unset default preset (y) :').strip().lower() in ['y', 'yes']:
					change = True
					self.default = None
			else:
				log.error('Unvalid menu choice', False)
	
	
	
	
	
	def list(self, index = False):
		'''a method to list all the group of the metapreset'''
		keys = list(self.groups.keys())
		keys.sort(key = str.lower)
		
		if index:
			for i,k in enumerate(keys):
				print(str(i)+'- '+k+' ('+self.getAnim(k)+')')
		else:
			for k in keys:
				print(k)
		
		return keys
	
	
	
	
	
	def getAnim(self, group):
		'''A method to return animation value'''
		if self.animation[group] == 0:
			return 'All Frames'
		else:
			return str(self.animation[group])+' Frames'
	
	
	
	
	
	def choose(self, log):
		'''a method to choose a group of the metapreset'''
		if len(self.groups) == 0:
			log.error('There is no group in the metapreset!')
			return None
		
		while True:
			
			log.print()
			
			print('\n\n        Choose The Target Group :')
			groups = self.list(True)
			
			choice = input('what\' the targeted group?').strip().lower()
			
			if choice in ['', 'q', 'quit', 'cancel']:
				return None
			
			try:
				choice = int(choice)
			except ValueError:
				log.error('integer value expected')
				continue
			
			if choice < 0 or choice >= len(groups):
				log.error('out of available choice range')
				continue
			
			return groups[choice]
	
	
	
	
	
	def print(self):
		'''a method to print Metapreset'''
		if self.default is None:
			print('Default Preset : \033[31mnot set!\033[0m')
		else:
			print('Default Preset : '+self.default)
		print()
		
		for group, preset in self.groups.items():
			print(columnLimit(group, 25, sep = ''),' : ',\
					columnLimit(preset, 25, sep = ''),' : ',\
					columnLimit(self.getAnim(group), 12, sep = ''))
	
	
	
	
	
	def copy(self):
		'''A method to get a copy of current object'''
		xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
		xml += self.toXml('')
		xml = xmlMod.fromstring(xml)
		return Metapreset(xml)
		
	
	
	
	
	
	
	
	def add(self, log, alias, presets):
		'''Method to add a group to the metapreset'''
		log.menuIn('Add renderlayer group to metapreset')
		
		
		group = presets.renderlayers.choose(log, list(self.groups.keys()))
		
		if group is None:
			log.menuOut()
			return False
		
		preset = presets.choose(log, False)
		
		if preset is None:
			log.menuOut()
			return False
		
		anim = Metapreset.animChoice(log)
		if anim is None:
			anim = 0
		
		log.menuOut()
		self.groups[group] = preset
		self.animation[group] = anim
		log.write('add «'+group+'» renderlayer group to «'+alias+'» metapreset, set it to «'+preset+'» preset and '+self.getAnim(group)+'.')
		return True
	
	
	
	
	
	def animChoice(log):
		'''A method to choose a animation settings for a group'''
		log.menuIn('Set Animation')
		while True:
			log.print()
			print('\n\n        Set Animation :\n\n')
			
			anim = input('animation choice in frames (or 0 for all animation) :').strip().lower()
			
			if anim in ['', 'q', 'quit', 'cancel']:
				log.menuOut()
				return None
			
			try:
				anim = int(anim)
			except ValueError:
				log.error('expect an integer value', False)
				continue
			
			if anim < 0:
				log.error('expect a positive value', False)
				continue
			
			log.menuOut()
			return anim
	
	
	
	
	
	def edit(self, log, alias, presets):
		'''Method to the preset associated with a renderlayer group'''
		log.menuIn('Editing Of Group')
		
		log.menuIn('Group Choice')
		group = self.choose(log)
		log.menuOut()
		
		if group is None:
			log.menuOut()
			return False
		
		log.menuIn('Preset Choice')
		preset = presets.choose(log, False)
		log.menuOut()
		
		if preset is None:
			log.menuOut()
			return False
		
		log.menuOut()
		self.groups[group] = preset
		log.write('«'+group+'» renderlayer group of «'+alias+'» metapreset set to «'+preset+'» preset')
		return True
	
	
	
	
	
	def remove(self, log, alias):
		'''a method to remove a group from the metapreset'''
		log.menuIn('Remove A Group')
		
		log.menuIn('Group Choice')
		group = self.choose(log)
		log.menuOut()
		
		if group is None:
			log.menuOut()
			return False
		
		log.menuIn('Remove Group Confirmation')
		log.print()
		confirm = input('Do you really want to remove/unset «'+group+'» renderlayer group of «'+alias+'» metapreset?(y)').strip().lower()
		log.menuOut()
		
		log.menuOut()
		if confirm == 'y':
			self.groups.pop(group)
			self.animation.pop(group)
			log.write('«'+group+'» Renderlayer group removed from «'+alias+'» metapreset')
			return True
		
		
		return False
	
	
	
	
	
	def setDefault(self, log, alias, presets):
		'''a method to set the default preset'''
		log.menuIn('Default Preset')
		
		log.menuIn('Preset Choice')
		preset = presets.choose(log, False)
		log.menuOut()
		
		log.menuOut()
		
		if preset is None:
			return False
		
		self.default = preset
		log.write('«'+alias+'» default preset set to «'+preset+'»')
		return True
	
	
	
	
	
	def useGroup(self, group):
		'''check if group is used by the metapreset'''
		return group in self.groups.keys()
	
	
	
	
	
	def unsetGroup(self, group):
		'''unset group if it's set for the metapreset'''
		if self.useGroup(group):
			self.groups.pop(group)
			self.animation.pop(group)
	
	
	
	
	
	def renameGroup(self, old, new):
		'''rename group if used'''
		if self.useGroup(old):
			self.groups[new] = self.groups[old]
			self.groups.pop(old)
			self.animation[new] = self.animation[old]
			self.animation.pop(old)
	
	
	
	
	
	def renamePreset(self, old, new):
		'''rename preset if it is used'''
		
		if self.default == old:
			self.default = new
		
		for g in self.groups.keys():
			if self.groups[g] == old:
				self.groups[g] = new
	
	
	
	
	
	def unsetPreset(self, preset):
		'''unset group that use preset'''
		for group in list(self.groups.keys()):
			if self.groups[group] == preset:
				self.groups.pop(group)
				self.animation.pop(group)
	
	
	
	
	
	def setAnim(self, log, alias):
		'''A method to edit animation settings'''
		log.menuIn('Group Choice')
		group = self.choose(log)
		log.menuOut()
		
		if group is None:
			return False
		
		anim = Metapreset.animChoice(log)
		
		if anim is None:
			return False
		else:
			self.animation[group] = anim
			return True
	
	
	
	
	
	def applyAndRun(self, bpy, task, preferences, groups, socket):
		'''apply settings to a blender scene object and render it, group by group, frame by frame'''
		scene = bpy.context.screen.scene
		sceneInfo = task.info.scenes[task.scene]
		
		for group in groups:
			
			if group != '[default]':
				scene.frame_start = sceneInfo.start
				if self.animation[group] > 0:
					scene.frame_end = sceneInfo.start + self.animation[group] - 1
				else: 
					scene.frame_end = sceneInfo.end
				
			else:
				scene.frame_start = sceneInfo.start
				scene.frame_end = sceneInfo.end
				
			logGroup = task.log.getGroup(group)
			preset = logGroup.preset
			
			for RL in scene.render.layers.values():
				RL.use = (RL.name in logGroup.renderlayers)
			
			preset.applyAndRun(bpy, preferences, logGroup, socket, task)
			if task.running in ['until next frame', 'until next group']:
				break
	
	
	
	
	
