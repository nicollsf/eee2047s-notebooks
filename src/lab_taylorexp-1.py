import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Symbolic function and derivatives
h, t = sp.symbols('h t');
h = sp.exp(3*t)*t**2;
hp = h.diff(t);
#hpp = hp.diff(t);

# Taylor expansions around point t0
t0 = 1;
h0 = h.subs(t,t0);
h1 = h0 + hp.subs({t:t0})*(t-t0);
#h2 = h0 + hp.subs(t,t0)*(t-t0) + 1/2*hpp.subs(t,t0)*(t-t0)**2;

# Direct Taylor expansion using sympy
h5s = sp.series(h, t, t0, 6).removeO();
print("Taylor 5: ", h5s);

# Convert symbolic to functions that can be evaluated
lam_h = sp.lambdify(t, h, modules=['numpy']);
lam_h1 = sp.lambdify(t, h1, modules=['numpy']);
lam_h5s = sp.lambdify(t, h5s, modules=['numpy']);

# Plots
fig, ax = plt.subplots(1,1);
t_vals = np.linspace(0.5, 1.5, 100);
ax.plot(t_vals, lam_h(t_vals), 'r');
ax.plot(t_vals, lam_h1(t_vals), 'g');
#ax.plot(t_vals, lam_h5s(t_vals), 'b');

# Symbolic plotting also probably works
#sp.plot(h, h1, (t, 0, 1.5))
