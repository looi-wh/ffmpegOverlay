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

# ffprobeRec foundation release
# - basically extracts subtitles

arrayOfExtentions = [".avi", ".mkv", ".mov", ".mp4", ".wmv", ".flv", ".webm"] # which file extension to search for
cwd = os.getcwd() # sets current location
targetContainer = ".mp4" # set target contatiner [IMPORTANT]
videotarget = "h264"
audiotarget = "aac"
audiochannelstTarget = 2

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

def runFFPROBE(mediaName): # runs ffmpeg [configure your ffmpeg here]
	global videotarget, audiotarget, audiochannelstTarget, target
	currentVideoCodec = str(subprocess.check_output("ffprobe '" + target + "' 2>&1 >/dev/null |grep Stream.*Video | sed -e 's/.*Video: //' -e 's/[, ].*//'", shell = True))
	currentAudioCodec = str(subprocess.check_output("ffprobe '" + target + "' 2>&1 >/dev/null |grep Stream.*Audio | sed -e 's/.*Audio: //' -e 's/[, ].*//'", shell=True))
	try:
		currentAudioChannels = str(subprocess.check_output("ffprobe -i '" + target + "' -show_entries stream=channels -select_streams a:0 -of compact=p=0:nk=1 -v 0", shell = True))
	except:
		currentAudioChannels = 2
	skip = 0
	if videotarget in currentVideoCodec:
		videoc = "copy"
		skip += 1
	else:
		print(target, "video is using", currentVideoCodec)
	if audiotarget in currentAudioCodec and str(audiochannelstTarget) in str(currentAudioChannels):
		audioc = "copy"
		skip += 1
	else:
		print(target, "audio is using", currentAudioCodec)
	if codecs == targetContainer:
		skip += 1
	if not skip == 3:
		return 1
	return 0

targetFiles = findFiles(arrayOfExtentions, cwd) # search for targets
for target in targetFiles: # recursive scrap thru all files in searched list
	for codecs in arrayOfExtentions: # helps with determining the codecs
		if not target.count(codecs) == 0: # prevent works on external
			if not "._" in target:
				try:
					if runFFPROBE(target) == 1:
						print(target, "failed")
				except:
					print(target, "is left unchecked as it contains illegal characters")

print("job done")