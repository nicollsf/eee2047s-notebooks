import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelmax

def rclowpass_resp(xv,n0,y0,TdRC,bflag=0):
    """RC lowpass output from given input using standard Euler 
    xv:  input signal (array)
    n0, y0:  auxiliary condition yv[n0] = y0
    TdRC:  value T/RC
    bflag:  method Euler forward (0) or backward (1)
    returns yv:  output signal (array)
    """
    
    yv = np.zeros(xv.shape);
    yv[n0] = y0;
    
    if bflag==0:
        # Forward Euler in each direction
        for n in range(n0,len(xv)-1):
            yv[n+1] = yv[n] + TdRC*(xv[n] - yv[n]);  # forward recursion
        for n in range(n0,0,-1):
            yv[n-1] = yv[n] - TdRC*(xv[n] - yv[n]);  # reverse recursion
    else:
        # Backward (implicit) Euler in each direction
        for n in range(n0,len(xv)-1):
            yv[n+1] = 1/(1+TdRC)*yv[n] + TdRC/(1+TdRC)*xv[n+1];  # forward recursion
        for n in range(n0,0,-1):
            yv[n-1] = 1/(1-TdRC)*yv[n] - TdRC/(1-TdRC)*xv[n-1];  # reverse recursion

    return yv;

# Input signal and discretisation
N = 20000;
omega0 = 0.1;  # current frequency
T = 0.01;  # small number
#T = 10/N*RC;
print('T=',T)
print('T0=', T0)
print('T0/180=', T0/180)

if omega0==0:  T0 = np.inf;
else:  T0 = 2*np.pi/omega0;  # waveform period (seconds) for current omega0
#nv = np.arange(-200,2000);  # discrete signal indices n
nv = np.arange(-200,N);  # discrete signal indices n
tv = nv*T;  # time values corresponding to indices t=nT
xv = np.zeros(tv.shape);
for i in range(0,len(xv)):  xv[i] = np.cos(omega0*tv[i])*(tv[i]>=0); 
    
# Response for given initial condition
RC = 1;  TdRC = T/RC;
n0 = np.where(nv==0)[0][0];  # find location in nv with zero value
y0 = 0.2;
yv = rclowpass_resp(xv,n0,y0,TdRC,0);
fig = plt.figure();  ph = plt.plot(tv,xv,'r-',tv,yv,'g-');
plt.xlabel('t');  plt.legend(['Input x(t)','Output y(t)']);  plt.ylim((-1.5,1.5));

# Use local maxima for input and output signals to estimate gain and phase
xvlmi = argrelmax(xv)[0];  # locations of local maxima
yvlmi = argrelmax(yv)[0];
if len(xvlmi)<2 or len(yvlmi)<2:  raise RuntimeError  # not enough peaks found
xlmi = xvlmi[-1];  ylmi = yvlmi[-1];  # locations of last maximum

# Required quantities
gain = yv[ylmi]/xv[xlmi];  # ratio of peak amplitudes
tdelay = tv[xlmi] - tv[ylmi];  # time delay (seconds) output peak relative to input
theta = 2*np.pi*tdelay/T0;  # delay in units of radians
while theta<=np.pi:  theta = theta + 2*np.pi;  # add or subtract multiples of 2*pi until in (-pi.pi]
while theta>np.pi:  theta = theta - 2*np.pi;

print('Last output peak:  y(', tv[ylmi], ') =', yv[ylmi]);
print('Last input peak:  x(', tv[xlmi], ') =', xv[xlmi]);
print('Gain:  A =', gain);
print('Phase lag:  theta =', theta, 'radians');
