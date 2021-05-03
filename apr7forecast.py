from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
import numpy as np
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                         cartopy_ylim, latlon_coords, ALL_TIMES)

# Lots of code borrowed from the wrf python tutorial

def plot_t(ncfile, name):
    # Get temperature in C
    temp00 = getvar(ncfile, "tc", timeidx = 0)
    temp06 = getvar(ncfile, "tc", timeidx = 2)
    temp12 = getvar(ncfile, "tc", timeidx = 4)
    temp18 = getvar(ncfile, "tc", timeidx = 6)
    temp24 = getvar(ncfile, "tc", timeidx = 8)
    temps = [temp00, temp06, temp12, temp18, temp24]
     
    # Get the latitude and longitude points
    lats, lons = latlon_coords(temp00)

    # Get the cartopy mapping object
    cart_proj = get_cartopy(temp00)

    # fake while loop :P
    hour = 0

    for t in temps:
        # smooth
        smooth_t = smooth2d(t, 3, cenweight=4)
        print(np.shape(to_np(smooth_t)))

        # Create a figure
        fig = plt.figure(figsize=(12,6))
        # Set the GeoAxes to the projection used by WRF
        ax = plt.axes(projection=cart_proj)

        # Download and add the states and coastlines
        states = NaturalEarthFeature(category="cultural", scale="50m",
            facecolor="none", name="admin_1_states_provinces_shp")
        ax.add_feature(states, linewidth=.5, edgecolor="black")
        ax.coastlines('50m', linewidth=0.8)

        # Make the contours for temp
        plt.contourf(to_np(lons), to_np(lats), to_np(smooth_t), 10,
            transform=crs.PlateCarree(), cmap=get_cmap("jet"))

        # Add a color bar
        plt.colorbar(ax=ax, shrink=.98)

        # Set the map bounds
        ax.set_xlim(cartopy_xlim(smooth_t))
        ax.set_ylim(cartopy_ylim(smooth_t))

        # Add the gridlines
        ax.gridlines(color="black", linestyle="dotted")
        date = "2021-04-07T00:00:00"
        time = date + "+" + str(hour) + " hours"
        plt.title("Temperature (C), " + time)
    
        plt.savefig(name + str(hour) + ".png")
        plt.show()
        hour += 6

if __name__ == "__main__":
    # Open the NetCDF file
    ncfile1 = Dataset("wrfout_d01_2021-04-07_00:00:00")
    ncfile2 = Dataset("wrfout_d01_2021-04-07_00:00:00")
    plot_t(ncfile1, "d1T")
    plot_t(ncfile2, "d2T")

