from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
import os
import numpy as np
import time
from math import sin, cos, radians, pi
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

total_state=100;
fea_num=5;
G=10**5;
diff_t=0.001;

def init(total_state,n_body,fea_num,orbit):
  data=np.zeros((total_state,n_body,fea_num),dtype=float);
  if(orbit):
    data[0][0][0]=100;
    data[0][0][1:5]=0.0;
    for i in range(1,n_body):
      data[0][i][0]=np.random.rand()*8.98+0.02;
      distance=np.random.rand()*90.0+10.0;
      theta=np.random.rand()*360;
      theta_rad = pi/2 - radians(theta);    
      data[0][i][1]=distance*cos(theta_rad);
      data[0][i][2]=distance*sin(theta_rad);
      data[0][i][3]=-1*data[0][i][2]/norm(data[0][i][1:3])*(G*data[0][0][0]/norm(data[0][i][1:3])**2)*distance/1000;
      data[0][i][4]=data[0][i][1]/norm(data[0][i][1:3])*(G*data[0][0][0]/norm(data[0][i][1:3])**2)*distance/1000;
      #data[0][i][3]=np.random.rand()*10.0-5.0;
      #data[0][i][4]=np.random.rand()*10.0-5.0;
  else:
    for i in range(n_body):
      data[0][i][0]=np.random.rand()*8.98+0.02;
      distance=np.random.rand()*90.0+10.0;
      theta=np.random.rand()*360;
      theta_rad = pi/2 - radians(theta);    
      data[0][i][1]=distance*cos(theta_rad);
      data[0][i][2]=distance*sin(theta_rad);
      data[0][i][3]=np.random.rand()*6.0-3.0;
      data[0][i][4]=np.random.rand()*6.0-3.0;
  return data;

def norm(x):
  return np.sqrt(np.sum(x**2));

def get_f(reciever,sender):
  diff=sender[1:3]-reciever[1:3];
  distance=norm(diff);
  if(distance<1):
    distance=1;
  return G*reciever[0]*sender[0]/(distance**3)*diff;
 
def calc(cur_state,n_body):
  next_state=np.zeros((n_body,fea_num),dtype=float);
  f_mat=np.zeros((n_body,n_body,2),dtype=float);
  f_sum=np.zeros((n_body,2),dtype=float);
  acc=np.zeros((n_body,2),dtype=float);
  for i in range(n_body):
    for j in range(i+1,n_body):
      if(j!=i):
        f=get_f(cur_state[i][:3],cur_state[j][:3]);  
        f_mat[i,j]+=f;
        f_mat[j,i]-=f;  
    f_sum[i]=np.sum(f_mat[i],axis=0); 
    acc[i]=f_sum[i]/cur_state[i][0];
    next_state[i][0]=cur_state[i][0];
    next_state[i][3:5]=cur_state[i][3:5]+acc[i]*diff_t;
    next_state[i][1:3]=cur_state[i][1:3]+next_state[i][3:5]*diff_t;
  return next_state;

def get_f_balls(reciever, sender):
  diff = sender[1:3] - receiver[1:3];
  distance = norm(diff);
  if distance<1:
    return (sender[3:] - receiver[3:])*diff/distance**2 * diff;
  else:
    return 0*diff
    

def calc_balls(cur_state, n_body):
  next_state=np.zeros((n_body,fea_num),dtype=float);
  f_mat=np.zeros((n_body,n_body,2),dtype=float);
  f_sum=np.zeros((n_body,2),dtype=float);
  acc=np.zeros((n_body,2),dtype=float);
  for i in range(n_body):
    for j in range(i+1,n_body):
      if(j!=i):
        f = get_f_balls(cur_state[i][:],cur_state[j][:]);  
        f_mat[i,j]+=f;
        f_mat[j,i]-=f;  
    f_sum[i]=np.sum(f_mat[i],axis=0); 
    acc[i]= f_sum[i]/cur_state[i][0];
    next_state[i][0]=cur_state[i][0];
    next_state[i][3:5]=cur_state[i][3:5]+acc[i]*diff_t;
    next_state[i][1:3]= cur_state[i][1:3] + next_state[i][3:5]*diff_t;
  return next_state;

def gen(n_body,orbit):
  # initialization on just first state
  data=init(total_state,n_body,fea_num,orbit);
  for i in range(1,total_state):
        data[i]=calc(data[i-1],n_body);
  return data;

'''
def make_video(xy,filename):
  os.system("rm -rf pics/*");
  FFMpegWriter = animation.writers['ffmpeg']
  metadata = dict(title='Movie Test', artist='Matplotlib',
                  comment='Movie support!')
  writer = FFMpegWriter(fps=15, metadata=metadata)
  fig = plt.figure()
  plt.xlim(-200, 200)
  plt.ylim(-200, 200)
  fig_num=len(xy);
  color=['ro','bo','go','ko','yo','mo','co'];
  with writer.saving(fig, filename, len(xy)):
    for i in range(len(xy)):
      for j in range(len(xy[0])):
        plt.plot(xy[i,j,1],xy[i,j,0],color[j%len(color)]);
      writer.grab_frame();
'''
    
def make_video(xy, filename):
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = plt.plot([], [], 'ro', animated = True)
    ax.set_axis_off()

    def init():
        ax.set_xlim(-100, 100)
        ax.set_ylim(-100, 100)
        return ln, 
    
    def update(frame):
        xdata, ydata = [], []
        for j in range(len(xy[0])):
            for k in range(0, frame):
              if frame - k >= 0:
                xdata.append(xy[frame - k, j, 1])
                ydata.append(xy[frame - k, j, 2])
              else:
                break
        ln.set_data(xdata, ydata)
        return ln,
    ani = FuncAnimation(fig, update, frames = len(xy), init_func = init, blit = False)
    ani.save(filename)
    return ani

if __name__=='__main__':
  data=gen(3,True);
  xy=data[:,:,1:3];
  make_video(xy,"test.mp4");