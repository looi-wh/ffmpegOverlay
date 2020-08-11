import platform
import os
import platform
from os import system, name # clearScreen
from pathlib import Path
from os import listdir
from os.path import isfile, join
import subprocess
import shutil
import re
clearScreenOption = 1



# VIDEO SETTINGS:
# note: read ffmpeg for this section
arrayOfExtentions = [".avi", ".mkv", ".mov", ".mp4", ".wmv", ".flv", ".webm"] # please keep it to an array format
#											^ note: if video is already processed/meets requirements, script will ignore
#													"requirements" is video, audio and container matches requested
containerFormat = ".mp4" # file extension (rmb to put the dot)
codecFormat = "h264" # video format (refrain from using copy)
audioFormat = "aac" # audio format (refrain from using copy)
preset = "veryfast" # recommended: veryfast (a balance between quality and speed)
videoBitrate = "8M" # recommended: 8M (can be viewed as mbps)
audioBitrate = "320k" # recommended: 192k (normal quality, change to 320k for highest)
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
useGPU = 0  # currently only vaapi support is written
render = "-hwaccel vaapi -hwaccel_device /dev/dri/renderD128 -hwaccel_output_format vaapi"
gpucommand = "-an -sn" # can ignore if u not using
extraCommands = "-map 0:v:0 -map 0:a" # important stuff
# 				^ maps video and audio(all). quality = 20 (higher than average)

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



# functions (some i created a long time ago)

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

def autoSubCodec(inputx, containerFormat):
	global extraCommands
	if containerFormat in inputx:
		extraCommands = extraCommands + " -map '0:s?' -c:s copy "
	if containerFormat == ".mp4" or containerFormat == ".mov":
		extraCommands = extraCommands + " -map '0:s?' -c:s mov_text "
	elif containerFormat == ".mkv":
		extraCommands = extraCommands + " -map '0:s?' -c:s srt "
	else:
		extraCommands = extraCommands + " -map '0:s?' -c:s copy " # copy as last resort

def filterArray(inputx, arrayOfList):
	inputTemp = str(inputx).replace("\n", "")
	for x in arrayOfList:
		inputTemp = inputTemp.replace(x, "")
	return inputTemp

def checkMediaHealth(file):
	return int(subprocess.check_output("ffprobe '" + file + "' > /dev/null 2>&1; echo $?", shell=True))

def runFFMPEG(inputx, vcodec, acodec, vbit, abit, outputx, extraCommands, bar, gpu):
	global preset, gpucommand, render, containerFormat
	if bar == 1:
		mainCommandx = "ffmpeg-bar"
	else:
		mainCommandx = "ffmpeg"
		extraCommands = extraCommands + " -loglevel fatal"
	if vcodec == "copy":
		vcodecGPU = 0
	else:
		vcodecGPU = 1
	if gpu == 1 and vcodecGPU == 1:  # run with gpu
		# How this GPU transcoding works
		# this script takes the input file and create an output with only video
		# then takes the input file and merge with the created video file
		mainCommand = mainCommandx + " " + render
		outputVid = outputx.replace(containerFormat, "_INPUT" + containerFormat)
		inputxVid = outputVid
		vcodecx = "vcodec" + "_vaapi"
		print("[INFO] processing video first with GPU")
		commandv = mainCommand + " -i '" + inputx + "' " + gpucommand + " -c:v " + vcodecx + " -y -b:v " + vbit + " '" + outputVid + "' "
		os.system(commandv) # creates a file without audio and subtitles
		if not os.path.exists(outputVid):
			print("[FATAL - GPU] video output not created")
			print(commandv)
			exit()
		if "-map 0:a" in extraCommands:
			extraCommands = extraCommands.replace("-map 0:a", "-map 1:a")
		else:
			print("[WARNING - GPU] unable to find -map 0:a in extraCommands! adding it..")
			extraCommands = extraCommands + " -map 1:a"
		commandx = mainCommandx + " -i '" + inputxVid + "' -i '" + inputx + "' " + extraCommands + " -c copy '" + outputx + "'"
		print("")
		print("[INFO] processing audio and subtitles without GPU")
		os.system(commandx) # merge original audio with created video
		if not os.path.exists(ouputx):
			print("[FATAL - GPU] final output not created, unable to merge audio with video")
			print(commandx)
			exit()
		else:
			os.remove(outputVid)
	else:
		mainCommand = mainCommandx + " -i '" + inputx + "' -preset: " + preset + " -c:v " + vcodec + " -c:a " + acodec + " -y -b:v " + vbit + " -b:a " + abit + " " + extraCommands + " '" + output + "' "
		os.system(mainCommand)


