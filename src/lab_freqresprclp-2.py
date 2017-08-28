import numpy as np
import matplotlib.pyplot as plt

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
omega0 = 1;  # current frequency
T = 0.01;  # small number
#T = 0.001*(2*np.pi/omega0);  # small number relative to wavelength
nv = np.arange(-200,2000);  # discrete signal indices n
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
#raise

# Search signals from back finding positive peaks (this works for the cases of interest)
no = len(yv)-1;  
while no-1>=0 and yv[no-1]<yv[no]:  no = no - 1;  # chomp decreasing from back
while no-1>=0 and yv[no-1]>yv[no]:  no = no - 1;  # stop when not increasing from back
ni = no;  # "no" should be first positive peak from end
while ni-1>=0 and xv[ni-1]<xv[ni]:  ni = ni - 1;  # chomp decreasing from back
while ni-1>=0 and xv[ni-1]>xv[ni]:  ni = ni - 1;  # stop when not increasing from back
    
# Period of input and output waveforms
if omega0==0:  T0 = np.inf;
else:  T0 = 2*np.pi/omega0;  # waveform period (seconds) for current omega_0

# Required quantities
gain = yv[no]/xv[ni];  # ratio of peak amplitudes
tdelay = tv[ni] - tv[no];  # time delay (seconds) output peak relative to input
theta = 2*np.pi*tdelay/T0;  # delay in units of radians

print('Last output peak:  y(', tv[no], ') =', yv[no]);
print('Preceeding input peak:  x(', tv[ni], ') =', xv[ni]);
print('Gain:  A =', gain);
print('Phase lag:  theta =', theta, 'radians');

# One-sided Bode plot values log-log
lwv = np.linspace(-3, 5, 1000);  # linear points in log space
wv = 10**lwv;  # actual frequencies
Hv = (1/RC)/((1/RC)+1j*wv);  # frequency response
dbHv = 10*np.log10(np.abs(Hv)**2);  # magnitude response in dB

# Current point
lw0 = np.log10(omega0);
dbHvw0 = 10*np.log10(np.abs(gain)**2);

# Plot
fh, ax = plt.subplots(2);
ax[0].plot(lwv, dbHv, c='g');  ax[0].set_ylabel('$10 \log_{10} |H(\omega)|^2$');
ax[0].scatter(lw0, dbHvw0);
ax[1].plot(lwv, np.angle(Hv), c='g');  ax[1].set_ylabel(r'$\angle H(\omega)$');
ax[1].scatter(lw0, theta);
plt.xlabel('$\log_{10} \omega$');
