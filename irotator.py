#! /usr/bin/python
import subprocess
import sys,os

if os.path.exists(sys.argv[-1]):
	input_file = sys.argv[-1]
	print input_file
	output_file = os.path.splitext(input_file)[0]+'_rotated'+os.path.splitext(input_file)[1]

else: 
	print 'input file does not exist.  Exiting'
	sys.exit()


mediainfo_output = subprocess.Popen('/usr/bin/mediainfo %s'%input_file, stdout=subprocess.PIPE, shell=True).communicate()[0]

for line in mediainfo_output.splitlines():
	if 'Rotation' in line:
		print line
		rotate_value = line.split()[-1]

if rotate_value > 0:
	if '180' in rotate_value:
		rotate = 'hflip'
	elif '-90' in rotate_value:
		rotate = 'rotate=1' 
#How do I distinguish between left 90 and right 90?
	elif '90' in rotate_value:
		rotate = 'rotate=2'
	else:
		print 'I do not know how to process non-right angles'
		sys.exit()

	cmd = '/usr/bin/ffmpeg -i %s -metadata:s:v %s -vf "transpose=1" -sameq -acodec copy %s'%(input_file,rotate,output_file)
	print cmd
	#choice = raw_input('Are you sure you want to run this command?  %s  (Y/n):'%cmd)
	#if not 'n' in choice:
	#	subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
else:
	print "video does not need rotating.  Thanks!"
