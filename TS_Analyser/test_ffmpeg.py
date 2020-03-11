import subprocess

result = subprocess.run(['ffmpeg', '-nostats', '-i', '/home/moi/go/VLC/bbb.mp4', '-filter_complex', 'ebur128', '-f', 'null', '-' ], stdout=subprocess.PIPE)
result=result.stdout.decode('utf-8')

with open('log.txt', 'r') as file:
    file.write(result)
