import bpy
import math
from .logic import calc_volume_logic, UNIT_DATA

# -------------------------------------------------------------------------
# Timer Callback & Management
# -------------------------------------------------------------------------

def volume_timer_callback():
    """Periodic callback to update volume"""
    context = bpy.context
    scene = context.scene
    
    # Safety check for scene.k_volume
    if not hasattr(scene, "k_volume"):
        return None
        
    props = scene.k_volume
    
    # Check if we should stop the timer
    if not props.realtime:
        return None

    if props.measure_mode == 'SPECIFIC':
        obj = props.target_object
    else:
        obj = context.active_object
        
    if obj and obj.type == 'MESH':
        # Perform calculation
        props.result = calc_volume_logic(obj, scene)
        
    return props.refresh_rate

def update_realtime_toggle(self, context):
    """Callback when the Start/Stop property is toggled"""
    if self.realtime:
        # Start timer
        if not bpy.app.timers.is_registered(volume_timer_callback):
            bpy.app.timers.register(volume_timer_callback)
    else:
        # Stop timer
        if bpy.app.timers.is_registered(volume_timer_callback):
            bpy.app.timers.unregister(volume_timer_callback)

# -------------------------------------------------------------------------
# Operators
# -------------------------------------------------------------------------

class OBJECT_OT_CalculateVolumeML(bpy.types.Operator):
    """Calculate the volume of the active mesh in ml (Manual)"""
    bl_idname = "object.calculate_volume_ml"
    bl_label = "Update Volume (ml)"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if not hasattr(context.scene, "k_volume"): return False
        props = context.scene.k_volume
        obj = props.target_object if props.measure_mode == 'SPECIFIC' else context.active_object
        return obj is not None and obj.type == 'MESH'

    def execute(self, context):
        scene = context.scene
        props = scene.k_volume
        obj = props.target_object if props.measure_mode == 'SPECIFIC' else context.active_object
        
        # Calculate
        vol_ml = calc_volume_logic(obj, scene)
        
        # Store result
        scene.k_volume.result = vol_ml
        
        self.report({'INFO'}, f"Volume: {vol_ml:,.2f} ml")
        return {'FINISHED'}

class OBJECT_OT_ScaleToTargetVolume(bpy.types.Operator):
    """Scale the object uniformly to match the Target Volume in selected units"""
    bl_idname = "object.scale_to_target_volume"
    bl_label = "Scale to Target"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if not hasattr(scene, "k_volume"): return False
        props = scene.k_volume
        obj = props.target_object if props.measure_mode == 'SPECIFIC' else context.active_object
        return obj and obj.type == 'MESH' and scene.k_volume.result > 0.001

    def execute(self, context):
        scene = context.scene
        props = scene.k_volume
        obj = props.target_object if props.measure_mode == 'SPECIFIC' else context.active_object
        
        v_current_ml = props.result
        
        # Convert user-input target to ML for calculation
        unit_key = props.unit
        mult, label = UNIT_DATA.get(unit_key, (1.0, "ml"))
        
        # Target in ml = (User Value) / (Unit Multiplier)
        # e.g. If User wants 1L, Target_ML = 1 / 0.001 = 1000ml. Correct.
        v_target_ml = props.target_volume / mult
        
        if v_current_ml <= 0:
            self.report({'ERROR'}, "Current volume is zero. Cannot scale.")
            return {'CANCELLED'}
            
        # Calculate uniform scale factor based on ML volumes
        ratio = v_target_ml / v_current_ml
        scale_factor = math.pow(ratio, 1/3)
        
        # Apply scaling
        obj.scale *= scale_factor
        
        # Recalculate to confirm
        props.result = calc_volume_logic(obj, scene)
        
        self.report({'INFO'}, f"Scaled to {props.target_volume}{label} (Factor: {scale_factor:.4f}x)")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_CalculateVolumeML)
    bpy.utils.register_class(OBJECT_OT_ScaleToTargetVolume)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CalculateVolumeML)
    bpy.utils.unregister_class(OBJECT_OT_ScaleToTargetVolume)
    # Ensure timer is stopped
    if bpy.app.timers.is_registered(volume_timer_callback):
        bpy.app.timers.unregister(volume_timer_callback)
