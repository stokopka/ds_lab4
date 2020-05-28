from sentinelhub import WmsRequest, WcsRequest, MimeType, CRS, BBox,SHConfig,DataSource,AwsProductRequest,AwsTile,AwsTileRequest
import datetime
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from osgeo import gdal
import sys
sys.path.append(r'C:\Program Files\QGIS 3.12\apps\Python37\Scripts')
import gdal_merge as gm

INSTANCE_ID = 'aa356db4-d4b1-4e8a-9467-74d8a832b85a'  # In case you put instance ID into configuration file you can leave this unchanged

if INSTANCE_ID:
    config = SHConfig()
    config.instance_id = INSTANCE_ID
else:
    config = None

product_id = 'S2A_MSIL2A_20190821T085601_N0213_R007_T36UUA_20190821T115206'
data_folder = './AwsData'

product_request = AwsProductRequest(product_id=product_id,
                                    data_folder=data_folder, safe_format=True)
product_request.save_data()

for i in [10, 20, 60]:
    path = 'A:\lab4\S2A_MSIL2A_20190821T085601_N0213_R007_T36UUA_20190821T115206.SAFE\GRANULE\L2A_T36UUA_A021740_20190821T085815\IMG_DATA\R{}m\\'.format(i)
    in1 = glob.glob(str(path)+('*B02_{}m.jp2').format(i))
    in2 = glob.glob(str(path)+'*B03_{}m.jp2'.format(i))
    in3 = glob.glob(str(path)+'*B04_{}m.jp2'.format(i))
    in4 = glob.glob(str(path)+'*_*_*8*_{}m.jp2'.format(i))
    gm.main(['', '-separate', '-o', 'AR{}.tif'.format(i), in1[0], in2[0], in3[0], in4[0]])

for i in [1, 2, 6]:
    gdal.Warp('12AR{}0.tif'.format(i),'1AR{}0.tif'.format(i),dstSRS="EPSG:4326")

gdal.Warp('final.tif', ['proek_AR10.tif', 'proek_AR20.tif', 'proek_AR60.tif', 'proek_BR10.tif', 'proek_BR20.tif', 'proek_BR60.tif'])


gdal.Warp('WrapedImg.tif', 'AllInOne.tif', format = 'GTiff', cutlineDSName='Kyiv_regions.shp', cutlineLayer = 'extent', cropToCutline = True, dstNodata = 0)