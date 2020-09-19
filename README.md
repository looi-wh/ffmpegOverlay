# ffmpegOverlay
This project contains tools that aims to help with my media server.

# Tools included
- ffmpegOverlay.py (Uses ffmpeg to convert everything in a local/current directory)
- ffprobeRec.py (Creates a list on which media does not meet the requirements)
- extractSubs.py (output subtitles in .srt with ".english.default" written to filename)
- fixSubs.py (Uses ffsubsync to fix out-of-sync subtitles)

# Requirements
- FFMPEG
- Python3
- ffsubsync (for fixSubs.py only - uses another github project)
