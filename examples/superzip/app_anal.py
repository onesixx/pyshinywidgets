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

from ipyleaflet import Map, Polyline

Korea_center = (36.355, 127.766)
Greenwich_center = (0,0)
map = leaf.Map(center=Greenwich_center, zoom=2)
line0N = Polyline( locations=[(0,0), ( 90,0)], color="red", fill=False)
line0S = Polyline( locations=[(0,0), (-90,0)], color="blue", fill=False)
line180E = Polyline( locations=[(0, 180), ( 90, 180)], color="red", fill=False)
line180W = Polyline( locations=[(0,-180), (-90,-180)], color="blue", fill=False)
map.add_layer(line0N)
map.add_layer(line0S)
map.add_layer(line180E)
map.add_layer(line180W)
display(map)


map = leaf.Map(
    center=(37.45, -88.85),
    zoom=4,
    scroll_wheel_zoom=True,
    attribution_control=False,
    #layout=ipywidgets.Layout(width="100%", height="100%"),
)
marker = leaf.Marker(location=(37.45, -88.85), draggable = True)
map.add(marker)
# map.add_layer(leaf.basemap_to_tiles(basemaps.CartoDB.DarkMatter))
display(map)

# locs = allzips[["Lat", "Long", input.variable()]].to_numpy()
locs = allzips[["Lat", "Long", "Score"]].to_numpy()

heatmap = leaf.Heatmap(
    locations=locs.tolist(),
    name="heatmap",
    #R> cat(paste0(round(scales::rescale(log10(1:10), to = c(0.05, 1)), 2), ": '", viridis::viridis(10), "'"), sep = "\n")
    # gradient={
    #     0.05: "#440154",
    #     0.34: "#482878",
    #     0.5: "#3E4A89",
    #     0.62: "#31688E",
    #     0.71: "#26828E",
    #     0.79: "#1F9E89",
    #     0.85: "#35B779",
    #     0.91: "#6DCD59",
    #     0.96: "#B4DE2C",
    #     1: "#FDE725",
    # },
)
map.add_layer(heatmap)
display(map)

import plotly.figure_factory as ff


def zips_in_bounds():
    #bb = reactive_read(map, "bounds")
    bb = map.bounds
    if not bb:
        # TODO: this should really be `raise SilentException`...why doesn't it work?
        # return pd.DataFrame()
        raise SilentException

    lats = (bb[0][0], bb[1][0])
    lons = (bb[0][1], bb[1][1])
    return allzips[
        (allzips.Lat >= lats[0])
        & (allzips.Lat <= lats[1])
        & (allzips.Long >= lons[0])
        & (allzips.Long <= lons[1])
    ]

zip_selected

# denstiry_plot
# density_plot(
#             allzips,
#             zips_in_bounds(),
#             selected=zip_selected(),
#             var="Score",
#             title="Overall Score",
#             showlegend=True,
#         )
overall = allzips
in_bounds = zips_in_bounds()
var = "Score"
selected =
dat = [overall[var], in_bounds[var]]

fig = ff.create_distplot(        dat,
        ["Overall", "In bounds"],
        colors=["black", "#6DCD59"],
        show_rug=False,
        show_hist=False,
    )

go.FigureWidget(data=fig.data, layout=fig.layout)





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
