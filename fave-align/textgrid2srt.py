''' Utility code for converting TextGrid files to ComplexTextStim files '''
from pliers.stimuli import ComplexTextStim, TextStim
import sys


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


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    stim = ComplexTextStim(elements=parse_textgrid(input_file))
    stim.save(output_file)  # would work with any valid CTS format
