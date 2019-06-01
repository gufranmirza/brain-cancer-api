import numpy as np

import scipy.ndimage
from skimage import measure

# Plotly
import plotly
import plotly.figure_factory as ff

from plotly.tools import FigureFactory as FF


def get_pixels_hu(slices):
    print("Generating Pixel Data")
    image = np.stack([s.pixel_array for s in slices])
    # Convert to int16 (from sometimes int16),
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 0
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0

    return np.array(image, dtype=np.int16)


def resample(image, scan, new_spacing=[1,1,1]):
    print(" Resampleing pixel data ")

    spacing = np.array([scan[0].SliceThickness] + scan[0].PixelSpacing, dtype=np.float32)

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor, mode='nearest')

    return image, new_spacing


def make_mesh(image, threshold=-300, step_size=1):

    print("Transposing surface")
    p = image.transpose(2,1,0)

    verts, faces, norm, val = measure.marching_cubes_lewiner(p, threshold, step_size=step_size, allow_degenerate=True)
    return verts, faces


def plotly_3d(verts, faces):
    x,y,z = zip(*verts)

    print("Drawing")

    # Make the colormap single color since the axes are positional not intensity.
    # colormap=['rgb(255,105,180)','rgb(255,255,51)','rgb(0,191,255)']
    colormap=['rgb(236, 236, 212)','rgb(236, 236, 212)']

    fig = ff.create_trisurf(
        x=x,
        y=y,
        z=z,
        plot_edges=False,
        colormap=colormap,
        simplices=faces,
        backgroundcolor='rgb(64, 64, 64)',
        title="Interactive Visualization"
    )
    plotly.offline.plot(fig, filename="temp.html")
