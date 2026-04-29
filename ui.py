import bpy
from .logic import UNIT_DATA

class VIEW3D_PT_CalculateVolume(bpy.types.Panel):
    """Sidebar panel for K-Tools Ghost Volume"""
    bl_label = "Ghost Volume"
    bl_idname = "VIEW3D_PT_ghost_volume"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'K-Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.k_volume
        obj = context.active_object

        # 1. Main Status & Toggle
        col = layout.column(align=True)
        is_running = props.realtime
        
        row = col.row(align=True)
        row.scale_y = 1.8 # Large prominent button
        state_icon = 'PAUSE' if is_running else 'PLAY'
        state_text = "ENGINE ACTIVE" if is_running else "START ENGINE"
        row.prop(props, "realtime", text=state_text, icon=state_icon, toggle=True)
        
        if is_running:
            sub = col.row(align=True)
            sub.scale_y = 0.9
            sub.prop(props, "refresh_rate", text="Rate", icon='TIME')
            sub.prop(props, "use_precision", text="High Precision", icon='CHECKMARK' if props.use_precision else 'BLANK1', toggle=True)

        layout.separator(factor=1.5)

        if not obj or obj.type != 'MESH':
            layout.label(text="Select a Mesh to begin", icon='INFO')
            return

        # 2. Hero Display Section
        box = layout.box()
        col = box.column(align=True)
        col.label(text="CURRENT MEASUREMENT", icon='MOD_PHYSICS')
        
        hero = col.row(align=True)
        hero.scale_y = 1.5
        
        unit_key = props.unit
        mult, label = UNIT_DATA.get(unit_key, (1.0, "ml"))
        display_vol = props.result * mult
        
        # Display volume prominently
        hero.label(text=f"{display_vol:,.2f} {label}")
        hero.prop(props, "unit", text="")
        hero.prop(props, "show_overlay", text="", icon='HIDE_OFF' if props.show_overlay else 'HIDE_ON', toggle=True)

        layout.separator(factor=1.0)

        # 3. Source & Filters
        col = layout.column(align=True)
        row = col.row()
        row.label(text="VOLUME SOURCE", icon='GROUP_VERTEX')
        
        src_box = col.box()
        s_row = src_box.row(align=True)
        s_row.prop(props, "use_selection", text="", icon='RESTRICT_SELECT_OFF')
        s_row.prop_search(obj, "k_volume_vg", obj, "vertex_groups", text="Target Group")

        layout.separator(factor=1.0)

        # 4. Virtual Liquid Level
        col = layout.column(align=True)
        row = col.row()
        row.label(text="VIRTUAL LIQUID", icon='MOD_OCEAN')
        
        wat_box = col.box()
        l_row = wat_box.row(align=True)
        l_row.prop(props, "use_waterline", text="Liquid Plane", toggle=True)
        l_row.prop(props, "show_waterline_plane", text="", icon='HIDE_OFF' if props.show_waterline_plane else 'HIDE_ON', toggle=True)
        
        if props.use_waterline:
            wat_box.prop(props, "waterline_z", text="Fill Height")

        # 5. Utilities & Manual Override
        if not is_running:
            layout.separator(factor=1.5)
            layout.operator("object.calculate_volume_ml", text="Refresh Measurement", icon='FILE_REFRESH')

        layout.separator()
        layout.label(text=f"Object: {obj.name}", icon='OBJECT_DATA')


def register():
    bpy.utils.register_class(VIEW3D_PT_CalculateVolume)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_CalculateVolume)
