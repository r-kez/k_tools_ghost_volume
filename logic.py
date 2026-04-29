import bpy
import bmesh
import mathutils

# -------------------------------------------------------------------------
# Constants & Units
# -------------------------------------------------------------------------

UNIT_DATA = {
    'ML': (1.0, "ml"),
    'L': (0.001, "L"),
    'M3': (0.000001, "m³"),
    'OZ': (0.033814, "fl oz")
}

# -------------------------------------------------------------------------
# Core Calculation Logic
# -------------------------------------------------------------------------

def calc_volume_logic(obj, scene, depsgraph=None):
    """Core logic to calculate volume of a mesh object in ml"""
    if not obj or obj.type != 'MESH':
        return 0.0

    # Get property group
    props = scene.k_volume
    
    bm = bmesh.new()
    
    # Use Edit Mesh BMesh if in Edit Mode for live dragging feedback
    if obj.mode == 'EDIT':
        bm_edit = bmesh.from_edit_mesh(obj.data)
        bm.free()
        bm = bm_edit.copy()
    else:
        # If no depsgraph is provided (e.g. manual button), get it from context
        if depsgraph is None:
            depsgraph = bpy.context.evaluated_depsgraph_get()
        
        obj_eval = obj.evaluated_get(depsgraph)
        bm.from_mesh(obj_eval.data)
    
    # Apply world matrix
    bm.transform(obj.matrix_world)
    
    # Properties from scene/object
    use_selection = props.use_selection
    vg_name = obj.k_volume_vg
    vg_index = obj.vertex_groups.find(vg_name)
    
    use_waterline = props.use_waterline
    waterline_height = props.waterline_z
    use_precision = props.use_precision

    # Calculate volume (BU^3)
    volume_bu = 0.0
    
    # Calculate Base Z and Effective Waterline (Relative to object/selection bottom)
    base_z = 0.0
    if bm.verts:
        base_z = min(v.co.z for v in bm.verts)
    
    effective_z = base_z + waterline_height

    if use_precision:
        # PRECISION MODE: Physical Ghost Proxy (Exact but heavier)
        
        # 1. Selection Filtering: Delete faces NOT in the assigned Vertex Group
        if use_selection and vg_index != -1:
            dvert_layer = bm.verts.layers.deform.active
            if not dvert_layer and bm.verts.layers.deform:
                dvert_layer = bm.verts.layers.deform[0]
                
            faces_to_delete = []
            for face in bm.faces:
                is_in_group = True
                if dvert_layer:
                    for v in face.verts:
                        if vg_index not in v[dvert_layer]:
                            is_in_group = False
                            break
                else:
                    is_in_group = False
                
                if not is_in_group:
                    faces_to_delete.append(face)
            
            if faces_to_delete:
                bmesh.ops.delete(bm, geom=faces_to_delete, context='FACES')

        # 2. Waterline Bisect: Cut the mesh and cap it at the specified height
        if use_waterline:
            # Ensure we have geometry to bisect
            if bm.faces:
                bmesh.ops.bisect_plane(
                    bm, 
                    geom=bm.verts[:] + bm.edges[:] + bm.faces[:],
                    plane_co=(0, 0, effective_z),
                    plane_no=(0, 0, 1),
                    clear_outer=True, # Remove everything ABOVE the waterline
                    clear_inner=False
                )

        # 3. Final Capping: Close any remaining holes
        boundary_edges = [e for e in bm.edges if e.is_boundary]
        if boundary_edges:
            bmesh.ops.holes_fill(bm, edges=boundary_edges)

        # Final Calculation on the solid proxy
        volume_bu = abs(bm.calc_volume())
    
    else:
        # FAST MODE: Mathematical Summation (Lightweight but assumes planar caps)
        if use_waterline or use_selection:
            # Re-use the Vertex Group filtering logic without deleting geometry
            dvert_layer = None
            if use_selection and vg_index != -1:
                dvert_layer = bm.verts.layers.deform.active
                if not dvert_layer and bm.verts.layers.deform:
                    dvert_layer = bm.verts.layers.deform[0]

            for face in bm.faces:
                is_in_group = True
                if use_selection and vg_index != -1:
                    if dvert_layer:
                        for v in face.verts:
                            if vg_index not in v[dvert_layer]:
                                is_in_group = False
                                break
                    else:
                        is_in_group = False

                if is_in_group:
                    verts = face.verts
                    v0 = verts[0].co
                    for i in range(1, len(verts) - 1):
                        v1 = verts[i].co
                        v2 = verts[i+1].co
                        area_xy = 0.5 * ((v1.x - v0.x) * (v2.y - v0.y) - (v2.x - v0.x) * (v1.y - v0.y))
                        ref_z = effective_z if use_waterline else 0.0
                        avg_z = (v0.z + v1.z + v2.z) / 3.0
                        volume_bu += area_xy * (avg_z - ref_z)
            volume_bu = abs(volume_bu)
        else:
            volume_bu = abs(bm.calc_volume())

    bm.free()

    # Unit Conversion (BU^3 -> m^3 -> ml)
    scale = scene.unit_settings.scale_length
    volume_m3 = volume_bu * (scale ** 3)
    volume_ml = volume_m3 * 1_000_000
    
    return volume_ml
