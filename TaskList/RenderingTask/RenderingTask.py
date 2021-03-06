'''A module to manage task rendering in blender'''
import bpy, sys, os, socket, time, threading
sys.path.append(os.path.abspath(sys.argv[4]+'/../../../..'))
from Preferences.PresetList.Preset.Preset import *

def RenderingTask(task, preferences, groups):
	task.running = True
	
	scene = bpy.data.scenes[task.scene]
	bpy.context.screen.scene = scene
	
	scene.render.use_stamp_time = True
	scene.render.use_stamp_date = True
	scene.render.use_stamp_render_time = True
	scene.render.use_stamp_frame = True
	scene.render.use_stamp_scene = True
	scene.render.use_stamp_camera = True
	scene.render.use_stamp_lens = True
	scene.render.use_stamp_filename = True
	scene.render.use_stamp_marker = True
	scene.render.use_stamp_sequencer_strip = True
	scene.render.use_stamp_note = True
	
	scene.render.use_file_extension = True
	scene.render.use_placeholder = True
	
	preset = task.log.preset
	
	connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connexion.connect(('localhost', preferences.port))
	
	listen = threading.Thread(
				target = socketListener,
				args=(connexion, task) 
							)
	listen.start()
	
	try:
		if type(preset) is Preset:
			sceneInfo = task.info.scenes[task.scene]
			scene.frame_start = sceneInfo.start
			scene.frame_end = sceneInfo.end
			scene.render.fps = sceneInfo.fps
		
			preset.applyAndRun(bpy, preferences, task.log.groups[0], connexion, task)
		else:
			preset.applyAndRun(bpy, task, preferences, groups, connexion)
	except Exception as e:
		connexion.sendall( (task.uid+' debugMsg('+str(e)+') EOS').encode() )
	
	task.running = 'NOW'
	connexion.sendall( (task.uid+' VersionEnded EOS').encode() )
	
	listen.join()
	
	connexion.close()



def socketListener(soc, task):
	'''a method to manage signal send by the main process'''
	msg = ''
	soc.settimeout(0.5)
	while True:
		try:
			msg += soc.recv(1024).decode()
		except:
			pass # (socket timeout error)
		
		if task.running == 'NOW':
			break
		if msg[-4:] != ' EOS':
			continue
		else:
			messages = msg.split(' EOS')
			messages.pop()
			for m in messages:
				if m == task.uid+' stopAfterFrame()':
					task.running = 'until next frame'
				if m == task.uid+' stopAfterGroup()':
					task.running = 'until next group'
			msg = ''
	






