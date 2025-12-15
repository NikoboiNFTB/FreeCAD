import FreeCAD as App       # type: ignore
import Part                 # type: ignore
from FreeCAD import Vector  # type: ignore

doc = App.newDocument("PhoneHolderAIEnhanced")

# Main block
main_block = Part.makeBox(50, 50, 31)
current_shape = main_block

# Cut 1
cut1 = Part.makeBox(42.25, 50, 15.5, Vector(7.75, 0, 7.75))
current_shape = current_shape.cut(cut1)

# Cut 2
cut2 = Part.makeBox(25, 15.5, 7.75, Vector(25, 16.25, 0))
current_shape = current_shape.cut(cut2)

# Large cylinder and subtract smaller cylinder
base_point = Vector(25, 25, 31)
large_cyl = Part.makeCylinder(23, 28, base_point)
small_cyl = Part.makeCylinder(11, 28, base_point)

current_shape = current_shape.fuse(large_cyl)
current_shape = current_shape.cut(small_cyl)

# Additional blocks
new_blocks = [
    (2, 25, 22, Vector(24, 12.5, 31)),
    (25, 2, 22, Vector(12.5, 24, 31)),
    (25, 15.5, 12, Vector(0, 16.25, -12)),
]

for length, width, height, pos in new_blocks:
    blk = Part.makeBox(length, width, height, pos)
    current_shape = current_shape.fuse(blk)

# Cable cut
cable_cut = Part.makeCylinder(2, 15.5)
cable_cut.Placement = App.Placement(Vector(17, 31.75, -6), App.Rotation(Vector(1, 0, 0), 90))
current_shape = current_shape.cut(cable_cut)

# Additional cut boxes
cut_boxes = [
    (17, 15.5, 4, Vector(0, 16.25, -8)),        # Charger Cut
    (2, 15.5, 10, Vector(0, 16.25, -12)),        # Charger Threads Cut
    (25, 19.5, 2, Vector(25, 14.25, 5.75)),     # Shelf Slide Cut
    (2, 19.5, 7.75, Vector(48, 14.25, 0)),      # Shelf Slide Cut
    (2, 50, 19.5, Vector(48, 0, 5.75)),         # Wall Cut
    (7, 4, 7.75, Vector(43, 31.75, 0)),         # Bolt Cut
    (2, 2, 7.75, Vector(41, 31.75, 0)),         # Bolt Slide Cut
    (2, 2, 2, Vector(41, 33.75, 5.75)),
    (2, 2, 7.75, Vector(48, 35.75, 0)),
    (7, 2, 2, Vector(41, 35.75, 5.75)),
]

for length, width, height, pos in cut_boxes:
    box = Part.makeBox(length, width, height, pos)
    current_shape = current_shape.cut(box)

# Cylinders (wires or supports)
cyl_positions = [
    ((2, 16.25, -2), (2, 31.75, -2)),           # Charger Thread
    ((2, 16.25, -10), (2, 31.75, -10)),         # Charger Thread
    ((48, 0, 25.25), (48, 50, 25.25)),          # Wall Thread
    ((48, 0, 5.75), (48, 14.25, 5.75)),         # Wall Thread
    ((48, 37.75, 5.75), (48, 50, 5.75)),        # Wall Thread
    ((25, 14.25, 5.75), (48, 14.25, 5.75)),     # Shelf Thread
    ((25, 33.75, 5.75), (41, 33.75, 5.75)),
    ((48, 14.25, 0), (48, 14.25, 5.75)),
    ((41, 33.75, 0), (41, 33.75, 5.75)),
    ((41, 33.75, 5.75), (41, 37.75, 5.75)),
    ((48, 37.75, 0), (48, 37.75, 5.75)),
    ((48, 37.75, 5.75), (41, 37.75, 5.75)),
]

for start, end in cyl_positions:
    start_v = Vector(*start)
    end_v = Vector(*end)
    direction = end_v - start_v
    height = direction.Length
    axis = direction.normalize()
    rotation = App.Rotation(Vector(0, 0, 1), direction)
    cyl = Part.makeCylinder(2, height)
    cyl.Placement = App.Placement(start_v, rotation)
    current_shape = current_shape.fuse(cyl)

# Add spheres
sphere_pos = [
    Vector(48, 14.25, 5.75),
    Vector(41, 33.75, 5.75),
    Vector(48, 37.75, 5.75),
]

spheres = [Part.makeSphere(2, pos) for pos in sphere_pos]

for s in spheres:
    current_shape = current_shape.fuse(s)

# Create final object in document
final_obj = doc.addObject("Part::Feature", "Final_Model")
final_obj.Shape = current_shape
doc.recompute()
