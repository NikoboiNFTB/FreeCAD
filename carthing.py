import FreeCAD as App
import Part

doc = App.newDocument("HollowCarvedPyramid")

# Outer pyramid dimensions
base_x = 73.0
base_y = 34.0
top_x  = 64.0
top_y  = 28.0
height = 19.0

# Carve-out rectangle
c0 = App.Vector(0, 0, 13)
c1 = App.Vector(73, 0, 13)
c2 = App.Vector(73, 24, 13)
c3 = App.Vector(0, 24, 13)

# Build outer pyramid
offset_x = (base_x - top_x) / 2.0
offset_y = (base_y - top_y) / 2.0

b0 = App.Vector(0, 0, 0)
b1 = App.Vector(base_x, 0, 0)
b2 = App.Vector(base_x, base_y, 0)
b3 = App.Vector(0, base_y, 0)
base_face = Part.Face(Part.makePolygon([b0, b1, b2, b3, b0]))

t0 = App.Vector(offset_x, offset_y, height)
t1 = App.Vector(offset_x + top_x, offset_y, height)
t2 = App.Vector(offset_x + top_x, offset_y + top_y, height)
t3 = App.Vector(offset_x, offset_y + top_y, height)
top_face = Part.Face(Part.makePolygon([t0, t1, t2, t3, t0]))

outer = Part.makeLoft([base_face, top_face], True)

# Carve front section
carve_face = Part.Face(Part.makePolygon([c0, c1, c2, c3, c0]))
carve_solid = carve_face.extrude(App.Vector(0, 0, 16))
cut_outer = outer.cut(carve_solid)

# Inner pyramid dimensions
inner_base_x = 69.0
inner_base_y = 30.0
inner_height = 11.0

# Wall thickness
wall = 2.0

# Taper shrink
shrink_x = ((base_x - top_x) / 2.0) * (inner_height / height)
shrink_y = ((base_y - top_y) / 2.0) * (inner_height / height)

inner_top_x = inner_base_x - 2 * shrink_x
inner_top_y = inner_base_y - 2 * shrink_y

# Inner base
ib0 = App.Vector(wall, wall, 0)
ib1 = App.Vector(wall + inner_base_x, wall, 0)
ib2 = App.Vector(wall + inner_base_x, wall + inner_base_y, 0)
ib3 = App.Vector(wall, wall + inner_base_y, 0)
inner_base_face = Part.Face(Part.makePolygon([ib0, ib1, ib2, ib3, ib0]))

# Inner top
it0 = App.Vector(wall + shrink_x, wall + shrink_y, inner_height)
it1 = App.Vector(wall + shrink_x + inner_top_x, wall + shrink_y, inner_height)
it2 = App.Vector(wall + shrink_x + inner_top_x, wall + shrink_y + inner_top_y, inner_height)
it3 = App.Vector(wall + shrink_x, wall + shrink_y + inner_top_y, inner_height)
inner_top_face = Part.Face(Part.makePolygon([it0, it1, it2, it3, it0]))

inner = Part.makeLoft([inner_base_face, inner_top_face], True)

hollow = cut_outer.cut(inner)

# Clip 1
clip1 = Part.makeBox(
    44.5 - 28.5,   # dx = 16 mm
    3,             # dy
    2,             # dz
    App.Vector(28.5, 0.5, 0)
)

# Clip 2
clip2 = Part.makeBox(
    44.5 - 28.5,
    3,
    2,
    App.Vector(28.5, 30.5, 0)
)

with_clips = hollow.fuse([clip1, clip2])

obj = doc.addObject("Part::Feature", "ClippedHollowPyramid")
obj.Shape = with_clips
doc.recompute()
