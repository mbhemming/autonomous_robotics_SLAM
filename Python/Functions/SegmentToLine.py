import math

import numpy as np

def SegmentToLine(x1,y1,x2,y2):
    m=(y1-y2)/(x1-x2)
    b=y1-m*x1
    return m,b

