import os
import sys
import codecs as cs

def converter(in_folder, out_folder, in_encode, out_encode, default_ext):
	for p, d, fs in os.walk(in_folder):
		for f in fs:
			in_file = os.path.join(p, f)
			out_file = os.path.join(out_folder, f)
			if os.path.splitext(in_file)[1][1:] == default_ext:
				command = 'iconv -f ' + in_encode + ' -t ' + out_encode + ' ' + os.path.join(p, f) + ' > ' + out_file
				os.system(command)


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print 'Usage: python convert_coding.py [in_folder] [out_folder] [in_enc: UTF-16] [out_enc: UTF-8] [ext: TextGrid]'
		sys.exit(0)
	else:
		if not os.path.isdir(sys.argv[1]):
			print "input folder not exist!"
			sys.exit(0)
		if not os.path.isdir(sys.argv[2]):
			os.mkdir(sys.argv[2])
		converter(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])