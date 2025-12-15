import FreeCAD as App       # type: ignore
import Part                 # type: ignore
from FreeCAD import Vector  # type: ignore

doc = App.newDocument("PhoneHolderAIEnhanced")

# Parameters
cyl_radius = 2
cyl_height = 15.5

# Main block
main_block = Part.makeBox(73, 48, 31.5)
current_shape = main_block

# Cut 1
cut1 = Part.makeBox(61.5, 48, 15.5, Vector(12.5, 0, 8))
current_shape = current_shape.cut(cut1)

# Cut 2
cut2 = Part.makeBox(48, 15.5, 8, Vector(25, 16.25, 0))
current_shape = current_shape.cut(cut2)

# Large cylinder and subtract smaller cylinder
base_point = Vector(49, 24, 31.5)
large_cyl = Part.makeCylinder(23, 28, base_point)
small_cyl = Part.makeCylinder(11, 28, base_point)

current_shape = current_shape.fuse(large_cyl)
current_shape = current_shape.cut(small_cyl)

# Additional blocks
new_blocks = [
    (2, 24, 22, Vector(48, 12, 31.5)),
    (24, 2, 22, Vector(37, 23, 31.5)),
    (25, 15.5, 16, Vector(0, 16.25, -16)),
]

for length, width, height, pos in new_blocks:
    blk = Part.makeBox(length, width, height, pos)
    current_shape = current_shape.fuse(blk)

# Cable cut
cable_cut = Part.makeCylinder(cyl_radius, cyl_height)
cable_cut.Placement = App.Placement(Vector(17, 31.75, -8), App.Rotation(Vector(1, 0, 0), 90))
current_shape = current_shape.cut(cable_cut)

# Additional cut boxes
cut_boxes = [
    (17, 15.5, 4, Vector(0, 16.25, -10)),
    (2, 15.5, 2, Vector(0, 16.25, -6)),
    (2, 15.5, 2, Vector(0, 16.25, -12)),
    (2, 15.5, 2, Vector(0, 16.25, -16)),
    (2, 48, 2, Vector(71, 0, 23.5)),
    (2, 48, 2, Vector(71, 0, 6)),
    (2, 2, 8, Vector(71, 14.25, 0)),
    (2, 2, 8, Vector(71, 31.75, 0)),
    (46, 2, 2, Vector(25, 14.25, 6)),
    (46, 2, 2, Vector(25, 31.75, 6)),
    (2, 48, 2, Vector(0, 0, 29.5)),
    (2, 16.25, 2, Vector(0, 0, 0)),
    (2, 16.25, 2, Vector(0, 31.75, 0)),
    (15, 4, 8, Vector(43, 31.75, 0)),
    (2, 2, 8, Vector(41, 31.75, 0)),
    (2, 2, 8, Vector(58, 31.75, 0)),
    (2, 2, 2, Vector(41, 33.75, 6)),
    (2, 2, 2, Vector(58, 33.75, 6)),
]

for length, width, height, pos in cut_boxes:
    box = Part.makeBox(length, width, height, pos)
    current_shape = current_shape.cut(box)

# Cylinders (wires or supports)
cyl_positions = [
    ((2, 31.75, -4), (2, 16.25, -4)),
    ((2, 31.75, -12), (2, 16.25, -12)),
    ((2, 31.75, -14), (2, 16.25, -14)),
    ((71, 0, 6), (71, 14.25, 6)),
    ((71, 33.75, 6), (71, 48, 6)),
    ((71, 14.25, 0), (71, 14.25, 6)),
    ((71, 33.75, 0), (71, 33.75, 6)),
    ((25, 14.25, 6), (71, 14.25, 6)),
    ((25, 33.75, 6), (41, 33.75, 6)),
    ((60, 33.75, 6), (71, 33.75, 6)),
    ((71, 0, 25.5), (71, 48, 25.5)),
    ((2, 0, 29.5), (2, 48, 29.5)),
    ((2, 0, 2), (2, 16.25, 2)),
    ((2, 31.75, 2), (2, 48, 2)),
    ((41, 33.75, 0), (41, 33.75, 6)),
    ((60, 33.75, 0), (60, 33.75, 6)),
    ((41, 33.75, 6), (41, 35.75, 6)),
    ((60, 33.75, 6), (60, 35.75, 6)),
]

for start, end in cyl_positions:
    start_v = Vector(*start)
    end_v = Vector(*end)
    direction = end_v - start_v
    height = direction.Length
    axis = direction.normalize()
    rotation = App.Rotation(Vector(0, 0, 1), direction)
    cyl = Part.makeCylinder(cyl_radius, height)
    cyl.Placement = App.Placement(start_v, rotation)
    current_shape = current_shape.fuse(cyl)

# Add spheres
sphere_pos = [
    Vector(71, 14.25, 6),
    Vector(71, 33.75, 6),
    Vector(41, 33.75, 6),
    Vector(60, 33.75, 6),
]

spheres = [Part.makeSphere(2, pos) for pos in sphere_pos]

for s in spheres:
    current_shape = current_shape.fuse(s)

# Create final object in document
final_obj = doc.addObject("Part::Feature", "Final_Model")
final_obj.Shape = current_shape
doc.recompute()
