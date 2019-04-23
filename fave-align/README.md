# How to use FAVE-align

@## Make docker image
`docker build . -t alignment`

### Run using Docker

`docker run -v /host/dir:/data -it --rm alignment /data/transcript.txt /data/media.avi /data/out.txt`

This command accepts either `.srt` or `.txt` files as transcripts. The latter is assumed to be a single text chunk for the whole audio.

Also, for the media, you can pass either an audio or video file, and pliers will extract the audio.
