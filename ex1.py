import numpy as np
from threeplot.threeplot import plot3D


u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 20), np.linspace(0, np.pi, 20))
x1 = .5 * np.cos(u) * np.sin(v)
y1 = .5 * np.sin(u) * np.sin(v)
z1 = .5 * np.cos(v)

x2, y2 = np.meshgrid(np.arange(-5, 5, 0.25), np.arange(-5, 5, 0.25))
z2 = 2 * np.sin(np.sqrt(x2 ** 2 + y2 ** 2))
#  y is up in threejs so if z is up in python x,y,z --> x,z,-y
plot3D([x2, z2, -y2, x1, z1 + 3.5, -y1], title="3D Plot")