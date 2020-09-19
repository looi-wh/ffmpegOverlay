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

# extractSubs foundation release
# - basically extracts subtitles

arrayOfExtentions = [".avi", ".mkv", ".mov", ".mp4", ".wmv", ".flv", ".webm"] # which file extension to search for
cwd = os.getcwd() # sets current location
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

def runExtract(mediaName, subtitleName): # runs ffmpeg [configure your ffmpeg here]
	command = "ffmpeg -dump_attachment:t '' -i '" + mediaName + "' -map 0:2 -c:s srt -y '" + subtitleName + "'"
	os.system(command) # runs the command
	return 0

targetFiles = findFiles(arrayOfExtentions, cwd) # search for targets
for target in targetFiles: # recursive scrap thru all files in searched list
	for codecs in arrayOfExtentions: # helps with determining the codecs
		if not target.count(codecs) == 0: # prevent works on external
			runExtract(target, target.replace(codecs, ".english.default.srt"))

print("job done")