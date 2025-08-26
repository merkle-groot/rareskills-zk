import galois
import numpy as np

GF = galois.GF(71)
(p1_x, p1_y) = (GF(10), GF(15))
(p2_x, p2_y) = (GF(23), GF(29))

slope = (p2_y - p1_y)/(p2_x - p1_x)
constant = -1 * p1_x * slope + p1_y

line_poly = galois.Poly([slope, constant], field=GF)
assert line_poly(10) == 15
assert line_poly(23) == 29

