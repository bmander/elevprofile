import rasterio as rio
from shapely.geometry import LineString
import numpy as np
from scipy import interpolate

def get_patch(path, dataset, layer=1, pad=1):
  ls = LineString(path)

  ll, bb, rr, tt=ls.bounds

  i1, j1 = dataset.index(ll, bb, op=round)
  i2, j2 = dataset.index(rr, tt, op=round)

  upside_down = i2<i1
  if upside_down:
      i1, i2 = i2, i1

  i1, i2, j1, j2 = i1-pad, i2+pad, j1-pad, j2+pad

  window = rio.windows.Window.from_slices((i1, i2), (j1, j2))
  A = dataset.read(layer, window=window)

  if upside_down:
      A = A[::-1,:] # flip ud
      x1, y1 = dataset.xy(i2, j1)
      x2, y2 = dataset.xy(i1, j2)
  else:
      x1, y1 = dataset.xy(i1, j1)
      x2, y2 = dataset.xy(i2, j2)

  bbox = (x1, y1, x2, y2)

  return bbox, A


def resample(path, resolution):
  ls = LineString(path)
  n = int(ls.length//resolution+1)
  return [ls.interpolate(i, normalized=True).coords[0] for i in np.linspace(0,1,n+1)]


def elevprofile(path, dataset, resolution):
  # Path, dataset, and resolution most all use the same units.

  bbox, patch = get_patch(path, dataset)

  ll, bb, rr, tt = bbox
  m, n = patch.shape

  x = np.linspace(ll, rr, n)
  y = np.linspace(bb, tt, m)
  f = interpolate.interp2d(x, y, patch)

  return np.array([(x,y,f(x,y)[0]) for x,y in resample(path, resolution)])




fname = "data/dc.vrt"

dataset = rio.open(fname)

path = [(-77.049533,38.931603), (-77.041999,38.941786), (-77.059450,38.944687)]




