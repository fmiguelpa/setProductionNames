import argparse
import getopt
import os
import re
import sys
import subprocess

from shotgun_api3 import Shotgun
import pprint
print Shotgun



parser = argparse.ArgumentParser(description='Creador de versiones')



parser.add_argument('--Shot', dest='Shot', action='store', help='Shot code')
parser.add_argument('--Sequence', dest='Sequence', action='store', help='Sequence code')
parser.add_argument('--Task', dest='Task', action='store', help='Task code')
parser.add_argument('--Asset', dest='Asset', action='store', help='Asset code')
parser.add_argument('--Path', dest='Path', action='store', help='Path code')
parser.add_argument('--id', dest='id', action='store', help='id code')

##print parser.parse_args()

args = parser.parse_args()
TodosArgs=True

"""print args
print args.Task
print type(args.Task)
"""
if args.Shot==None and args.Task==None and args.Sequence==None and args.Asset==None  and args.id==None  and args.Path==None:
	print "Error: Uno de tus argumentos es nulo, porfavor asegurate que has introducido todos los elementos --shot ### --Task ### --sequence ### --Asset ### --Path*:\\\\**\\\\** --id###"


try:
	Mytask=int(args.Task)
except:
	print "Error: --Task no es un numero"
try:
	MyShot=int(args.Shot)
except:
	print "Error: --shot no es un numero"
try:
	MySequence=int(args.Sequence)
except:
	print "Error: --sequence no es un numero"
try:
	MyAsset=int(args.Asset)
except:
	print "Error: --Asset no es un numero"
try:
	MyID=int(args.id)
except:
	print "Error: --id no es un numero"
if type(args.Path) != str:
	print "Error: --Path no es una dirccion"
##elif if args.Path in open('example.txt').read():
print "Shot:", args.Shot
print "Task:", args.Task
print "Sequemce:", args.Sequence
print "Asset:", args.Asset
print "Path:", args.Path
print "id:", args.id



sg = Shotgun("https://upgdl.shotgunstudio.com","MPadillaTest","803365751699e81520ba2b72253393b2dcd51553883a3d8612b22ba80c6f1875")
print MyAsset
print sg.base_url


entity = {'id':MyAsset, 'type': 'Asset'}
task = {'id':int(args.Task), 'type': 'Task'}

filters = [['entity','is', entity],
			['sg_task','is',task]]

fields = ['creatd_at','code']
result = sg.find("Version", filters,fields)

version_token=r'v\d\d\d'
max_ver = 0
for ver in result:
	tokens=re.findall(version_token,ver['code'])
	if len(tokens) != 0:
		ver_num = int(tokens[0][1:])
		if ver_num> max_ver:
			max_ver = ver_num

nombre = "mPadillaAsset"
PipelineName = "%s v%03d"%(nombre,max_ver + 1)

data = {'code': PipelineName,
	'entity':entity,
	'description':'Pipeline Test',
	'sg_task':task,
	'user':{'id':int(args.id),'type':'HumanUser'},
	'sg_status_list':'rev',
	#'shot':{'id':int(args.Shot),'type':'shot'},
	#'sequence':{'id':int(args.Sequence),'type':'Sequence'},
	'project':{'id':112,'type':'Project'}}
		
result = sg.create("Version",data)
pprint.pprint(result)
mov_file= args.Path
sg.upload("Version",result['id'], mov_file, field_name="sg_uploaded_movie", display_name="Media")

"""except ValueError:
	print "Error: Has escrito algo de manera incorrecta, asegurate que escribiste bien el formato: python args.py--shot ### --Task ### --sequence ### --Asset ### --Path*:\\\\**\\\\** --id###"""