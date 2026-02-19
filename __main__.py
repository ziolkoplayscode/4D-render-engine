import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as ani
from matplotlib import collections as mc
import os
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip as mpy
from tqdm import tqdm

def rotate(vector, theta, plane):
  # Convert point to a numpy column vector [x, y, z, w]
  v = np.array(vector)
    
  # Initialize a 4x4 Identity Matrix
  m = np.eye(4)
  c, s = np.cos(theta), np.sin(theta)

  # Apply the rotation to the specific plane
  # In 4D, there are 6 primary planes: xy, xz, xw, yz, yw, zw
  if plane == 'xy':
      m[0, 0], m[0, 1], m[1, 0], m[1, 1] = c, -s, s, c
  elif plane == 'yz':
      m[1, 1], m[1, 2], m[2, 1], m[2, 2] = c, -s, s, c
  elif plane == 'xz':
      m[0, 0], m[0, 2], m[2, 0], m[2, 2] = c, s, -s, c
  elif plane == 'xw':
      m[0, 0], m[0, 3], m[3, 0], m[3, 3] = c, -s, s, c
  elif plane == 'yw':
      m[1, 1], m[1, 3], m[3, 1], m[3, 3] = c, -s, s, c
  elif plane == 'zw':
      m[2, 2], m[2, 3], m[3, 2], m[3, 3] = c, -s, s, c
  return m @ v


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

cx = 0
cy = 0
cz = 0
cw = 0


x = [-1,-1,-1,-1, 1, 1, 1, 1,-1,-1,-1,-1, 1, 1, 1, 1]
y = [-1,-1, 1, 1,-1,-1, 1, 1,-1,-1, 1, 1,-1,-1, 1, 1]
z = [-1, 1,-1, 1,-1, 1,-1, 1,-1, 1,-1, 1,-1, 1,-1, 1]
#w = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
w = [-1,-1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 1, 1, 1]
origin = [0,0,0,0]
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

def update_tick(vector,o_vector,fov=90,distance=2,azim=0,elev=0):
  plt.cla()
  if fov == 180:
    ax.set_proj_type('ortho')
  else:
    fl = 1/np.tan(fov/2)
    ax.set_proj_type('persp', focal_length=fl)
  ax.set_xlim(-1.5, 1.5)
  ax.set_ylim(-1.5, 1.5)
  ax.set_zlim(-1.5, 1.5)
  ax.view_init(azim=azim, elev=elev)
  ax.set_axis_off()
  ax.set_facecolor('#000000')
  xp = vector[0].copy()
  yp = vector[1].copy()
  zp = vector[2].copy()
  wp = vector[3].copy()
  xo, yo, zo, wo = o_vector
  for n in range(len(xp)):
    w_factor = 1 / (distance - (wp[n]+ wo))
    xp[n] = (xp[n] + xo) * w_factor
    yp[n] = (yp[n] + yo) * w_factor
    zp[n] = (zp[n] + zo) * w_factor
  line_sx, line_sy, line_sz, line_ex, line_ey, line_ez = update_lines(xp, yp, zp)
  for i in range(len(line_sx)):
    ax.plot([line_sx[i], line_ex[i]], [line_sy[i],line_ey[i]],zs=[line_sz[i],line_ez[i]], color='#FFFFFF')
  ax.scatter(xp,yp,zp, color='#FFFFFF')

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
  for img_number in range(0,frames): 
    image_files.append(os.path.join(image_folder, f'{img_number}.png'))
  clip = mpy(image_files, fps=fps)
  clip.write_videofile(output_path)

def keyframe(folder, sframe, eframe,vectors,origin,rotate_plane='xy',rotate_theta=0,transform=[0,0,0,0],scale=[1,1,1,1]):
  framel = eframe-sframe
  xv, yv, zv, wv = list(zip(*vectors))
  xv = list(xv)
  yv = list(yv)
  zv = list(zv)
  wv = list(wv)
  
  xs, ys, zs, ws = scale
  
  xo, yo, zo, wo = origin

  xt, yt, zt, wt = transform
  
  for n in tqdm(range(int(framel))):
    for o in range(len(vectors)):
      #xv[o], yv[o], zv[o], wv[o] = xv[o]*((1-(n/framel))+xs*(n/framel)), yv[o]*((1-(n/framel))+ys*(n/framel)), zv[o]*((1-(n/framel))+zs*(n/framel)), wv[o]*((1-(n/framel))+ws*(n/framel))
      #xo, yo, zo, wo = xo+xt, yo+yt, zo+zt, wo+wt
      xv[o], yv[o], zv[o], wv[o] = rotate([xv[o], yv[o], zv[o], wv[o]], (np.pi/180)*rotate_theta, rotate_plane)
    update_tick([xv,yv,zv,wv],[xo, yo, zo, wo], fov=90,elev=30)
    plt.savefig(os.path.join(folder, os.path.join('tmp',f'{int(sframe+n)}.png')))
  return list(zip(xv,yv,zv,wv))

def animation(folder, frames, fps):
  mkdir(folder)
  mkdir(os.path.join(folder,'tmp'))
  mkdir(os.path.join(folder,'build'))
  p = list(zip(x,y,z,w))

  keyframe(folder, 0,90,p,origin,rotate_plane='xy',rotate_theta=1)
  keyframe(folder, 90,180,p,origin,rotate_plane='zw',rotate_theta=1)
  keyframe(folder, 180,270,p,origin,rotate_plane='xw',rotate_theta=1)
  keyframe(folder, 270,360,p,origin,rotate_plane='yw',rotate_theta=1)
  
  build_video(os.path.join(folder, 'tmp'), os.path.join(folder, f'build/0-{frames}.mp4'), frames, fps)
  
animation("ani", 360, 30)