"""Blender Node Renderer
Author: andyc06
Version: 0.1.0
Date: 2022-08-04

* This script will render the active camera at the location of each object
in a collection named "FPV_nodes" (first person view nodes) for each
rotation angle listed in the camera_rotations dictionary.
This is intended for use with the "FPV web viewer" project.

* By default this will render the view at each point of an 8-wind compass rose,
with each view being 45 degrees apart (N, NW, W, SW, S, SE, E, NE).

* Any number of angles can be rendered (even just a single angle)
by editing the camera_rotations dictionary.
The key should match the rotation angle

* IMPORTANT: This script will overwrite rendered images on subsequent runs
WITHOUT WARNING, so change the output directory or move completed renders out of
the output directory before rerunning if you want to save them .
"""

import bpy
from pathlib import Path
import math

# Constants
# The current scene
SCENE = bpy.context.scene
# This is the currently active camera
CAMERA = SCENE.camera
# Store the base output path
OUTPUT_DIR = SCENE.render.filepath
# Name of the collection that contains the "nodes" (e.g. empties)
NODE_COLLECTION = "FPV_nodes"
# Camera rotation angles
# X is always 90 in order to point at the horizon
# Compass headings (angles) increase clockwise,
# but Blender rotation increases counter-clockwise,
# so flip the Z rotation to negative to compensate.
ROTATION_ANGLES = {
    0: [math.radians(90), math.radians(0), math.radians(0)],
    45: [math.radians(90), math.radians(0), math.radians(-45)],
    90: [math.radians(90), math.radians(0), math.radians(-90)],
    135: [math.radians(90), math.radians(0), math.radians(-135)],
    180: [math.radians(90), math.radians(0), math.radians(-180)],
    225: [math.radians(90), math.radians(0), math.radians(-225)],
    270: [math.radians(90), math.radians(0), math.radians(-270)],
    315: [math.radians(90), math.radians(0), math.radians(-315)],
}


def get_node_locations() -> list:
    '''Creates a list of dictionaries for each node w/name & location, e.g.:
    [
        {'node': 'node1', 'loc': Vector((-11.520919799804688, -1.73835289478302, 1.202102780342102))},
        {'node': 'node2', 'loc': Vector((-2.2694787979125977, -1.73835289478302, 1.202102780342102))},
        {'node': 'node3', 'loc': Vector((9.29961109161377, -1.73835289478302, 1.202102780342102))},
        {'node': 'node4', 'loc': Vector((16.616485595703125, -1.73835289478302, 1.202102780342102))}
    ]
    '''
    # Empty list to hold dictionaries
    node_locations = []

    # Append a dictionary with the name & location of each object in NODE_COLLECTION to the list
    for obj in bpy.data.collections[NODE_COLLECTION].all_objects:
        n = {"node": obj.name, "loc": obj.location}
        node_locations.append(n)
    
    return node_locations


def render_node_angles(nodes: list) -> None:
    # Iterate through a list of node dictionaries,
    # set the camera location & rotation, and render a frame.
    
    for d in nodes:
        # Set node name variable
        node_name = d.get("node")
        
        # Set camera location
        CAMERA.location = d.get("loc")
        
        for k, v in ROTATION_ANGLES.items():
            # Set camera rotation
            CAMERA.rotation_euler = v
            
            # Node name and rotation angle are included in filename
            output_file = f"{node_name}__angle_{k}.png"
            
            # Set the filepath
            SCENE.render.filepath = str(Path(OUTPUT_DIR, output_file))
            
            # Render the frame
            bpy.ops.render.render(write_still=True)


def run() -> None:
    # Store the list of node dictionaries
    nodes = get_node_locations()

    # Render angles at each node location
    render_node_angles(nodes)
    
    # Reset the output path since it will have the last image file appended
    # to it after render_node_angles() finishes running
    SCENE.render.filepath = OUTPUT_DIR

# This will fire when the script is run in Blender
run()
