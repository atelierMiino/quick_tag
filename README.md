# QuickTag

## Function
Quickly tag audio metadata.
Written for personal use, intended to work in junction with the command:
```
yt-dlp --extract-audio --output '%(title)s.%(ext)s'
```
Most convenient to use on music.youtube.com.
Note: yt-dlp and youtube-dl cannot download off spotify.


## Application
QuickTag always only tags Artist and Title audio metadata or nothing at all.

The program only accepts folder-paths. If none is given, program defaults to
current folder.

WARNING: Files containing mp4 headers (mp4 / m4a) will be rewritten as opus.

Tagging can be achieved in in 2 ways.


## Tag by File-Folder (Default)
```
python QuickTag.py
```
Yields the default Tag by File-Folder mode. File structure is assumed to be setup as:
```
{ ROOT DIR }/{ ARTIST }/{ SONG_TITLE }.{ FILETYPE }
```
Note: File-Folder is assumed to be the artist and the File-Name is assumed to be just
the song title and filetype.


## Tag by File-Name
```
python QuickTag.py -n
```
Yields the Tag by File-Name mode. File structure is assumed to be setup as:
```
{ ROOT DIR }/{ ARTIST - SONG_TITLE }.{ FILETYPE }
```
Note: File-Name is assumed to be exactly '< ARTIST > - < SONG_TITLE >.< FILETYPE >'.
Note: ' - ' is important. Simply using '-' will not suffice.
Note: Deviating from this format will cause QuickTag to skip file.


## Dependencies
* Python3.x
* [mutagen](https://mutagen.readthedocs.io/en/latest/)
* [ffmpeg](https://github.com/FFmpeg/FFmpeg)

## Possible Point of Failures
* Uses '/' instead of '\' to interpret directories, so it will not work properly on Windows machines.
* ffmpeg could fail conversion.
* Only m4a / opus files have been tested.

## Possible Improvements
* Instead of avoiding mp4 tags via file conversion, the issue could be dealt with directly.
* Instead of converting mp4 tag audio, file conversion can be optional.