# !/usr/bin/python3
import platform
import os
from os import system, name # clearScreen
from pathlib import Path
from os import listdir
from os.path import isfile, join
import subprocess
import shutil
import re
import datetime
import time
import sys
import glob

# ffmpegOverlay foundation release
# - stipped down version
# - not mean for large scale production
#
# features written:
# - delete original files
# - input and output filename separation
#
# warnings:
# - no checking feature [script can fail anytime]
# - stopping script with removeOriginalFile turned on will delete the original file too[known issue]
# - no graphical indication [you have no idea whats the progress and the errors occured]

arrayOfExtentions = [".avi", ".mkv", ".mov", ".mp4", ".wmv", ".flv", ".webm"] # which file extension to search for
cwd = os.getcwd() # sets current location
removeOringalFile = 1 # delete original files after writing the output files
targetContainer = ".mp4" # set target contatiner [IMPORTANT]

def findFiles(arrayOfNames, workingDir): # file files in a given directory
	filtered = []
	for extension in arrayOfNames:
		path = cwd
		files = []
		for r, d, f in os.walk(path):
			for file in f:
				if extension in file:
					files.append(os.path.join(r, file))
		filtered.append(list(filter(lambda k: extension in k, files)))
		combinedFiltered = combineArray(filtered)
	return combinedFiltered

def combineArray(input): # converts two dimension array to one dimension
	combine = []
	for x in input:
		for y in x:
			combine.append(y)
	return combine

def runFFMPEG(inputname, outputname): # runs ffmpeg [configure your ffmpeg here]
	# the defaults are configured for:
	# made for maximum jellyfin compatibility
	# h264	(4M - 1920x1080 max)
	# aac	(320K - 2 channel audio)
	# full audio and subtitles pass through
	# faststart, profile main
	command = "ffmpeg -i " + inputname + " -preset veryfast -c:v h264 -c:a aac -y -b:v 4M -b:a 320k -map 0:0 -map 0:a -movflags +faststart -profile:v main -video_size 1920x1080 -crf 20 -ac 2  -map '0:s?' -c:s mov_text '" + outputname + "'"
	os.system(command) # runs the command
	return 0

# brain of operations
targetFiles = findFiles(arrayOfExtentions, cwd) # search for targets
for target in targetFiles: # recursive scrap thru all files in searched list
	for codecs in arrayOfExtentions: # helps with determining the codecs
		if not target.count(codecs) == 0: # prevent works on external 
			targetZero = target # saves a backup of target filename for a clean output name
			if targetContainer in str(target): # check if output filename will clash with input filename
				target = target.replace(codecs, str(".input") + str(codecs)) # new target filename
				os.rename(targetZero, target) # renames the file
				targetNameChanged = 1 # prevents target name from mixing with output name
			output = targetZero.replace(codecs, targetContainer) # target output
			runFFMPEG(target, output) # main command
			if removeOringalFile == 1: # removes original file
				os.remove(target)



print("job done")