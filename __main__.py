import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as ani
from matplotlib import collections as mc
import os
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip as mpy
from tqdm import tqdm

def rotate_4d(vector, theta, plane='xw'):
  """
  Rotates a 4D vector (x, y, z, w) by angle theta in specified plane.
  """
  c, s = np.cos(theta), np.sin(theta)
  
  # Initialize 4x4 Identity Matrix
  R = np.eye(4)
    
  # Define rotation matrix for a plane (e.g., xw plane)
  if plane == 'xw':
    R[0, 0] = c; R[0, 3] = -s
    R[3, 0] = s; R[3, 3] = c
  elif plane == 'xy':
    R[0, 0] = c; R[0, 1] = -s
    R[1, 0] = s; R[1, 1] = c
  elif plane == 'zw':
    R[2, 2] = c; R[2, 3] = -s
    R[3, 2] = s; R[3, 3] = c
  elif plane == 'yz':
    R[1, 1] = c; R[1, 3] = -s
    R[2, 1] = s; R[2, 3] = c
  elif plane == 'xz':
    R[0, 0] = c; R[0, 2] = -s
    R[2, 0] = s; R[2, 2] = c
  elif plane == 'yw':
    R[1, 1] = c; R[1, 3] = -s
    R[3, 1] = s; R[3, 3] = c
  
  return np.dot(R, vector)


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

cx = 0
cy = 0
cz = 0
cw = 0


x = [-1,-1,-1,-1, 1, 1, 1, 1,-1,-1,-1,-1, 1, 1, 1, 1]
y = [-1,-1, 1, 1,-1,-1, 1, 1,-1,-1, 1, 1,-1,-1, 1, 1]
z = [-1, 1,-1, 1,-1, 1,-1, 1,-1, 1,-1, 1,-1, 1,-1, 1]
w = [-1,-1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 1, 1, 1]

s = [ 0, 0, 0, 7, 7, 7, 1, 5, 4, 6, 2, 3, 0, 1, 2, 3, 4, 5, 6, 7, 8, 8, 8,15,15,15, 9,13,12,14,10,11]
e = [ 1, 2, 4, 6, 5, 3, 5, 4, 6, 2, 3, 1, 8, 9,10,11,12,13,14,15, 9,10,12,14,13,11,13,12,14,10,11, 9]


line_sx=[]
line_sy=[]
line_sz=[]
line_ex=[]
line_ey=[]
line_ez=[]

def update_lines(x, y, z):
  line_sx=[]
  line_sy=[]
  line_sz=[]
  for n in s:
    line_sx.append(x[n])
    line_sy.append(y[n])
    line_sz.append(z[n])

  line_ex=[]
  line_ey=[]
  line_ez=[]
  for n in e:
    line_ex.append(x[n])
    line_ey.append(y[n])
    line_ez.append(z[n])
  return line_sx, line_sy, line_sz, line_ex, line_ey, line_ez

def update_tick():
  plt.cla()
  ax.view_init(azim=0)
  ax.set_axis_off()
  ax.set_facecolor('#000000')
  xp = []
  yp = []
  zp = []
  for n in range(len(w)):
    xp.append(x[n])
    yp.append(y[n])
    zp.append(z[n])
  line_sx, line_sy, line_sz, line_ex, line_ey, line_ez = update_lines(xp, yp, zp)
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
    #ax.view_init(azim=n)
    r = (np.pi/180)s #convert degrees to radians
    for o in range(len(x)):
      x[o], y[o], z[o], w[o] = rotate_4d([x[o], y[o], z[o], w[o]], r, 'xw')
    update_tick()
    plt.savefig(os.path.join(folder, os.path.join('tmp',f'{n}.png')))
  #shutil.make_archive('frames', 'zip', root_dir=folder)
  build_video(os.path.join(folder, 'tmp'), os.path.join(folder, f'build/0-{frames}.mp4'), frames, fps)
  

  
animation("ani", 360, 30)

