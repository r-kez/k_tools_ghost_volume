import bpy
import blf
import gpu
import mathutils
from gpu_extras.batch import batch_for_shader
from bpy_extras import view3d_utils
from .logic import UNIT_DATA

# -------------------------------------------------------------------------
# GPU Drawing Handlers
# -------------------------------------------------------------------------

def draw_callback_px():
    """Draw volume information in the 3D Viewport overlay"""
    # Use bpy.context to avoid _RestrictContext issues
    context = bpy.context
    scene = context.scene
    props = scene.k_volume
    if hasattr(props, "measure_mode") and props.measure_mode == 'SPECIFIC':
        obj = props.target_object
    else:
        obj = context.active_object
    
    if not props.show_overlay:
        return

    if not obj or obj.type != 'MESH':
        return

    # Calculate center position in 3D
    coord = obj.matrix_world @ (0.125 * sum((mathutils.Vector(v) for v in obj.bound_box), mathutils.Vector()))
    
    # Project to 2D screen space
    region = context.region
    rv3d = context.region_data
    pos_2d = view3d_utils.location_3d_to_region_2d(region, rv3d, coord)

    if pos_2d:
        font_id = 0
        volume = props.result
        
        # Drawing Text logic
        blf.size(font_id, 18)
        
        # Background shadow/glow for readability
        blf.color(font_id, 0, 0, 0, 0.7)
        blf.position(font_id, pos_2d.x + 1, pos_2d.y - 1, 0)
        
        # Main Text
        unit_key = props.unit
        mult, label = UNIT_DATA.get(unit_key, (1.0, "ml"))
        display_vol = volume * mult
        
        # Change color based on volume (vibrant cyan)
        blf.color(font_id, 0.2, 0.8, 1.0, 1.0)
        blf.position(font_id, pos_2d.x, pos_2d.y, 0)
        blf.draw(font_id, f"{obj.name}: {display_vol:,.2f} {label}")

    # Draw Waterline Indicator
    if props.use_waterline:
        # Simple text for waterline height
        blf.size(font_id, 14)
        blf.color(font_id, 0.2, 0.5, 1.0, 0.8)
        # Position at top-left of the 3D region for info
        blf.position(font_id, 20, 50, 0)
        blf.draw(font_id, f"Liquid Height: {props.waterline_z:.3f}m")

def draw_callback_3d():
    """Draw a 3D preview plane for the waterline"""
    # Use bpy.context to avoid _RestrictContext issues
    context = bpy.context
    scene = context.scene
    
    if not scene or not hasattr(scene, "k_volume"):
        return
    
    props = scene.k_volume
    if not props.use_waterline or not props.show_waterline_plane:
        return
        
    if hasattr(props, "measure_mode") and props.measure_mode == 'SPECIFIC':
        obj = props.target_object
    else:
        obj = context.active_object
    if not obj or obj.type != 'MESH':
        return

    # Calculate plane bounds and base Z
    bbox = [obj.matrix_world @ mathutils.Vector(v) for v in obj.bound_box]
    min_x = min(v.x for v in bbox)
    max_x = max(v.x for v in bbox)
    min_y = min(v.y for v in bbox)
    max_y = max(v.y for v in bbox)
    min_z = min(v.z for v in bbox)
    
    # Add some padding
    margin = (max_x - min_x + max_y - min_y) * 0.1
    min_x -= margin; max_x += margin
    min_y -= margin; max_y += margin
    
    # Effective Z is base of object + offset
    z = min_z + props.waterline_z
    
    # 3D Plane coordinates
    coords = [
        (min_x, min_y, z), (max_x, min_y, z),
        (max_x, max_y, z), (min_x, max_y, z)
    ]
    
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": coords})
    
    # Draw transparent plane
    gpu.state.blend_set('ALPHA')
    shader.bind()
    shader.uniform_float("color", (0.1, 0.4, 0.9, 0.25)) # Water blue
    batch.draw(shader)
    
    # Draw outline
    shader.uniform_float("color", (0.2, 0.6, 1.0, 0.8)) # Brighter blue
    indices = [(0, 1), (1, 2), (2, 3), (3, 0)]
    outline_batch = batch_for_shader(shader, 'LINES', {"pos": coords}, indices=indices)
    outline_batch.draw(shader)
    
    gpu.state.blend_set('NONE')

# -------------------------------------------------------------------------
# Registration
# -------------------------------------------------------------------------

_handle_2d = None
_handle_3d = None

def register():
    global _handle_2d, _handle_3d
    _handle_2d = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, (), 'WINDOW', 'POST_PIXEL')
    _handle_3d = bpy.types.SpaceView3D.draw_handler_add(draw_callback_3d, (), 'WINDOW', 'POST_VIEW')

def unregister():
    global _handle_2d, _handle_3d
    if _handle_2d is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_handle_2d, 'WINDOW')
        _handle_2d = None
    if _handle_3d is not None:
        bpy.types.SpaceView3D.draw_handler_remove(_handle_3d, 'WINDOW')
        _handle_3d = None
