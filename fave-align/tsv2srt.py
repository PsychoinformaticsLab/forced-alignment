import codecs
import sys

def clean_codecs(input, output):
	f = codecs.open(input, 'r', encoding='utf-8')   
	l = f.readlines()
	f.close()

	w = codecs.open(output, 'w', encoding='ascii', errors='ignore')
	w.writelines(l)
	w.close()


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    clean_codecs(input_file, output_file)

