""" Utility code for converting SRT or txt files to FAVE-align input files """
import re
import click
from os.path import splitext
import subprocess
from pliers.stimuli import ComplexTextStim, load_stims, AudioStim, TextStim
from pliers.converters import VideoToAudioConverter


def _clean_save(filtered, new_file, onset, duration):
    # Matches with video captions, e.g. (PEOPLE YELLING)
    matches = re.findall('\(\s*[A-Z]{2,}.*\)', filtered)

    # Matches with speaker information, e.g. (NARRATOR: )
    matches.extend(re.findall('[A-Z\s]{2,}:', filtered))

    # Remove in between brackets
    matches.extend(re.findall('\[.*\]', filtered))

    # Remove matches and empty lines
    for m in matches:
        filtered = filtered.replace(m, '')
    if filtered == '':
        return

    filtered = filtered.replace("\r\n\r\n", " ")
    filtered = filtered.replace("-", "")

    # Speaker is probably irrelevant, so just using Bob for now
    new_file.write('01\tBob\t%f\t%f\t%s\n' % (onset,
                                              onset + duration,
                                              filtered))


def clean_transcript(input_transcript, input_media, onset=0):
    stim = load_stims([input_media])[0]

    if not isinstance(stim, AudioStim):
        conv = VideoToAudioConverter()
        stim = conv.transform(stim)
        input_media = '/tmp/input_audio.wav'
        stim.save(input_media)

    _, extension = splitext(input_transcript)

    clean_transcript = '/tmp/clean_transcript.txt'
    with open(clean_transcript, 'w') as new_file:

        if extension == 'srt':
            txt = ComplexTextStim(input_transcript)
            for el in txt.elements:
                _clean_save(el.text, new_file, el.onset, el.duration)
        else:  # Treat as a singe block of text
            txt = TextStim(input_transcript)
            _clean_save(txt.text, new_file, onset, stim.duration - onset)

    return clean_transcript, input_media


def parse_textgrid(transcript_path):
    with open(transcript_path) as f:
        start_parse = False  # Indicates we are on the 'word' portion of output
        all_lines = f.readlines()
        texts = []
        for i, line in enumerate(all_lines):
            if line == '\titem [2]:\n':
                start_parse = True
            if start_parse and line.startswith('\t\t\ti'):
                onset = float(all_lines[i+1].split()[-1])
                duration = float(all_lines[i+2].split()[-1]) - onset
                text = str(all_lines[i+3].split()[-1])[1:-1].lower()
                if not (text == 'sp'):  # Space/hesitation in audio
                    texts.append(TextStim(text=text,
                                          onset=onset,
                                          duration=duration))
    return texts


@click.command()
@click.argument('input_transcript')
@click.argument('input_media')
@click.argument('output_file')
@click.option('--onset', default=0,
              help='Onset of first word. Only for .txt files.')
def run_fave(input_transcript, input_media, output_file, onset):
    transcript, audio = clean_transcript(
        input_transcript, input_media, onset)

    text_grid = '/tmp/output.textGrid'

    bashCommand = "python2 FAAValign.py {} {} {}".format(
        audio, transcript, text_grid)
    subprocess.call(bashCommand.split())

    stim = ComplexTextStim(elements=parse_textgrid(text_grid))
    stim.save(output_file)


if __name__ == '__main__':
    run_fave()
