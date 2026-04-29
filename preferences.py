import bpy

class KVolumeAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        col = box.column(align=True)
        col.label(text="K-Tools: Ghost Volume", icon='MOD_PHYSICS')
        col.label(text="High-precision physical volume prototyping with Ghost Proxy technology.", icon='BLANK1')
        
        layout.separator()
        
        row = layout.row(align=True)
        
        # Left side: About/Support
        left = row.column()
        left.label(text="Support & Links:", icon='HELP')
        left.operator("wm.url_open", text="Report an Issue", icon='URL').url = "https://github.com/r-kez/k_tools_ghost_volume/issues"
        left.operator("wm.url_open", text="Repository / Docs", icon='HELP').url = "https://github.com/r-kez/k_tools_ghost_volume"
        
        # Right side: Creator/Branding
        right = row.column()
        right.label(text="Developed by:", icon='USER')
        right.label(text="Robert Kezives", icon='BLANK1')
        right.operator("wm.url_open", text="Creator Profile", icon='WORLD').url = "https://github.com/r-kez"

def register():
    bpy.utils.register_class(KVolumeAddonPreferences)

def unregister():
    bpy.utils.unregister_class(KVolumeAddonPreferences)
