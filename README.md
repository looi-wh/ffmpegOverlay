# ffmpegOverlay
Designed to help convert large amount of media easily

# Installing on Ubuntu/Debian
Apt update
```
sudo apt-get update
```
Install ffmpeg, mediainfo, nodejs, npm and some stuff
```
sudo apt install -y ffmpeg mediainfo nodejs npm libx264-dev autoconf automake build-essential libass-dev libtool pkg-config texinfo zlib1g-dev libva-dev cmake mercurial libdrm-dev libvorbis-dev libogg-dev git libx11-dev libperl-dev libpciaccess-dev libpciaccess0 xorg-dev
```
Install ffmpeg-bar
```
sudo npm install --global ffmpeg-progressbar-cli
```

# Installing on Mac
Install Homebrew (to make install easier)
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```
Install ffmpeg and node
```
brew install ffmpeg node
```
Install ffmpeg-bar
```
sudo npm install --global ffmpeg-progressbar-cli
```

# How to run
- Make sure you have ffmpeg-progressbar-cli, ffmpeg and media-info
- Download file from release section
- Extract to directory that you want to concert
- And run the following command
```
sudo python3 convert.py
```

# Features
- Supports FFMPEG-BAR
- Able to find any media file recursively
- Able to survive even when a single file fails
- Auto skip media if input codec is the same as the requested codec
- Auto delete input file when output file is created (can be disabled in settings)
- Auto delete original file after creating an output file
- Able to create an output file even when input file name is the same as output
- Capable of running long term (tested for 24 hours converting more than 100 files)
- Able to delete NFO file (made solely for jellyfin - can be ignored)
- Default commands is able to support multiple audio streams and subtitles

# Upcoming planned features
- Use GPU whenever possible
- Able to save original media to a backup location
- Feel free to suggest any features

# Notes
- Edit and find the section for the settings first (make sure its what you want)
- Please ensure read and write permission is done properly
- V9 and H265 conversion is not recommended as it takes too long to convert
- Containers other than mp4, mov and mkv might have buggy subtitles that doesnt work
- The default settings is optimized for video streaming
- Before starting conversion, script will ask you to press the enter key to start
- And lastly, if there are any issues, please send it to the issue or contact me instead

# Screenshot(s)
example of ffmpegOverlay using ffmpeg-bar
![work](screenshot.png)
