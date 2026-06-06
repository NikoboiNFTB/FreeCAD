import FreeCAD as App   # type: ignore
import Part             # type: ignore
from FreeCAD import Vector # type: ignore



# New document
doc = App.newDocument("TestCable")



# Base block - minimal flat 16x16 with 4mm thickness height
base_block = Part.makeBox(16, 26, 4)
base_obj = doc.addObject("Part::Feature", "Base_Block")
base_obj.Shape = base_block
doc.recompute()



# Add Cable Holder - 16x26x4 is now 16x16x4 since width limited to base width
cable_holder = Part.makeBox(16, 26, 4)
cable_holder.translate(Vector(16, 0, 0))  # shifted right, sticking out from base block

main_block = doc.Objects[-1]
fused_shape = main_block.Shape.fuse(cable_holder)

fused_obj = doc.addObject("Part::Feature", "With_Cable_Holder")
fused_obj.Shape = fused_shape

main_block.ViewObject.Visibility = False
doc.recompute()



# Cut Cable - cylinder cut through the holder to simulate cable slot
cyl_radius = 2
cyl_height = 4

cyl = Part.makeCylinder(cyl_radius, cyl_height)
cyl.translate(Vector(24, 13, 0))  # centered height-wise on cable holder and base height

main_block = doc.Objects[-1]
cut_shape = main_block.Shape.cut(cyl)

cut_obj = doc.addObject("Part::Feature", "Cable_Cut")
cut_obj.Shape = cut_shape

main_block.ViewObject.Visibility = False
doc.recompute()



# Cut Shaft - small rectangular cut, reduced height to 4
cut_box = Part.makeBox(8, 3, 4, Vector(24, 11.5, 0))

main_block = doc.Objects[-1]
cut_shape = main_block.Shape.cut(cut_box)

cut_block = doc.addObject("Part::Feature", "Insert_Cut")
cut_block.Shape = cut_shape

main_block.ViewObject.Visibility = False
doc.recompute()



# Cut Corner 1 - 1x1x4 cube cut at corner
cut_box = Part.makeBox(2, 2, 4, Vector(30, 9.5, 0))

main_block = doc.Objects[-1]
cut_shape = main_block.Shape.cut(cut_box)

cut_block = doc.addObject("Part::Feature", "Cut_Corner_1")
cut_block.Shape = cut_shape

main_block.ViewObject.Visibility = False
doc.recompute()



# Cut Corner 2 - another corner cut
cut_box = Part.makeBox(2, 2, 4, Vector(30, 14.5, 0))

main_block = doc.Objects[-1]
cut_shape = main_block.Shape.cut(cut_box)

cut_block = doc.addObject("Part::Feature", "Cut_Corner_2")
cut_block.Shape = cut_shape

main_block.ViewObject.Visibility = False
doc.recompute()



# Add Cylinder 1 and Fuse - smaller cylinders with height 4
cyl_radius = 2
cyl_height = 4
cyl_position = Vector(30, 9.5, 0)

cylinder = Part.makeCylinder(cyl_radius, cyl_height)
cylinder.translate(cyl_position)

main_block = doc.Objects[-1]
fused_shape = main_block.Shape.fuse(cylinder)

fused_obj = doc.addObject("Part::Feature", "Cylinder_1")
fused_obj.Shape = fused_shape

main_block.ViewObject.Visibility = False
doc.recompute()



# Add Cylinder 2 and Fuse
cyl_position = Vector(30, 16.5, 0)

cylinder = Part.makeCylinder(cyl_radius, cyl_height)
cylinder.translate(cyl_position)

main_block = doc.Objects[-1]
fused_shape = main_block.Shape.fuse(cylinder)

fused_obj = doc.addObject("Part::Feature", "Cylinder_2")
fused_obj.Shape = fused_shape

main_block.ViewObject.Visibility = False
doc.recompute()







# Cut Shaft - small rectangular cut, reduced height to 4
cut_box = Part.makeBox(16, 26, 4, Vector(0, 0, 0))

main_block = doc.Objects[-1]
cut_shape = main_block.Shape.cut(cut_box)

cut_block = doc.addObject("Part::Feature", "Insert_Cut")
cut_block.Shape = cut_shape

main_block.ViewObject.Visibility = False
doc.recompute()

