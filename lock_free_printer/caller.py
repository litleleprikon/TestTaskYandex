import subprocess

while True:
	time = float(input('time\n'))
	text = input('text\n')
	subprocess.Popen('python test.py -s {0:f} -t "{1:s}"'.format(time, text), shell=True)