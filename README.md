# ffmpegOverlay
This project contains tools that was created to help with my media server.


# Tools included
- ffmpegOverlay.py (Uses ffmpeg to convert everything in a local/current directory)
- ffprobeRec.py (Creates a list on which media does not meet the requirements)
- extractSubs.py (output subtitles in .srt with ".english.default" written to filename)
- fixSubs.py (Uses ffsubsync to fix out-of-sync subtitles, complicated and not recommended)
- subtitleConvert.py (Uses ffmpeg to convert anything other than srt to srt, further making sure there will be lesser chances of remuxing)

# Features (ffmpegOverlay)
- Easily configurable
- Automatically detect which stream can be copied and which needs to be converted
- Automatically detect if subtitles exists and will remove it if enabled
- Automatically skip media if it passes the requirements set by the script (reduce conversion time)

# Requirements
- FFMPEG (All scripts are tested on ffmpeg version 4.2.4-1ubuntu0.1)
- FFPROBE (Recommended)
- Python3 (All the scripts here are powered by python3)
- ffsubsync (For fixSubs.py only - uses another github project)

# Warnings (ffmpegOverlay)
- Even when removeSubtitles is disabled, anything the script touches will still have their subtitles removed
- Forcing the script to stop halfway might result in files being deleted!!
- It might take a long time for conversion, so please run the script inside a screen if applicable

# How to run (Most of the script)
1. Edit the script settings (Default is .mp4, h264 and aac)
2. Ensure that the requirements are met
3. Put the script in the same folder beside the media that you want to convert
4. Run the script using python3
```
python3 ffmpegOverlay.py
```
