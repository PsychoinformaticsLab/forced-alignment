# How to use FAVE-align

### Preprocess the .srt/.txt file with
	
	python3 srt2fave.py /path/to/input /path/to/output

### Build the docker container via

	docker build -t alignment .

### Run the docker container, mounting the directory with the desired WAV and .srt/.txt files

	docker run --rm -v /path/to/input:/root/work/ -it alignment

### Once in the container, run the following commands
You should be located in `~/htk/FAVE/FAVE-align`. Note the use of Python 2.

	cp /root/work/*.wav .
	cp /root/work/*.srt .
	python2 FAAValign.py audio.wav subtitles.srt output.TextGrid

You will be asked to provide pronunciation for unknown words, but you can probably just skip this. After that the algorithm should run fine (takes 6-8 minutes on an hour long clip). You can then copy it back to the mounted directory with.

	cp output.TextGrid /root/work/

After this, you should exit out of the docker container.

### Postprocess the TextGrid file with

	python3 textgrid2srt.py /path/to/mounted/dir/ /path/to/output
