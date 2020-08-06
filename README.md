# JellyfinMediaOptimizer
a python script that uses FFMPEG and/or FFMPEG-BAR

dependency: 
FFMPEG(IMPORTANT)
FFMPEG-BAR(RECOMMENDED)
PYTHON3(IMPORTANT)

i designed this script in a rush. I tested it and it went quite well.
i made this script for my jellyfin server

# NOTES:
- by default, the script is set to use FFMPEG-BAR, so edit the settings section inside the script to your liking
- you can set the video and audio bitrate, the files to scan for and the container output
- NFO file can also be selected to be removed automatically
- due to some limitations to file naming, characters like " ' " or " ? " might not be accepted
- script will change the file names without asking you.
- if you find the script to be making your computer hot and want to fix it, i suggest using tools like TLP to limit cpu usage

# UPDATES?
see first. im studying aerospace and not IT. I know how to write to script using tons of google search and experiences from trying to make an AI using python.
if you want me to update the script to do something, just send an email to weiheng@looi.org

# SUGGESTIONS:
- keep it to the default settings, best for compatibility
- run TLP to limit cpu to prevent your server from burning (Unless you think your computer can handle it)
- edit to script to your own liking. SEND IT TO ME IF YOU THINK YOU CAN HELP, I WILL CREDIT
- if you are running using ssh into your server, use screen tool instead so you can leave the process running after closing ssh.

i might implement something like a switch for file naming. but i dont need it so i will do it someday when im free.
