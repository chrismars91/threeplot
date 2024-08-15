import numpy as np
from threeplot.threeplot import plot3DAnimationJS

x2, y2 = np.meshgrid(np.arange(-5, 5, 0.25), np.arange(-5, 5, 0.25))
z2 = 2 * np.sin(np.sqrt(x2 ** 2 + y2 ** 2))

u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 20), np.linspace(0, np.pi, 20))
x1 = .5 * np.cos(u) * np.sin(v)
y1 = .5 * np.sin(u) * np.sin(v)
z1 = .5 * np.cos(v)

myJsFunc1 = {"args": ["x", "y", "z", "time"], "return": "const t = time;""return [x,y * Math.sin(t),z];"}
myJsFunc2 = {"args": ["x", "y", "z", "time"], "return": "return [x,y + 1*Math.sin(.5*time),z];"}

plot3DAnimationJS(
    [x2, z2, -y2, x1, 2+z1, -y1],
    jsFunctions=[myJsFunc1, myJsFunc2],
    title="3D Plot Animation Style", applyCmaps=[True, False], theme="light_theme")
