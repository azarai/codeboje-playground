auth= 'simplegeoauth'
secret = 'simplegeosecret'

image_width = 500

import codecs
import simplegeo.context
from pysvg.structure import svg
from pysvg.shape import path
from pysvg.builders import *

import math, traceback, sys
from decimal import *
from os import path, makedirs

def merc_x(lon):
    r_major=6378137.000
    return r_major*math.radians(lon)
 
def merc_y(lat):
    if lat > Decimal("89.5"):
        lat = 89.5
    if lat < Decimal("-89.5"):
        lat = -89.5
    r_major = 6378137.000
    r_minor = 6356752.314245179
    temp = r_minor / r_major
    eccent = math.sqrt(1.0 - temp ** 2)
    phi = math.radians(lat)
    sinphi = math.sin(phi)
    con = eccent * sinphi
    com = eccent / 2
    con = ((1.0 - con) / (1.0 + con)) ** com
    ts = math.tan((math.pi / 2.0 - phi) / 2.0) / con
    y = 0 - r_major * math.log(ts)
    return y


def get_bbox(polygon, min_x, max_x, min_y, max_y):
    for p in polygon:
        lng,lat = p
        if lng < min_x:
            min_x = lng
        if lng > max_x:
            max_x = lng
        if lat < min_y:
            min_y = lat
        if lat > max_y:
            max_y = lat

    return min_x, max_x, min_y, max_y
def draw_country(country_code, capital_coords, file_name, sg_client):
    country_context = sg_client.get_context(capital_coords[0],capital_coords[1])
    #print country_context['features']
    for feature in country_context['features']:
        classifiers = feature['classifiers'][0]
        print feature['classifiers']
        if classifiers['category'] == 'National' and classifiers['type'] == 'Region':
            print feature['name']
            print feature['handle']
            print feature['href']
            country = sg_client.get_feature(feature['handle']).to_dict()
            cgeo = country['geometry']
            min_x =1000
            max_x =-1000
            min_y =1000
            max_y =-1000
            oh=ShapeBuilder()
            if cgeo['type'] == 'MultiPolygon':
                # get bounding box
                for poly in cgeo['coordinates']:
                    geopath = poly[0]
                    min_x, max_x, min_y, max_y = get_bbox(geopath, min_x, max_x, min_y, max_y )

                print min_x, min_y, merc_x(min_x), merc_y(min_y),max_x, max_y
                
                #transform bounding bo to mercator
                merc_x_min = merc_x(min_x)
                merc_y_min = merc_y(min_y)
                merc_y_max = merc_y(max_y)
                #scale to image
                scale = image_width / (merc_x(max_x) - merc_x_min)
                image_height = (merc_y_max - merc_y_min) * scale
                mySVG =svg(image_width, image_height)

                for poly in cgeo['coordinates']:
                    mypoints = ''
                    for p in poly[0]:
                        lng, lat = p
                        x = (merc_x(lng)- merc_x_min ) * scale
                        y = ( (merc_y(lat) -merc_y_min )* -1 * scale) + image_height
                        mypoints += "%s,%s " %(x,y)
                    pl = oh.createPolygon(points=mypoints,stroke=None, fill='red')
                    mySVG.addElement(pl)
                mySVG.save(file_name)
                return True    
            elif cgeo['type'] == 'Polygon':
                min_x, max_x, min_y, max_y = get_bbox(cgeo['coordinates'][0], min_x, max_x, min_y, max_y )
                merc_x_min = merc_x(min_x)
                merc_y_min = merc_y(min_y)
                merc_y_max = merc_y(max_y)
                #scale to image
                scale = image_width / (merc_x(max_x) - merc_x_min)
                image_height = (merc_y_max - merc_y_min) * scale
                mySVG =svg(image_width, image_height)
                mypoints = ''
                for p in cgeo['coordinates'][0]:
                    lng, lat = p
                    x = (merc_x(lng)- merc_x_min ) * scale
                    y = ( (merc_y(lat) -merc_y_min )* -1 * scale) + image_height
                    mypoints += "%s,%s " %(x,y)
                pl = oh.createPolygon(points=mypoints,stroke=None, fill='red')
                mySVG.addElement(pl)
                mySVG.save(file_name)
                return True
          
if __name__ == '__main__':
    client = simplegeo.context.Client(auth, secret)
    outdir = "svg"
    if not path.exists(outdir):
      makedirs(outdir)

    countries_in = codecs.open( "../capitals/countries_capitals.csv", "r", "utf-8" )
    for line in countries_in:
      try:
        if not line.startswith("Country_Code"):
          data = line.split(";")
          file_name = outdir + "/"+data[0] + '.svg'
          if not path.exists(file_name):
            if not draw_country(data[0], [float(data[3]), float(data[4])], file_name, client):
              print data[0] + " failed"
          else:
            print data[0] + " already exists"
      except:
        traceback.print_exc(file=sys.stdout)
    countries_in.close()
            