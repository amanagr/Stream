# # import subprocess
# # import os
# # def getLength(input_video):
# #    result = subprocess.Popen(['ffprobe', '-i', input_video, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv="p=0"'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
# #    output = result.communicate()
# #    return output[0]
# # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# x = '../uploads/Chandan.mp4'
# # print(getLength(x))
# # print(BASE_DIR)
# print(x)

# import subprocess
# subprocess.call('ffmpeg -i '+ x +' video.mp4',shell=True)
# print('y')

# x = r'



# extension = '.mp4'
# extension_less_url = '/home/aman/Desktop/stream/src/stream/uploads/lorem ipsiumf'
# import subprocess
# subprocess.call(['ffmpeg', '-i', extension_less_url + extension, extension_less_url + '.mkv'])
#!/usr/bin/env python3
import random
print(''.join(random.choice('abckdlasdkfjalsdfhorghaovnbklasldfq9823195') for _ in range(12)))
print('asdlkf'.upper())