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
        left.operator("wm.url_open", text="Report an Issue", icon='URL').url = "https://github.com/yourusername/calculate-volume/issues"
        left.operator("wm.url_open", text="Documentation", icon='HELP').url = "https://yourwebsite.com/docs"
        
        # Right side: Creator/Branding
        right = row.column()
        right.label(text="Developed by:", icon='USER')
        right.label(text="K-Tools / Jacques Lucke", icon='BLANK1')
        right.operator("wm.url_open", text="Visit Website", icon='WORLD').url = "https://yourwebsite.com"

def register():
    bpy.utils.register_class(KVolumeAddonPreferences)

def unregister():
    bpy.utils.unregister_class(KVolumeAddonPreferences)
