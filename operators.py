import bpy
from .logic import calc_volume_logic

# -------------------------------------------------------------------------
# Timer Callback & Management
# -------------------------------------------------------------------------

def volume_timer_callback():
    """Periodic callback to update volume"""
    context = bpy.context
    scene = context.scene
    props = scene.k_volume
    
    # Check if we should stop the timer
    if not props.realtime:
        return None

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
        return context.active_object is not None and context.active_object.type == 'MESH'

    def execute(self, context):
        obj = context.active_object
        scene = context.scene
        
        # Calculate
        vol_ml = calc_volume_logic(obj, scene)
        
        # Store result
        scene.k_volume.result = vol_ml
        
        self.report({'INFO'}, f"Volume: {vol_ml:,.2f} ml")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_CalculateVolumeML)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CalculateVolumeML)
    # Ensure timer is stopped
    if bpy.app.timers.is_registered(volume_timer_callback):
        bpy.app.timers.unregister(volume_timer_callback)
