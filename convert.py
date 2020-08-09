import platform
import os
import platform
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
containerFormat = ".mp4" # file extension (rmb to put the dot)
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
extraCommands = "-map 0:0 -map 0:a -crf 20" # important stuff
# 				^ maps video, audio(all) and subtitles(all - if it exists). quality = 20 (higher than average)

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

# auto install required tools
clearScreen()
print("[PREPARE] checking installation, please wait..")
if not "ffprobe" in str(subprocess.check_output("pip3 list", shell=True)):
	print("[PREPARE] ffprobe not found, proceeding to install..")
	subprocess.check_output("pip3 install ffprobe", shell=True)
if not "ffmpeg-bitrate-stats" in str(subprocess.check_output("pip3 list", shell=True)):
	print("[PREPARE] ffmpeg-bitrate-stats not found, proceeding to install..")
	subprocess.check_output("pip3 install ffmpeg-bitrate-stats", shell=True)
if not "FFmpeg developers" in str(subprocess.check_output("ffmpeg -version", shell=True)):
	print("[PREPARE] ffmpeg not found, proceeding to install..")
	if platform.system() == Windows:
		print("[FATAL] windows support coming soon")
		exit()
	if not "Example usage:" in str(subprocess.check_output("brew", shell=True)):
		print("[PREPARE] cannot find Homebrew!")
		print("[PREPARE] script will require you to install Homebrew first")
		print("[PREPARE] Homebrew might ask for your password!")
		input("[PREPARE] Press Enter to accept and install")
		os.system("/bin/bash -c '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh'")
	print("[PREPARE] Homebrew found, installing ffmpeg..")
	os.system("brew install nasm pkg-config texi2html aom fontconfig freetype frei0r gnutls lame libass libbluray libsoxr libvorbis libvpx opencore-amr openjpeg opus rtmpdump rubberband sdl2 snappy speex tesseract theora x264 x265 xvid xz ffmpeg")
if not "ffmpeg-progressbar-cli" in str(subprocess.check_output("npm list -g", shell=True)):
	print("[PREPARE] ffmpeg-bar not found, proceeding to install..")
	if not "Usage: npm <command>" in str(subprocess.check_output("npm", shell=True)):
		print("[PREPARE] installing npm using Homebrew..")
		os.system("brew install node")
	print("[PREPARE] npm found, installing ffmpeg-bar")
	os.system("sudo npm install --global ffmpeg-progressbar-cli")
print("[PREPARE] done")




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

# end of functions

# start of main
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
	try:
		input("[READY] Press Enter to accept and start job...") # wait for user permission to start. crtl + c will not do anything at this point
	except:
		print("")
		print("[CANCELLED] you declined")
		exit()
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
			if not skip == 3: #skip if all four passes
				autoSubCodec(targetZero, containerFormat)
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
					command = "ffmpeg -i '" + target + "' " + "-c:v " + tempcodecFormat + " " + extraCommands + " -c:a " + tempaudioFormat + " -preset " + preset +" -y -b:v " + videoBitrate +" -b:a " + audioBitrate + " '" + output + "' -loglevel 8"
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
		successCount += 1
	else:
		if removeOringalFile == 1:
			print("[FAILED]", x)
			failCount += 1
if not fileCount == 0:
	print("[RESULT]", successCount, "file(s) verified")
	if removeOringalFile == 1:
		print("[RESULT]", failCount, "file(s) failed")
	print("[RESULT]", doneCount, "file(s) processed")
print("[END] job done")

