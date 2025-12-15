import FreeCAD as App       # type: ignore
import Part                 # type: ignore
from FreeCAD import Vector  # type: ignore

doc = App.newDocument("TestFitPiece")

# Main test block: (0, 0, 0) -> (45, 12, 8)
main_block = Part.makeBox(45, 12, 8)
current_shape = main_block

# Cut 1: (6, 0, 0) -> (45, 6, 8)
cut1 = Part.makeBox(
    45 - 6,
    6 - 0,
    8 - 0,
    Vector(6, 0, 0)
)
current_shape = current_shape.cut(cut1)

# Cut 2: (24, 6, 0) -> (39, 9, 8)
cut2 = Part.makeBox(
    39 - 24,
    9 - 6,
    8 - 0,
    Vector(24, 6, 0)
)
current_shape = current_shape.cut(cut2)

# Add to document
obj = doc.addObject("Part::Feature", "Test_Piece")
obj.Shape = current_shape
doc.recompute()
