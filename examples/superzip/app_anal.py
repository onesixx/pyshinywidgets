import os
from typing import List, Optional, Tuple

import ipyleaflet as leaf
import ipywidgets
import matplotlib as mpl
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objs as go
from ipyleaflet import basemaps
from matplotlib import cm

vars = {
    "Score": "Overall score",
    "College": "% college educated",
    "Income": "Median income",
    "Population": "Population",
}

app_dir = os.path.dirname(__file__)
allzips = pd.read_csv(os.path.join(app_dir, "superzip.csv")).sample(
    n=10000, random_state=42
)




map = leaf.Map(
    center=(37.45, -88.85),
    zoom=4,
    scroll_wheel_zoom=True,
    attribution_control=False,
    #layout=ipywidgets.Layout(width="100%", height="100%"),
)
# map.add_layer(leaf.basemap_to_tiles(basemaps.CartoDB.DarkMatter))
map

# locs = allzips[["Lat", "Long", input.variable()]].to_numpy()
locs = allzips[["Lat", "Long", "Score"]].to_numpy()

leaf.Heatmap(
    locations=locs.tolist(),
    name="heatmap",
    # R> cat(paste0(round(scales::rescale(log10(1:10), to = c(0.05, 1)), 2), ": '", viridis::viridis(10), "'"), sep = "\n")
    gradient={
        0.05: "#440154",
        0.34: "#482878",
        0.5: "#3E4A89",
        0.62: "#31688E",
        0.71: "#26828E",
        0.79: "#1F9E89",
        0.85: "#35B779",
        0.91: "#6DCD59",
        0.96: "#B4DE2C",
        1: "#FDE725",
    },
)


zips = zips_in_bounds()
if not show_markers():
    remove_heatmap()
    map.add_layer(layer_heatmap())
else:
    zip_colors = dict(zip(zips.Zipcode, zips_marker_color()))
    for x in map.layers:
        if x.name.startswith("marker-"):
            zipcode = int(x.name.split("-")[1])
            if zipcode in zip_colors:
                x.color = zip_colors[zipcode]
