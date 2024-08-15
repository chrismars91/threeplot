import json
from threeplot.threeplot import plot3DVerts
import gzip

with gzip.open("threeplot/static/assets/models/highpolyjetZip.json", 'rt', encoding='UTF-8') as zipfile:
    jet = json.load(zipfile)

# vertices must be 1D x,y,z arrays and pairs of three
plot3DVerts([jet['x'], jet['y'], jet['z']], title=f"Jet Model, {3 * len(jet['x'])} Vertices", theme="dark_theme")
