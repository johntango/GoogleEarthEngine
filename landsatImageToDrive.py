import ee

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize()

Landsat8 = ee.Image(
    'LANDSAT/LC08/C01/T1_TOA/LC08_170052_20170108').select(['B2', 'B4', 'B3'])
countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
Ethiopia = countries.filter(ee.Filter.eq('country_na', 'Ethiopia'))

landsat = ee.ImageCollection(
    'LANDSAT/LC08/CO1/T1').filterDate('2016-01-01', '2017-01-01').filterBounds(Ethiopia)
composite = ee.Algorithms.Landsat.simpleComposite(**{
    'collection': landsat,
    'asFloat': True
})
rgbVis = {'bands': ['B3]', 'B4'], 'min': 0, 'max': 0.3}
nirVis = {'bands': ['B5]', 'B4'], 'min': 0, 'max': [0.5, 0.3]}

region = ee.Geometry.Rectangle(37.07, 11.50, 37.39, 11.82)
task = ee.batch.Export.image.toDrive(**{'image': Landsat8,
                                        'description': 'imagetoDrive_L8_01',
                                        'folder': 'ExampleEarthEngine',
                                        'scale': 30,
                                        'region': region.getInfo()['coordinates']}
                                     )

task.start()
