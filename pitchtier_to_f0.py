import sys
import os

shift=0.005

def batch_process(in_dir, out_dir):
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	for p, d, fs in os.walk(in_dir):
		for f in fs:
			ext = f.split('.')[-1]
			base_name = f[:len(ext) * -1 - 1]
			# print base_name + ext
			# raw_input()
			if ext == 'PitchTier':
				with open(os.path.join(p, f)) as fi, open(os.path.join(out_dir, base_name + '.f0'), 'w') as fo:
					n = []; v = []
					for line in fi:
						line = line.strip()
						parts = line.split()
						if len(parts) != 3:
							continue
						if parts[0] == 'number':
							n.append(float(parts[2]))
						if parts[0] == 'value':
							v.append(float(parts[2]))
					start_idx = [0]
					end_idx = []
					for i in range(1, len(n)):
						if n[i] - n[i - 1] >= shift * 2:
							# print n[i], n[i - 1]
							end_idx.append(i - 1)
							start_idx.append(i)
					end_idx.append(len(n) - 1)
					# re-arrange n
					# for i in range(len(start_idx)):
					# 	interval = (end_idx[i] - start_idx[i] + 1) * shift
					# 	end = round(n[end_idx[i]] / shift) * shift
					# 	start = end - interval
					# 	for j in range(start_idx[i], end_idx[i]):
					# 		n[j] = start + shift
					# get f0
					# print start_idx
					# print end_idx
					# raw_input()
					f0 = []
					for i in range(len(start_idx)):
						s_t = 0.0; e_t = 0.0
						if i == 0:
							s_t = shift
						else:
							s_t = n[end_idx[i - 1]] + shift
						e_t = n[start_idx[i]]
						# print e_t, s_t
						# print (e_t - s_t) / shift
						num_zero = int(round((e_t - s_t) / shift))
						# print num_zero
						for j in range(num_zero):
							f0.append(0.000000)
						for j in range(start_idx[i], end_idx[i] + 1):
							f0.append(v[j])
					for i in range(len(f0)):
						print >> fo, f0[i]
		
if __name__ == '__main__':
	if len(sys.argv) < 3:
		print 'Usage: python f0_to_pitchtier.py [in_dir] [out_idr]'
		sys.exit()
	batch_process(sys.argv[1], sys.argv[2])