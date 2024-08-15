from flask import Flask, render_template
import numpy as np
import matplotlib.pyplot as plt


def xyForThree(x, y, idx):
    return {"x": x.tolist(), "y": y.tolist(), "N": len(y), "rgb": getHexColorsFromIdx(idx)}


def xyzSurfaceForThree(x, y, z, idx: int):
    return {"xyz": np.array([x.flatten(), y.flatten(), z.flatten()]).T.tolist(),
            "Nx": x.shape[0], "Ny": x.shape[1],
            "rgb": getHexColorsFromIdx(idx)}


def xyzVertsForThree(x, y, z, idx: int):
    return {"xyz": np.array([x, y, z]).T.tolist(),
            "N": len(x), "rgb": getHexColorsFromIdx(idx)}


def setUpForThree(data):
    """
    :param data: [x0,f0,x1,f1,....] needs to be in x,y pairs and lists; len(x0)==len(f0),len(x1)==len(f1),...
    :return: dict, contains original and limits to help normalize plotting
    """
    maxx = []
    minx = []
    maxy = []
    miny = []
    dataxy = []
    for i in range(0, len(data), 2):
        maxx.append(data[i].max())
        minx.append(data[i].min())
        maxy.append(data[i + 1].max())
        miny.append(data[i + 1].min())
        dataxy.append(xyForThree(data[i], data[i + 1], i // 2))
    maxX = max(maxx)
    minX = min(minx)
    maxY = max(maxy)
    minY = min(miny)
    ynorms = maxY - minY
    xnorms = maxX - minX
    if ynorms == 0:
        ynorms = .1
        minY -= .05
    if xnorms == 0:
        xnorms = .1
        minX -= .05
    return {"limits": {"ymin": minY,
                       "ynorms": ynorms,
                       "xmin": minX,
                       "xnorms": xnorms},
            "data": dataxy}


def setUpForSurfaceThree(data):
    """
    for scaling 3d plot:
        1) find the largest x,y,z difference
        2) get y (assuming Y as up axis) max and max-min to apply colormap
        3) get midpoints for x,y,z scaled by 1)
    :param data: [x0,y0,z0,x1,y1,z1,...] needs to be in x,y,z pairs, ie pairs of three where x,y,z are 2D numpy arrays
    :return: dict, contains original and limits to help normalize plotting
    """
    maxX = max([data[i].max() for i in range(0, len(data), 3)])
    minX = min([data[i].min() for i in range(0, len(data), 3)])
    maxY = max([data[i + 1].max() for i in range(0, len(data), 3)])
    minY = min([data[i + 1].min() for i in range(0, len(data), 3)])
    maxZ = max([data[i + 2].max() for i in range(0, len(data), 3)])
    minZ = min([data[i + 2].min() for i in range(0, len(data), 3)])
    dataxy = [xyzSurfaceForThree(data[i], data[i + 1], data[i + 2], i // 3) for i in range(0, len(data), 3)]
    normYs = [data[i + 1].max() - data[i + 1].min() for i in range(0, len(data), 3)]
    minYs = [data[i + 1].min() for i in range(0, len(data), 3)]
    mx = max([maxX - minX, maxY - minY, maxZ - minZ])
    midX = ((maxX + minX) / 2) / mx
    midY = ((maxY + minY) / 2) / mx
    midZ = ((maxZ + minZ) / 2) / mx
    return {"limits": {"max": mx,
                       "midX": midX,
                       "midY": midY,
                       "midZ": midZ, },
            "data": dataxy,
            "colorMapYLims": {"normY": normYs, "minY": minYs}}


def setUpForVertsThree(data):
    """
    :param data: [x0,y0,z0,x1,y1,z1,...] needs to be in x,y,z pairs, ie pairs of three where x,y,z are 2D numpy arrays
    :return: dict, contains original and limits to help normalize plotting
    """
    maxX = max([data[i].max() for i in range(0, len(data), 3)])
    minX = min([data[i].min() for i in range(0, len(data), 3)])
    maxY = max([data[i + 1].max() for i in range(0, len(data), 3)])
    minY = min([data[i + 1].min() for i in range(0, len(data), 3)])
    maxZ = max([data[i + 2].max() for i in range(0, len(data), 3)])
    minZ = min([data[i + 2].min() for i in range(0, len(data), 3)])
    dataxy = [xyzVertsForThree(data[i], data[i + 1], data[i + 2], i // 3) for i in range(0, len(data), 3)]
    mx = max([maxX - minX, maxY - minY, maxZ - minZ])
    midX = ((maxX + minX) / 2) / mx
    midY = ((maxY + minY) / 2) / mx
    midZ = ((maxZ + minZ) / 2) / mx
    return {"limits": {"max": mx,
                       "midX": midX,
                       "midY": midY,
                       "midZ": midZ, },
            "data": dataxy}


def plot(data: list, title="", theme="dark_theme"):
    app = Flask(__name__)
    if len(data) % 2 != 0:
        print("data needs to be formatted like [x0,f0,x1,f1,....]")
        return

    if theme not in ["dark_theme", "light_theme"]:
        print("theme needs to be `dark_theme` or `light_theme`")
        return

    for i in range(0, len(data), 2):
        if type(data[i]) == list:
            data[i] = np.array(data[i])
        if type(data[i + 1]) == list:
            data[i + 1] = np.array(data[i + 1])

    @app.route("/")
    def index():
        dataForThree = setUpForThree(data)
        dataForThree["title"] = title
        dataForThree["theme"] = theme
        return render_template("index.html", dataForThree=dataForThree)

    app.run()


def plot3D(data: list, title="", theme="dark_theme", applyCmaps=[]):
    if len(data) % 3 != 0:
        print("data needs to be formatted like [x1,y1,z1,x2,y2,z2,...]")
        return

    if theme not in ["dark_theme", "light_theme"]:
        print("theme needs to be `dark_theme` or `light_theme`")
        return

    for i in data:
        try:
            if len(i.shape) != 2:
                print('data needs to have shape (2,N)')
                return
        except:
            print('data needs to be np.arrays with shape (2,N)')
            return

    if not applyCmaps:
        for i in range(len(data) // 3):
            applyCmaps.append(False)
    else:
        if len(applyCmaps) >= len(data) // 3:
            for i in range(0, len(data) // 3 - len(applyCmaps)):
                applyCmaps.append(False)

    app = Flask(__name__)

    dataForThree = setUpForSurfaceThree(data)
    dataForThree["title"] = title
    dataForThree["theme"] = theme
    dataForThree["applyCmaps"] = [int(i) for i in applyCmaps]

    @app.route("/")
    def index():
        return render_template("index3D.html", dataForThree=dataForThree)

    app.run()


def plot3DAnimationJS(data: list, jsFunctions: list, title="", theme="dark_theme", applyCmaps=[]):
    if len(data) % 3 != 0:
        print("data needs to be formatted like [x1,y1,z1,x2,y2,z2,...]")
        return

    if theme not in ["dark_theme", "light_theme"]:
        print("theme needs to be `dark_theme` or `light_theme`")
        return

    for i in data:
        try:
            if len(i.shape) != 2:
                print('data needs to have shape (2,N)')
                return
        except:
            print('data needs to be np.arrays with shape (2,N)')
            return

    if not applyCmaps:
        for i in range(len(data) // 3):
            applyCmaps.append(False)
    else:
        if len(applyCmaps) >= len(data) // 3:
            for i in range(0, len(data) // 3 - len(applyCmaps)):
                applyCmaps.append(False)

    app = Flask(__name__)

    dataForThree = setUpForSurfaceThree(data)
    dataForThree["title"] = title
    dataForThree["theme"] = theme
    dataForThree["applyCmaps"] = [int(i) for i in applyCmaps]
    dataForThree["jsFunctions"] = jsFunctions

    @app.route("/")
    def index():
        return render_template("index3DAnimation.html", dataForThree=dataForThree)

    app.run()


def plot3DVerts(data: list, title="", theme="dark_theme", ):
    app = Flask(__name__)

    for i in range(0, len(data)):
        if type(data[i]) == list:
            data[i] = np.array(data[i])

    dataForThree = setUpForVertsThree(data)
    dataForThree["title"] = title
    dataForThree["theme"] = theme

    @app.route("/")
    def index():
        return render_template("index3Dvertices.html", dataForThree=dataForThree)

    app.run()


def getHexColorsFromIdx(idx, color_palette="tab10"):
    """
    :param color_palette: matplotlib colormap instance
    :param idx: 0<>9
    :return: rgb of tab color_palette
    """
    return list(plt.get_cmap(color_palette)(idx / 9)[0:3])
