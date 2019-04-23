#
# Docker image for forced alignment using the FAVE-align algorithm
# @author Quinten McNamara
#

FROM armariya/htk-ubuntu

# working directory
ENV HOME /root
WORKDIR $HOME

# packages list
RUN \
	apt-get update && apt-get install -y \
    libc6-dev-i386 \
    libx11-dev \
    gawk \
    python-dev \
    python-pip \
    curl \
    git \
    sox

# pip
RUN pip install --upgrade pip

WORKDIR $HOME/htk/
RUN sed "1650s/labid/labpr/" HTKLib/HRec.c > HRec_temp.c ; mv HRec_temp.c HTKLib/HRec.c && \
	./configure --disable-hslab && \
	make clean && \
    make all && \
    make install

RUN pip install --upgrade setuptools
RUN pip install git+https://github.com/tyarkoni/pliers.git@1f4e58 contextlib2
RUN imageio_download_bin ffmpeg

RUN git clone https://github.com/JoFrhwld/FAVE
WORKDIR $HOME/htk/FAVE/FAVE-align

COPY *.py $HOME/htk/FAVE/FAVE-align/

ENTRYPOINT ["python2", "run.py"]
