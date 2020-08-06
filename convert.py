import platform
import os
from os import system, name # clearScreen
from pathlib import Path
from os import listdir
from os.path import isfile, join
clearScreenOption = 1

# VIDEO SETTINGS:
arrayOfExtentions = [".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mp4"] # please keep it to an array format
containerFormat = ".mp4" # one container type only
codecFormat = "h264" # video format
audioFormat = "aac" # audio format
preset = "medium"
videoBitrate = "3M"
audioBitrate = "320k"
# END OF SETTINGS

# ADVANCED SETTINGS:
# note: 1 for enable, 0 for disable
cwd = os.getcwd() # current working directory, replace os.getcwd() to somewhere you would like
removeNFO = 1 # removes the original nfo file
removeOringalFile = 1 # removes the original media file
useFFMPEGBAR = 1 # uses ffmpeg-bar instead
illegalChar = [",", "'", "?", ">", "<"] # characters to remove from file name


def clearScreen(): # for screen clearing. can be disabled using clearScreenOption
	# version 3: optimized with better automation
	global clearScreenOption
	fault = 0
	if not clearScreenOption == 0:
		if name == "nt":
			fault = system("cls")
		else:
			fault = system("clear")
		if not fault == 0:
			clearScreenOption = 0 #disabling it just in case of any further use
	return fault

def filterContent(arrayOfNames, workingDir):
	filtered = []
	for extension in arrayOfNames:
		path = cwd
		files = []
		for r, d, f in os.walk(path):
			for file in f:
				if extension in file:
					files.append(os.path.join(r, file))
		filtered.append(list(filter(lambda k: extension in k, files)))
	return filtered

def renameFiles(arrayOfTargets):
	for x in arrayOfTargets:
		targetFiles = filterContent(arrayOfExtentions, cwd)[0]
		for y in targetFiles:
			os.rename(y, y.replace(x, ""))

clearScreen()
print("[OK] convertmp4.py started")
if platform.system() == "Windows":
	print("[FAILED] windows support still on the way")
	operating = "windows"

# declare to user
print("[SETTINGS] looking at", str(cwd))
print("[SETTINGS] formats to detect:")
for x in arrayOfExtentions:
	print("[SETTINGS]",x)
print("[SETTINGS] containerFormat:", containerFormat)
print("[SETTINGS] codecFormat:", codecFormat)
print("[SETTINGS] audioFormat:", audioFormat)

# find files
fileCount = 0
# rename files
renameFiles(illegalChar)
targetFiles = filterContent(arrayOfExtentions, cwd)[0]
for x in targetFiles:
	print("[FILES] found", x)
	fileCount += 1
print("[TOTAL] number of target(s) found:", fileCount)
input("[READY] Press Enter to accept and start job...")
doneCount = 0
for target in targetFiles:
	for codecs in arrayOfExtentions:
		if not target.count(codecs) == 0:
			output =  target.replace(codecs, containerFormat)
			deleteNFO = target.replace(codecs, ".nfo")
	if useFFMPEGBAR == 1:
		command = "ffmpeg-bar -i '" + target + "' " + "-c:v " + codecFormat + " -c:a " + audioFormat + " -preset " + preset +" -y -b:v " + videoBitrate +" -b:a " + audioBitrate + " '" + output + "'"
	else:
		command = "ffmpeg -i '" + target + "' " + "-c:v " + codecFormat + " -c:a " + audioFormat + " -preset " + preset +" -y -b:v " + videoBitrate +" -b:a " + audioBitrate + " '" + output + "'"
	os.system(command) # run command into system
	doneCount += 1
	if os.path.exists(output):
		if str(containerFormat) in str(target): 
			print("ignoring delete for", output) # if output format = input format, do not delete output file
		else:
			if removeOringalFile == 1:
				os.remove(target) # removes original file
			if removeNFO == 1:
				os.remove(deleteNFO) # deletes the nfo file

targetFiles = filterContent(arrayOfExtentions, cwd)[0]
for x in targetFiles:
	print("[finished] found", x)