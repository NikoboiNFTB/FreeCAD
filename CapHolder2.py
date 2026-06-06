import FreeCAD as App       # type: ignore
import Part                 # type: ignore
import math                 # type: ignore
from FreeCAD import Vector  # type: ignore
from typing import List     # type: ignore

doc = App.newDocument("CapHolderAIEnhanced")


def create_base_box(doc, length: float, width: float, height: float):
    """Create the base box object."""
    main_block = doc.addObject("Part::Box", "Base")
    main_block.Length = length
    main_block.Width = width
    main_block.Height = height
    doc.recompute()
    return main_block


def create_cut_box(length: float, width: float, height: float, position: Vector):
    """Create a cut box with the given dimensions and position."""
    return Part.makeBox(length, width, height, position)


def perform_cut(doc, obj, cut_box):
    """Perform a cut operation on the given object using the cut box."""
    cut_shape = obj.Shape.cut(cut_box)
    cut_obj = doc.addObject("Part::Feature", f"Cut")
    cut_obj.Shape = cut_shape
    doc.removeObject(obj.Name)
    doc.recompute()
    return cut_obj


def add_cylinder_between_points(doc, p1: Vector, p2: Vector, radius: float = 1.0, name: str = "Cylinder"):
    """Add a cylinder between the given points."""
    direction = p2.sub(p1)
    height = direction.Length
    z_axis = Vector(0, 0, 1)
    axis = z_axis.cross(direction)

    angle = math.degrees(z_axis.getAngle(direction))
    cyl = Part.makeCylinder(radius, height)

    if axis.Length > 0:
        cyl.rotate(Vector(0, 0, 0), axis, angle)

    cyl.translate(p1)

    obj = doc.addObject("Part::Feature", name)
    obj.Shape = cyl
    doc.recompute()
    return obj


def add_sphere_at_point(doc, p: Vector, radius: float = 1.0, name: str = "Sphere"):
    """Add a sphere at the given point."""
    sphere = Part.makeSphere(radius)
    sphere.translate(p)
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = sphere
    doc.recompute()
    return obj


def fuse_objects(doc, objects: List):
    """Fuse the given objects into a single object."""
    if len(objects) < 2:
        print("Not enough objects to fuse.")
        return None

    fused_shape = objects[0].Shape
    for obj in objects[1:]:
        fused_shape = fused_shape.fuse(obj.Shape)

    fused_obj = doc.addObject("Part::Feature", "Fused")
    fused_obj.Shape = fused_shape

    for obj in objects:
        obj.ViewObject.Visibility = False

    doc.recompute()
    print("Fusion complete.")
    return fused_obj


def get_all_objects(doc):
    """Get all objects in the document."""
    return [obj for obj in doc.Objects if isinstance(obj, Part.Feature)]


def optimize_cap_holder(doc):
    """Optimize the cap holder design."""
    # Create the base box
    main_block = create_base_box(doc, 31.5, 127.5, 31.5)

    # Perform the cuts
    cut_boxes = [
        (31.5, 8, 15.5, Vector(0, 0, 16)),
        (31.5, 31.5, 23.5, Vector(0, 8, 8)),
        (31.5, 80, 15.5, Vector(0, 47.5, 8)),
        (15.5, 80, 31.5, Vector(8, 47.5, 0)),
        (8, 74, 8, Vector(23.5, 53.5, 23.5)),
        (1, 80, 1, Vector(7, 47.5, 23.5)),
        (1, 80, 1, Vector(7, 47.5, 7)),
        (1, 80, 1, Vector(23.5, 47.5, 7)),
        (1, 6, 1, Vector(23.5, 47.5, 23.5)),
        (1, 1, 8, Vector(7, 126.5, 23.5)),
        (1, 1, 8, Vector(7, 126.5, 0)),
        (1, 1, 8, Vector(23.5, 52.5, 23.5)),
        (1, 1, 8, Vector(23.5, 126.5, 0)),
        (8, 1, 1, Vector(0, 126.5, 23.5)),
        (8, 1, 1, Vector(0, 126.5, 7)),
        (8, 1, 1, Vector(23.5, 52.5, 23.5)),
        (8, 1, 1, Vector(23.5, 126.5, 7)),
        (31.5, 1, 1, Vector(0, 39.5, 30.5)),
        (31.5, 1, 1, Vector(0, 7, 15)),
        (31.5, 1, 1, Vector(0, 0, 15))
    ]

    cut_obj = main_block
    for cut_box in cut_boxes:
        cut_obj = perform_cut(doc, cut_obj, create_cut_box(*cut_box))

    # Add the cylinders
    cylinder_positions = [
        ((7, 47.5, 24.5), (7, 126.5, 24.5)),
        ((7, 47.5, 7), (7, 126.5, 7)),
        ((24.5, 47.5, 7), (24.5, 126.5, 7)),
        ((24.5, 47.5, 24.5), (24.5, 52.5, 24.5)),
        ((0, 126.5, 24.5), (7, 126.5, 24.5)),
        ((0, 126.5, 7), (7, 126.5, 7)),
        ((24.5, 126.5, 7), (31.5, 126.5, 7)),
        ((24.5, 52.5, 24.5), (31.5, 52.5, 24.5)),
        ((7, 126.5, 24.5), (7, 126.5, 31.5)),
        ((7, 126.5, 0), (7, 126.5, 7)),
        ((24.5, 126.5, 0), (24.5, 126.5, 7)),
        ((24.5, 52.5, 24.5), (24.5, 52.5, 31.5)),
        ((0, 40.5, 30.5), (31.5, 40.5, 30.5)),
        ((0, 7, 15), (31.5, 7, 15)),
        ((0, 1, 15), (31.5, 1, 15)),
    ]

    for i, (p1, p2) in enumerate(cylinder_positions):
        add_cylinder_between_points(doc, Vector(*p1), Vector(*p2), name=f"Cylinder_{i}")


# Run the design generation
optimize_cap_holder(doc)

# Get all objects in the document
objects_to_fuse = get_all_objects(doc)

# Fuse all objects into one
fused_object = fuse_objects(doc, objects_to_fuse)

