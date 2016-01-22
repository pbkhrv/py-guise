"Describe and compare data shapes"
from functools import partial
from numbers import Number
import operator as op
from collections import Callable

def is_of_class(clazz, obj):
    "True if obj.__class__ == clazz"
    return hasattr(obj, '__class__') and obj.__class__ == clazz

def is_of_class_and_value(clazz, val, obj):
    "True if obj is of particular type and value"
    return is_of_class(clazz, obj) and obj == val

def each_fits_one_of(shapes, obj):
    """True if obj is a list or tuple of non-zero length
       and each element fits one of given shapes"""
    return isinstance(obj, (list, tuple)) and len(obj) > 0 and \
        all(any(shp(item) for shp in shapes) for item in obj)

def each_fits_in_order(shapes, obj):
    """True if obj is a list or tuple of same length as shapes
       and each element of obj fits item from shapes in order"""
    return isinstance(obj, (list, tuple)) and len(obj) == len(shapes) and \
        all(shape(item) for shape, item in zip(shapes, obj))

def each_kv_fits_one_of(kvshapes, obj):
    """True if obj is a dict and each key-value pair of obj
       fits one of the specified key-shape/value-shape pairs"""
    return isinstance(obj, dict) and \
        all(any(ks(k) and vs(v) for ks, vs in kvshapes) \
            for k, v in obj.items())

def each_kvshape_is_used(kvshapes, obj):
    "True if obj is a dict and each given key-shape/value-shape is found in obj"
    return isinstance(obj, dict) and \
        all(any(ks(k) and vs(v) for k, v in obj.items()) \
            for ks, vs in kvshapes)

def empty_list_or_tuple(obj):
    "True if obj is an empty list or tuple"
    return isinstance(obj, (list, tuple)) and len(obj) == 0

def empty_dict(obj):
    "True of obj is an empty dict"
    return isinstance(obj, dict) and len(obj) == 0

NUMERIC_TYPES = (int, float)
SIMPLE_TYPES = (str, unicode, bool)
CONTAINER_TYPES = (list, tuple, dict)

def shape(shp):
    "Turn shape definition into a callable 'does this obj fit?' function"
    if shp is None:
        return lambda obj: obj is None
    elif isinstance(shp, type) and shp in SIMPLE_TYPES + CONTAINER_TYPES + NUMERIC_TYPES:
        return partial(is_of_class, shp)
    elif isinstance(shp, type) and shp == Number:
        return lambda obj: isinstance(obj, shp) and not isinstance(obj, bool)
    elif isinstance(shp, Number) and not isinstance(shp, bool):
        return partial(op.eq, shp)
    elif isinstance(shp, SIMPLE_TYPES):
        return partial(is_of_class_and_value, shp.__class__, shp)
    elif isinstance(shp, list) and len(shp) > 0:
        shapes = [shape(s) for s in shp]
        return partial(each_fits_one_of, shapes)
    elif isinstance(shp, tuple) and len(shp) > 0:
        shapes = [shape(s) for s in shp]
        return partial(each_fits_in_order, shapes)
    elif isinstance(shp, (list, tuple)) and len(shp) == 0:
        return empty_list_or_tuple
    elif isinstance(shp, dict) and len(shp) > 0:
        kvshapes = [(shape(k), shape(v)) for k, v in shp.items()]
        return lambda obj: each_kv_fits_one_of(kvshapes, obj) and \
                           each_kvshape_is_used(kvshapes, obj)
    elif isinstance(shp, dict) and len(shp) == 0:
        return empty_dict
    elif isinstance(shp, Callable):
        return shp
    else:
        raise ValueError('Unknown shape type specified')

def fit(shp, obj):
    "True if obj fits the shape defined by shp"
    return shape(shp)(obj)
