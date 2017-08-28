import sympy as sp
from IPython.display import display
sp.init_printing()  # pretty printing

# Define impulse and unit step as functions of t
t = sp.symbols('t');
imp = sp.DiracDelta(t);
ustep = sp.Heaviside(t);
#ustep = sp.Piecewise( (0, t<1), (1, True));  # diff() doesn't give delta function?!

# Setup differential equation
x = sp.Function('x');  y = sp.Function('y');
RC = sp.symbols('RC');#, real=True);
lp1de = sp.Eq(y(t) + RC*sp.diff(y(t), t), x(t));
#print(lp1de);  display(lp1de);

# Generic solution
y_sl0e = sp.dsolve(lp1de, y(t));
y_sl0r = y_sl0e.rhs  # take only right hand side
#print(y_sl0e);  display(y_sl0e);

# Initial condition
a0 = sp.symbols('a0');
cnd1 = sp.Eq(y_sl0r.subs(t, -1), a0);  # y(-1) = a0
#cnd2 = sp.Eq(y_sl0r.diff(t).subs(t, -1), b0)  # y'(-1) = b0
#print(cnd1);  display(cnd1);

# Solve for C1:  magic brackets in solve() returns result as dictionary
C1 = sp.symbols('C1')  # generic constants
C1_sl = sp.solve([cnd1], (C1))
#C1C2_sl = sp.solve([cnd1, cnd2], (C1, C2))
#print(C1_sl);  display(C1_sl);

# Substitute back for solution in terms of a0
y_sl1 = y_sl0r.subs(C1_sl);
#print(sp.Eq(y(t), y_sl1));  display(sp.Eq(y(t), y_sl1));

# Set values for constants
y_sl1s = y_sl1.subs({RC:1,a0:0}).doit()
#print(sp.Eq(y(t), y_sl1s));  display(sp.Eq(y(t), y_sl1s));

# Set input function and solve
y_sl1sx = y_sl1s.subs({x(t):ustep}).doit()
print(sp.Eq(y(t), y_sl1sx));  display(sp.Eq(y(t), y_sl1sx))

# Plot output
sp.plot(y_sl1sx, (t,-4,8))
