# ffmpegOverlay
Designed to help convert large amount of media easily

# How to run
- Install ffmpeg (required), ffprobe (required) and ffmpeg-bar (recommended)
- Download file from release section
- Extract and run "python3 convert.py" (no need for sudo)

# Features
- Supports FFMPEG-BAR
- Able to find any media file recursively
- Auto skip media if input codec is the same as the requested codec
- Auto delete input file when output file is created (can be disabled in settings)
- Auto delete original file after creating an output file
- Able to create an output file even when input file name is the same as output
- Capable of running long term (tested 30 days)
- Able to delete NFO file (made solely for jellyfin - can be ignored)
- Default commands is able to support multiple audio streams and subtitles

# Upcoming planned features
- Able to survive even when a single file fails
- Use GPU whenever possible
- Able to save original media to a backup location
- Feel free to suggest any features

# Notes
- Edit and find the section for the settings first (make sure its what you want)
- Please ensure read and write permission is done properly
- V9 and H265 conversion is not recommended as it takes too long to convert
- The default settings is optimized for video streaming
- Before starting conversion, script will ask you to press the enter key to start
- And lastly, if there are any issues, please send it to the issue or contact me instead

# Screenshot(s)
example of ffmpegOverlay using ffmpeg-bar
![work](screenshot.png)
