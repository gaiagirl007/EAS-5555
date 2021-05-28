from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
import numpy as np
from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                         cartopy_ylim, latlon_coords, ALL_TIMES)

ncfile = Dataset("wrfout_d01_2012-03-18_00:00:00")

# Lots of code borrowed from the wrf python tutorial

# Get temperature in C
temps = getvar(ncfile, "tc")
print(np.shape(to_np(temps)))

# Get the latitude and longitude points
lats, lons = latlon_coords(temps)
lat_np, lon_np = to_np(lats), to_np(lons)

# Get the cartopy mapping object
cart_proj = get_cartopy(temps)

# fake while loop :P
hour = 0

for t in temps:
    
    smooth_t = smooth2d(t, 3, cenweight = 4)
    t_np = to_np(smooth_t)
    
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
    plt.contourf(lon_np, lat_np, t_np, 10,
        transform=crs.PlateCarree(), cmap=get_cmap("jet"))

    # Add a color bar
    plt.colorbar(ax=ax, shrink=.98)

    # Set the map bounds
    ax.set_xlim(cartopy_xlim(smooth_t))
    ax.set_ylim(cartopy_ylim(smooth_t))

    # Add the gridlines
    ax.gridlines(color="black", linestyle="dotted")
    date = "2021-04-07T00:00:00"
    time = date + "+" + str(hour)
    plt.title("Temperature (C), " + time)
    
    strhr = str(hour) if hour > 9 else "0" + str(hour)
    plt.savefig("d01T" + strhr + ".png")
    plt.close()
    hour += 1



#if __name__ == "__main__":
    # Open the NetCDF file
 #   ncfile2 = Dataset("wrfout_d01_2021-04-07_00:00:00")
  #  plot_t(ncfile1, "d1T")
   # plot_t(ncfile2, "d2T")

