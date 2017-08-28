# Standard Euler metod for voltage across capacitor in series RC circuit versus
# input voltage for unit step input.  Initial rest conditions are assumed

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Assume R=C=1
R = 1.0;  C = 1.0;

# Show results for different values of T.  The solution becomes exact as T
# tends to zero
fh1 = plt.figure(1);
for T in [1.0, 0.5, 0.2, 0.1]:
    
    # Discrete time points to calculate (we want to plot from t=0 to t=tmax) 
    tmax = 5.001;
    tv = np.arange(0, tmax, T);
    N = len(tv);  # number of points
    
    # Create a vector yv = (y[0], y[1], ..., y[N-1]) to hold the values of y[n]
    # for nonnegative values of n.  We know that for n<0 the output is zero
    yv = np.zeros(tv.shape);
  
    # Calculate the value for y[0] and put it in vector yv
    yv[0] = 0;

    # Iterate the recursion for the required number of values
    for n in range(1,N):
        yv[n] = yv[n-1] + T/(R*C) - T/(R*C)*yv[n-1];
    
    # Plot the resulting points
    ph = plt.plot(tv, yv, c='g');
    
#end for

# Also plot the exact solution for comparison
tcv = np.arange(0, tmax, T/100);
ycv = 1 - np.exp(-tcv/(R*C));
ph = plt.plot(tcv, ycv, c='k');
plt.xlabel('t');  plt.ylabel('g(t)');
