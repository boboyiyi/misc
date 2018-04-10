# -*- coding= utf-8 -*-
import os
import sys
import codecs as cs

ld = {'chs': u'。', 'eng': u'.'}
def proc(in_dir, out_dir, lang):
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	for p, d, fs in os.walk(in_dir):
		for f in fs:
			with cs.open(os.path.join(p, f), 'r', 'utf-8') as fi, cs.open(os.path.join(out_dir, f), 'w', 'utf-8') as fo:
				for line in fi:
					line = line.strip()
					if line.strip() and line.strip() != u'\ufeff':
						parts = line.split(ld[lang])
						for i in range(len(parts)):
							if parts[i]:
								if i != len(parts) - 1:
									fo.write(parts[i].strip() + ld[lang] + '\n')
								else:
									fo.write(parts[i].strip() + '\n')
							
							
if __name__ == '__main__':
	if len(sys.argv) < 4:
		print 'Usage: split_text in_dir out_dir lang'
		sys.exit(1)
	else:
		proc(sys.argv[1], sys.argv[2], sys.argv[3])