# end of functions

# start of main
# declare to user
clearScreen()
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
	try:
		input("[READY] Press Enter to accept and start job...") # wait for user permission to start. crtl + c will not do anything at this point
	except:
		print("")
		print("[CANCELLED] you declined")
		exit()
doneCount = 0
# start converting
checkMediaFailed = 0
listOfOutput = []
listOfExpectedSize = []
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
			commandCheckBitrate = "ffmpeg -i in.mp4 -map 0:v -c copy -f segment -segment_time 1 -break_non_keyframes 1 folder seg%d.264"
			skip = 0
			if codecFormat in str(subprocess.check_output(commandCheckVideo, shell=True)): # copy if matches for faster transcoding
				skip += 1
				tempcodecFormat = "copy"
			if audioFormat in str(subprocess.check_output(commandCheckAudio, shell=True)): # copy if matches for faster transcoding
				skip += 1
				tempaudioFormat = "copy"
			if str(containerFormat) in str(target): # if video and audio matches except for container, script will only ask for remux
				skip += 1
			if checkMediaHealth(target) == 1:
				print("[WARNING] media", targetZero, "failed, skipping..")
				skip = 3
			if not skip == 3: #skip if all four passes
				print("")
				autoSubCodec(targetZero, containerFormat)
				output =  targetZero.replace(codecs, containerFormat) # output filename and container
				deleteNFO = targetZero.replace(codecs, ".nfo") # jellyfin nfo reset (just in case the file was renamed due to illegal char. its easier to ask jellyfin to process again)
				print("[CONVERTING] working on", targetZero)
				print("[CONVERTING] output to", output)
				print("[CONVERTING] processing file", doneCount+1, "of", fileCount)
				print("[DETAILS] original video codec:", filterArray(subprocess.check_output(commandCheckVideo, shell=True), ["b'", "'", "n"]))
				print("[DEBUG] tempcodecFormat (video):", tempcodecFormat)
				print("[DEBUG] tempaudioFormat (audio):", tempaudioFormat)
				print("[DETAILS] original audio codec:", filterArray(subprocess.check_output(commandCheckAudio, shell=True), ["b'", "'", "n"]))

				runFFMPEG(target, tempcodecFormat, tempaudioFormat, videoBitrate, audioBitrate, output, extraCommands, useFFMPEGBAR, useGPU)

				if checkMediaHealth(target) == 0:
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
					print("[WARNING] output file is invalid!")
					print("[WARNING] proceeding to remove output file")
					os.remove(output)
			else:
				if checkMediaHealth(x) == 1:
					print("[NOTICE] ignored file", doneCount + 1, "of", fileCount,"as requirements has already been met")
					doneCount -= 1
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
	if codecFormat in str(subprocess.check_output(commandCheckVideo, shell=True)) and audioFormat in str(subprocess.check_output(commandCheckAudio, shell=True)) and str(containerFormat) in str(x) and checkMediaHealth(x) == 0:
		successCount += 1
	else:
		if removeOringalFile == 1:
			print("[FAILED]", x)
			failCount += 1
if not fileCount == 0:
	print("[RESULT]", successCount, "file(s) verified")
	if removeOringalFile == 1:
		print("[RESULT]", failCount, "file(s) failed")
	print("[RESULT]", doneCount, "file(s) converted")
print("[END] job done")

