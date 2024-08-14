import numpy as np
from threeplot.threeplot import plot

x1 = np.arange(-4.0, 4.0, 0.005)
x2 = np.linspace(-6, 6, 5001)
f2 = np.cos(3 * x2) * np.exp(-x2 ** 2 / 10) + np.random.normal(0, .1, len(x2))
plot([x2, f2, x2, 1.5 * f2], title="Main Example")
