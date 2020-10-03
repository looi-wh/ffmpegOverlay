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

# subtitleConvert foundation release
# - converts most subtitles format to srt (better support)

arrayOfExtentions = [".ass", ".sub", ".sbv"] # which file extension to search for
cwd = os.getcwd() # sets current location
final = ".srt"

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

def combineArray(inputx): # converts two dimension array to one dimension
	combine = []
	for x in inputx:
		for y in x:
			combine.append(y)
	return combine

def runConvert(inputx, output):
	command = "ffmpeg -i '" + inputx + "' '" + output + "'"
	os.system(command) # runs the command
	return 0

targetFiles = findFiles(arrayOfExtentions, cwd) # search for targets
print("job started")
for x in targetFiles:
	print(x)
for target in targetFiles: # recursive scrap thru all files in searched list
	for extension in arrayOfExtentions: # helps with determining the extension
		if not target.count(extension) == 0: # prevent works on external
			runConvert(target, target.replace(extension, final))
			os.remove(target)