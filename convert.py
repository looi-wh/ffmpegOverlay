import platform
import os
from os import system, name # clearScreen
from pathlib import Path
from os import listdir
from os.path import isfile, join
import subprocess
clearScreenOption = 1

# VIDEO SETTINGS:
# note: read ffmpeg for this section
arrayOfExtentions = [".avi", ".mkv", ".mov", ".mp4", ".wmv", ".flv", ".webm"] # please keep it to an array format
containerFormat = ".mp4" # one container type only
codecFormat = "h264" # video format (refrain from using copy)
audioFormat = "aac" # audio format (refrain from using copy)
preset = "veryfast"
videoBitrate = "5M"
audioBitrate = "192k"
# END OF SETTINGS

# ADVANCED SETTINGS:
# note: 1 for enable, 0 for disable
#		this settings is more for jellyfin only
cwd = os.getcwd() # current working directory, replace os.getcwd() to somewhere you would like
removeNFO = 1 # removes the original nfo file
removeOringalFile = 0 # removes the original media file
useFFMPEGBAR = 1 # uses ffmpeg-bar instead PLEASE HAVE THIS INSTALLED
illegalChar = ["'", '"'] # characters to remove from file name
extraCommands = "-map 0:0 -map 0:a -map '0:s?' -crf 20 -c:s mov_text " # important stuff
# 				^ maps video, audio(all) and subtitles(all - if it exists). quality = 20 (higher than average). subititle = mov_test


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
		combinedFiltered = combineArray(filtered)
	return combinedFiltered

def renameFiles(arrayOfTargets):
	for x in arrayOfTargets:
		targetFiles = filterContent(arrayOfExtentions, cwd)
		for y in targetFiles:
			os.rename(y, y.replace(x, ""))

def combineArray(input):
	combine = []
	for x in input:
		for y in x:
			combine.append(y)
	return combine

clearScreen()
# declare to user
print("[SETTINGS] looking at", str(cwd))
print("[SETTINGS] formats to detect:")
for x in arrayOfExtentions:
	print("[SETTINGS]",x)
print("[SETTINGS] containerFormat:", containerFormat)
print("[SETTINGS] codecFormat:", codecFormat)
print("[SETTINGS] audioFormat:", audioFormat)
print("[SETTINGS] preset:", preset)
print("[SETTINGS] videoBitrate:", audioBitrate)
print("[SETTINGS] audioBitrate:", videoBitrate)
# find files
fileCount = 0
# rename files
renameFiles(illegalChar)
targetFiles = filterContent(arrayOfExtentions, cwd)
for x in targetFiles:
	print("[FILES] found", x)
	fileCount += 1
print("[TOTAL] number of target(s) found:", fileCount)
input("[READY] Press Enter to accept and start job...")
doneCount = 0
# start converting
for target in targetFiles:
	clearScreen()
	tempcodecFormat = codecFormat
	tempaudioFormat = audioFormat
	for codecs in arrayOfExtentions:
		if not target.count(codecs) == 0:
			# check video codec:
			commandCheckVideo = "ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 '" + target +"'"
			commandCheckAudio = "ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 '" + target +"'"
			commandCheckSub = "ffmpeg -i '" + target + "' -c copy -map 0:s -f null - -v 0 -hide_banner && echo $? || echo $?"
			commandCheckStreams = "ffprobe '" + target + "' -show_entries format=nb_streams -v 0 -of compact=p=0:nk=1"
			skip = 0
			if subprocess.check_output(commandCheckVideo, shell=True) == codecFormat:
				skip += 1
				tempcodecFormat = "copy"
			if subprocess.check_output(commandCheckAudio, shell=True) == audioFormat:
				skip += 1
				tempaudioFormat = "copy"
			if not skip == 2: #skip if all four passes
				output =  target.replace(codecs, containerFormat)
				deleteNFO = target.replace(codecs, ".nfo")
				if useFFMPEGBAR == 1:
					print("[CONVERTING] working on", target, "using ffmpeg-bar")
					print("[CONVERTING] output to", output)
					print("[CONVERTING] file", doneCount+1, "of", fileCount)
					command = "ffmpeg-bar -i '" + target + "' " + "-c:v " + tempcodecFormat + " " + extraCommands + " -c:a " + tempaudioFormat + " -preset " + preset +" -y -b:v " + videoBitrate +" -b:a " + audioBitrate + " '" + output + "'"
				else:
					print("[CONVERTING] working on", target, "using ffmpeg only")
					print("[CONVERTING] output to", output)
					print("[CONVERTING] file", doneCount+1, "of", fileCount)
					print("[CONVERTING] please wait, script might look non-responsive for large file")
					command = "ffmpeg -i '" + target + "' " + "-c:v " + tempcodecFormat + " " + extraCommands + " -c:a " + tempaudioFormat + " -preset " + preset +" -y -b:v " + videoBitrate +" -b:a " + audioBitrate + " '" + output + "' 2> /dev/null"
				os.system(command) # run command into system
				if os.path.exists(output):
					if str(containerFormat) in str(target): 
						print("ignoring delete for", output) # if output format = input format, do not delete output file
					else:
						if removeOringalFile == 1:
							if os.path.exists(target):
								os.remove(target) # removes original file
						if os.path.exists(deleteNFO):
							if removeNFO == 1:
								os.remove(deleteNFO) # deletes the nfo file
	doneCount += 1

targetFiles = filterContent(arrayOfExtentions, cwd)
clearScreen()
for x in targetFiles:
	print("[finished] found", x)