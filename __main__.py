import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as ani
from matplotlib import collections as mc
import os
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip as mpy
from tqdm import tqdm


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.set_axis_off()
ax.set_facecolor('#000000')


x = [-1,-1,-1,-1, 1, 1, 1, 1,-1,-1,-1,-1, 1, 1, 1, 1]
y = [-1,-1, 1, 1,-1,-1, 1, 1,-1,-1, 1, 1,-1,-1, 1, 1]
z = [-1, 1,-1, 1,-1, 1,-1, 1,-1, 1,-1, 1,-1, 1,-1, 1]

w = [-1,-1,-1,-1,-1,-1,-1,-1,1,1,1,1,1,1,1,1]

s = [0,0,0,7,7,7,1,5,4,6,2,3]
e = [1,2,4,6,5,3,5,4,6,2,3,1]

line_sx=[]
line_sy=[]
line_sz=[]
line_sw = []
for n in s:
  line_sx.append(x[n])
  line_sy.append(y[n])
  line_sz.append(z[n])

line_ex=[]
line_ey=[]
line_ez=[]
line_ew = []
for n in e:
  line_ex.append(x[n])
  line_ey.append(y[n])
  line_ez.append(z[n])



for i in range(len(line_sx)):
  ax.plot([line_sx[i], line_ex[i]], [line_sy[i],line_ey[i]],zs=[line_sz[i],line_ez[i]], color='#FFFFFF')

ax.scatter(x,y,z, color='#FFFFFF')

def mkdir(folder):
  try:
    os.mkdir(folder)
    print(f"Directory '{folder}' created successfully.")
  except FileExistsError:
    print(f"Directory '{folder}' already exists.")
  except OSError as e:
    print(f"Error creating directory '{folder}': {e}")

def build_video(image_folder, output_path, frames, fps):
  image_files = [] 
  for img_number in range(1,frames): 
    image_files.append(os.path.join(image_folder, f'{img_number}.png'))
  clip = mpy(image_files, fps=fps)
  clip.write_videofile(output_path)

def animation(folder, frames, fps):
  mkdir(folder)
  mkdir(os.path.join(folder,'tmp'))
  mkdir(os.path.join(folder,'build'))
  for n in tqdm(range(frames)):
    ax.view_init(azim=n)
    plt.savefig(os.path.join(folder, os.path.join('tmp',f'{n}.png')))
  #shutil.make_archive('frames', 'zip', root_dir=folder)
  build_video(os.path.join(folder, 'tmp'), os.path.join(folder, f'build/0-{frames}.mp4'), frames, fps)
  

  
animation("ani", 360, 30)



