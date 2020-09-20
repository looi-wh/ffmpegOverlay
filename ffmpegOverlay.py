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
videotarget = "h264" # video codec
audiotarget = "aac" # audio codec
audiochannelstTarget = 2
removeSubtitles = 1

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

def runFFMPEG(inputname, outputname, videoc, audioc, channels): # runs ffmpeg [configure your ffmpeg here]
	# the defaults are configured for:
	# made for maximum jellyfin compatibility
	# h264	(4M - 1920x1080 max)
	# aac	(320K - 2 channel audio)
	# full audio and subtitles pass through
	# faststart, profile main
	# -map '0:s?' -c:s mov_text 
	# command = "ffmpeg -i '" + inputname + "' -preset veryfast -c:v copy -c:a copy -y -map 0:v:0 -map 0:a -movflags +faststart -ac 2 -map '0:s?' -c:s mov_text '" + outputname + "' "
	command = "ffmpeg -i '" + inputname + "' -preset veryfast -c:v " + videoc +" -c:a " + audioc +" -hide_banner -loglevel panic -movflags +faststart -ac " + str(channels) + " '" + outputname + "' "
	os.system(command) # runs the command
	return 0

def runFFPROBE(mediaName, codecsx): 
	global videotarget, audiotarget, audiochannelstTarget, videocTEMP, audiocTEMP, targetContainer, removeSubtitles
	currentVideoCodec = str(subprocess.check_output("ffprobe '" + target + "' 2>&1 >/dev/null |grep Stream.*Video | sed -e 's/.*Video: //' -e 's/[, ].*//'", shell = True))
	currentAudioCodec = str(subprocess.check_output("ffprobe '" + target + "' 2>&1 >/dev/null |grep Stream.*Audio | sed -e 's/.*Audio: //' -e 's/[, ].*//'", shell=True))
	currentSubtitleCheck = int(subprocess.check_output("ffmpeg -i '" + target + "' -c copy -map 0:s -f null - -v 0 -hide_banner && echo $? || echo $?", shell=True))
	try:
		currentAudioChannels = int(subprocess.check_output("ffprobe -i '" + target + "' -show_entries stream=channels -select_streams a:0 -of compact=p=0:nk=1 -v 0", shell = True))
	except:
		currentAudioChannels = 0 # Converts anyways
	skip = 0
	if videotarget in currentVideoCodec:
		videocTEMP = "copy"
		skip += 1
	if audiotarget in currentAudioCodec and int(audiochannelstTarget) == int(currentAudioChannels):
		audiocTEMP = "copy"
		skip += 1
	if codecsx == targetContainer:
		skip += 1
	if currentSubtitleCheck == 0 and removeSubtitles == 1:
		skip += 1
	if not skip == 4 and removeSubtitles == 1:
		return 1
	elif not skip == 3 and removeSubtitles == 0:
		return 1
	return 0

# brain of operations
print("started")
targetFiles = findFiles(arrayOfExtentions, cwd) # search for targets
print(len(targetFiles), "potential targets found")
print("script might look unresponsive but it is actively checking and converting files quietly")
print("Use HTOP to view the running command")
for target in targetFiles: # recursive scrap thru all files in searched list
	for codecs in arrayOfExtentions: # helps with determining the codecs
		if not target.count(codecs) == 0: # prevent works on external
			if not "._" in target:
				targetZero = target # saves a backup of target filename for a clean output name
				videocTEMP = str(videotarget)
				audiocTEMP = str(audiotarget)
				try:
					if runFFPROBE(target, codecs) == 1:
						if targetContainer in str(target): # check if output filename will clash with input filename
							target = target.replace(codecs, str(".input") + str(codecs)) # new target filename
							os.rename(targetZero, target) # renames the file
						output = targetZero.replace(codecs, targetContainer)
						runFFMPEG(target, output, videocTEMP, audiocTEMP, audiochannelstTarget)
						print(targetZero, "completed successfully")
						if removeOringalFile == 1: # removes original file
							os.remove(target)
					else:
						print(targetZero, "passed")
				except:
					print(targetZero, "is ignored as an error has occured")



print("job done")