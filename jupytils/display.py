################################################################################
#    Jupytils: Display and geospatial utils for Jupytern notebook (python)
#
#    AUTHOR: Matthew Hanson
#    EMAIL:  matt.a.hanson@gmail.com
#
#    Copyright (C) 2016 Matthew Hanson
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
################################################################################

import numpy as np
from matplotlib import pyplot as plt
from skimage.transform import downscale_local_mean


def display_image(band, nodata=np.nan, title=''):
    """ Display image in current plot """
    img = np.ma.masked_where(band == nodata, band)
    plt.set_cmap('gray')
    plt.axis('off')
    plt.title(title)
    return plt.imshow(img)


def display_and_plot_hist(band, nodata=np.nan, **kwargs):
    """ Display image and plot histogram side by side """
    ar = float(band.shape[1])/float(band.shape[0])
    plt.figure(figsize=(20*ar, 10))
    plt.subplot(1, 2, 1)
    # downscale image
    maxsize = 2000
    factor = min(band.shape[1]/maxsize, band.shape[0]/maxsize)
    band = downscale_local_mean(band, (factor, factor))
    display_image(band, nodata=nodata, **kwargs)
    plt.subplot(1, 2, 2)
    inds = np.where(band != nodata)
    plt.hist(band[inds], bins=256)


def display_image_and_vector(image, geoimg, df, title=''):
    nodata = geoimg[0].nodata()
    ar = float(image.shape[1])/float(image.shape[0])
    fig, axes = plt.subplots(figsize=(20*ar, 10), nrows=1, ncols=2)
    plt.sca(axes[0])
    display_image(image, nodata, title=title)
    # display vector
    pt0 = geoimg.minxy()
    pt1 = geoimg.maxxy()
    axes[1].set_xlim([pt0.x(), pt1.x()])
    axes[1].set_ylim([pt0.y(), pt1.y()])
    ax = df.plot(ax=axes[1], linewidth=3.0, color='Red')
    plt.title(title)
