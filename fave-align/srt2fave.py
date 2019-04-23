''' Utility code for converting SRT or txt files to FAVE-align input files '''
import re
import sys
from pliers.stimuli import ComplexTextStim, load_stims, AudioStim
from pliers.converts import VideoToAudioConverter


def run_fave(input_file, input_media, output_file):
	stim = load_stims([input_media])[0]
	if not isinstance(stim, AudioStim):
		conv = VideotoAudioConverter()
		


def clean_transcript(input_file, output_file):
    cts = ComplexTextStim(input_file)  # would work with any valid CTS format

    with open(output_file, 'w') as new_file:
        for el in cts.elements:
            filtered = el.text

            # Matches with video captions, e.g. (PEOPLE YELLING)
            matches = re.findall('\(\s*[A-Z]{2,}.*\)', filtered)

            # Matches with speaker information, e.g. (NARRATOR: )
            matches.extend(re.findall('[A-Z\s]{2,}:', filtered))

            # Remove matches and empty lines
            for m in matches:
                filtered = filtered.replace(m, '')
            if filtered == '':
                continue

            # Speaker is probably irrelevant, so just using Bob for now
            new_file.write('01\tBob\t%f\t%f\t%s\n' % (el.onset,
                                                      el.onset + el.duration,
                                                      filtered))


if __name__ == '__main__':
    input_file = sys.argv[1]
    input_media = sys.argv[1]
    output_file = sys.argv[2]
    run_fave(input_file, input_media, output_file)
