import cv2
import numpy as np
import cadquery as cq
from shapely import geometry, affinity, ops

def create_mask(image_file):
    image = cv2.imread(image_file)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([60, 0, 0])
    upper = np.array([175, 255, 255])
    img_range = cv2.inRange(image_hsv, lower, upper)

    #kernels for morphology operations
    kernel_noise = np.ones((3,3),np.uint8) 
    kernel_dilate = np.ones((30,30),np.uint8)
    kernel_erode = np.ones((38,38),np.uint8)

    img_erode = cv2.erode(img_range, kernel_noise, 1)
    img_dilate = cv2.dilate(img_erode , kernel_dilate, 1)
    img_mask = cv2.erode(img_dilate, kernel_erode, 1)

    # put mask with green screen on src image
    masked = cv2.bitwise_and(image_rgb, image_rgb, mask = img_mask)

    return masked, img_mask

def create_line_geometry(mask):
    _,thresh = cv2.threshold(mask,27,25,0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_TC89_L1)
    contours_max = max(contours, key=cv2.contourArea)
    
    return contours, contours_max

def generate_stl(points, filepath):
    bladeHeight = 7.5
    bladeWidth = 0.8
    baseHeight = 1.6
    baseWidth = 3.2

    blade = cq.Workplane("XY").polyline(points).offset2D(bladeWidth).extrude(bladeHeight).cut(
        cq.Workplane("XY").polyline(points).close().extrude(bladeHeight)
    )
    base = cq.Workplane("XY").polyline(points).offset2D(baseWidth).extrude(baseHeight).cut(
        cq.Workplane("XY").polyline(points).close().extrude(baseHeight)
    )

    results = blade + base

    cq.exporters.export(results, filepath)

def preprocess_line(points, width=70):
    line = geometry.LinearRing(points).normalize()
    (minx, miny, maxx, maxy) = line.bounds

    line = ops.clip_by_rect(line, minx, miny, maxx, maxy).normalize()
    if line.geom_type == 'MultiLineString':
        lsegs = line.geoms
        r = lsegs[0]
        for l in lsegs[1:]:
            r = r if len(r.coords) > len(l.coords) else l
        line = r

    line = geometry.LinearRing(line.coords)
    xscale = (1.0/maxx)*width
    line = affinity.scale(line, xfact=xscale, yfact=xscale, origin=(0,0,0))

    return line.simplify(0.3)
