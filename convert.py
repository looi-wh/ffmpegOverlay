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
#											^ note: if video is already processed/meets requirements, script will ignore
#													"requirements" is video, audio and container matches requested
containerFormat = ".mp4" # one container type only
codecFormat = "h264" # video format (refrain from using copy)
audioFormat = "aac" # audio format (refrain from using copy)
preset = "veryfast" # default: veryfast (a balance between quality and speed)
videoBitrate = "5M" # default: 5M (can be viewed as mbps)
audioBitrate = "320k" # default: 192k (normal quality, change to 320k for highest)
# END OF SETTINGS

# ADVANCED SETTINGS:
# note: 1 for enable, 0 for disable
#		this settings is more for jellyfin only
cwd = os.getcwd() # current working directory, replace os.getcwd() to somewhere you would like
removeNFO = 1 # removes the original nfo file
removeOringalFile = 0 # removes the original media file
showFiles = 1 # display the files before startings
useFFMPEGBAR = 1 # uses ffmpeg-bar instead PLEASE HAVE THIS INSTALLED
illegalChar = ["'", '"'] # characters to remove from file name
extraCommands = "-map 0:0 -map 0:a -map '0:s?' -crf 20 -c:s mov_text" # important stuff
# 				^ maps video, audio(all) and subtitles(all - if it exists). quality = 20 (higher than average). subititle = mov_test


# functions (some i created a long time ago)
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

def renameSpecific(file, target, replace):
	os.rename(file, file.replace(target, replace))

def combineArray(input):
	combine = []
	for x in input:
		for y in x:
			combine.append(y)
	return combine
# end of functions

# start of main
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
print("[SETTINGS] videoBitrate:", videoBitrate)
print("[SETTINGS] audioBitrate:", audioBitrate)
# prepare variable
fileCount = 0
# rename files
renameFiles(illegalChar) # removes illegal characters that might screw with the script
targetFiles = filterContent(arrayOfExtentions, cwd) # checks recursively inside folders
for x in targetFiles: # for loop files
	if showFiles == 1: # respect settings
		print("[FILES] found", x) # show files and location (good for double checking)
	fileCount += 1 # counter
print("[TOTAL] number of target(s) found:", fileCount)
if fileCount == 0:
	print("[WARNING] try checking file premission and the working directory in the script")
	print("[WARNING] maybe format detect doesnt include the extension you want")
else:
	input("[READY] Press Enter to accept and start job...") # wait for user permission to start. crtl + c will not do anything at this point
doneCount = 0
# start converting
for target in targetFiles:
	targetZero = target
	tempcodecFormat = codecFormat
	tempaudioFormat = audioFormat
	for codecs in arrayOfExtentions:
		if not target.count(codecs) == 0:
			if str(containerFormat) in str(target):
				renameSpecific(target, codecs, str(".input") + str(codecs))
				target = target.replace(codecs, str(".input") + str(codecs))
			# prepare commands that to be used later
			commandCheckVideo = "ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 '" + target +"'"
			commandCheckAudio = "ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 '" + target +"'"
			commandCheckSub = "ffmpeg -i '" + target + "' -c copy -map 0:s -f null - -v 0 -hide_banner && echo $? || echo $?"
			commandCheckStreams = "ffprobe '" + target + "' -show_entries format=nb_streams -v 0 -of compact=p=0:nk=1"
			skip = 0
			if codecFormat in str(subprocess.check_output(commandCheckVideo, shell=True)): # copy if matches for faster transcoding
				skip += 1
				tempcodecFormat = "copy"
			if audioFormat in str(subprocess.check_output(commandCheckAudio, shell=True)): # copy if matches for faster transcoding
				skip += 1
				tempaudioFormat = "copy"
			if str(containerFormat) in str(target): # if video and audio matches except for container, script will only ask for remux
				skip += 1
			if not skip == 3: #skip if all four passes
				output =  targetZero.replace(codecs, containerFormat) # output filename and container
				deleteNFO = targetZero.replace(codecs, ".nfo") # jellyfin nfo reset (just in case the file was renamed due to illegal char. its easier to ask jellyfin to process again)
				print("[CONVERTING] working on", targetZero)
				print("[CONVERTING] output to", output)
				print("[CONVERTING] processing file", doneCount+1, "of", fileCount)
				print("[DETAILS] original video codec:", subprocess.check_output(commandCheckVideo, shell=True))
				print("[DETAILS] original audio codec:", subprocess.check_output(commandCheckAudio, shell=True))
				if useFFMPEGBAR == 1: # recommended cause of ETA and progress bar
					print("[CONVERTING] using ffmpeg-bar")
					command = "ffmpeg-bar -i '" + target + "' " + "-c:v " + tempcodecFormat + " " + extraCommands + " -c:a " + tempaudioFormat + " -preset " + preset +" -y -b:v " + videoBitrate +" -b:a " + audioBitrate + " '" + output + "'"
				else:
					print("[CONVERTING] using ffmpeg only")
					print("[CONVERTING] please wait, script might look non-responsive for large file")
					command = "ffmpeg -i '" + target + "' " + "-c:v " + tempcodecFormat + " " + extraCommands + " -c:a " + tempaudioFormat + " -preset " + preset +" -y -b:v " + videoBitrate +" -b:a " + audioBitrate + " '" + output + "' 2> /dev/null"
				os.system(command) # run command into system
				if os.path.exists(output): # checks for output file first
					if str(containerFormat) in str(target): 
						print("ignoring delete for", output) # if output format = input format, do not delete output file
					else:
						if removeOringalFile == 1: # respect user settings
							if os.path.exists(target):
								os.remove(target) # removes original file
						if os.path.exists(deleteNFO):
							if removeNFO == 1:
								os.remove(deleteNFO) # deletes the nfo file
			else:
				print("[NOTICE] ignored file", doneCount + 1, "of", fileCount,"as requirements has already been met")
				renameSpecific(target, ".input", "")

	doneCount += 1

print("")
print("END RESULT:")
targetFiles = filterContent(arrayOfExtentions, cwd)
successCount = 0
failCount = 0
for x in targetFiles:
	commandCheckVideo = "ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 '" + x +"'"
	commandCheckAudio = "ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 '" + x +"'"
	commandCheckSub = "ffmpeg -i '" + x + "' -c copy -map 0:s -f null - -v 0 -hide_banner && echo $? || echo $?"
	if codecFormat in str(subprocess.check_output(commandCheckVideo, shell=True)) and audioFormat in str(subprocess.check_output(commandCheckAudio, shell=True)) and str(containerFormat) in str(x):
		print("[SUCCESS] verified", x)
		successCount += 1
	else:
		print("[FAILED] did not passed", x)
		failCount += 1
if not fileCount == 0:
	print("[RESULT]", successCount, "file(s) verified")
	print("[RESULT]", failCount, "file(s) failed")
	print("[RESULT]", doneCount, "file(s) processed")
print("[END] job done")

