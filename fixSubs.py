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

# fixSubs foundation release
# - uses ffsubsync on github
# - recursively find and apply
# - not mean for large scale production

arrayOfExtentions = [".avi", ".mkv", ".mov", ".mp4", ".wmv", ".flv", ".webm"] # which file extension to search for
cwd = os.getcwd() # sets current location
removeOringalFile = 1 # delete original files after writing the output files
subtitleExt = ".srt"
mediaTarget = ".english.default" # movie.english.default.srt

def findFiles(arrayOfNames, workingDir): # file files in a given directory
	filtered = []
	for extension in arrayOfNames:
		path = cwd
		files = []
		for r, d, f in os.walk(path):
			for file in f:
				if extension in file:
					if not "._" in file:
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

def runFFSubsync(inputsubs, outputsubs, videofile):
	command = "ffsubsync '" + videofile + "' -i '" + inputsubs + "' -o '" + outputsubs + "'"
	os.system(command) # runs the command
	return 0

# brain of operations
targetFiles = findFiles(arrayOfExtentions, cwd) # search for targets
for target in targetFiles: # recursive scrap thru all files in searched list
	for codecs in arrayOfExtentions: # helps with determining the codecs
		if not target.count(codecs) == 0:
			subtitleOutput = target.replace(codecs, str(mediaTarget) + str(subtitleExt))
			subtitleTarget = subtitleOutput.replace(subtitleExt, str(".input") + str(subtitleExt))
			try:
				os.rename(subtitleOutput, subtitleTarget)
				runFFSubsync(subtitleTarget, subtitleOutput, target)
				if removeOringalFile == 1:
					os.remove(subtitleTarget)
			except:
				print("failed", subtitleOutput)

print("job done")