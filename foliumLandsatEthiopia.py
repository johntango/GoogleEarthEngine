# See https://www.youtube.com/watch?v=AD1YtRqc5kA
import ee
import folium


# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize()

countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
Ethiopia = countries.filter(ee.Filter.eq('country_na', 'Ethiopia'))
landsat = ee.ImageCollection(
    'LANDSAT/LC08/C01/T1').filterDate('2016-01-01', '2017-01-01').filterBounds(Ethiopia)
composite = ee.Algorithms.Landsat.simpleComposite(**{
    'collection': landsat,
    'asFloat': True
})
rgbVis = {'bands': ['B3', 'B4'], 'min': 0, 'max': 0.3}
nirVis = {'bands': ['B5', 'B4'], 'min': 0, 'max': [0.5, 0.3]}


def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.fileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy:; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)


folium.Map.add_ee_layer = add_ee_layer

my_map = folium.Map(location=[9, 39], zoom_start=6)
my_map.add_ee_layer(composite, rgbVis, 'RGB')
my_map.add_ee_layer(composite, nirVis, 'false Color')

my_map.add_child(folium.LayerControl())

display(my_map)
