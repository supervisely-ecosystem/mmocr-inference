import supervisely as sly

def det_polygon_2_label(rect, obj_class: sly.ObjClass):
    rect = list(map(int, rect))
    x,y = rect[::2], rect[1::2]
    xmin, ymin, xmax, ymax = min(x), min(y), max(x), max(y)
    rect = sly.Rectangle(ymin, xmin, ymax, xmax)
    label = sly.Label(rect, obj_class)
    return label