import bpy

class KVolumeProperties(bpy.types.PropertyGroup):
    result: bpy.props.FloatProperty(
        name="Volume Result",
        description="Last calculated volume in ml",
        default=0.0,
        precision=2
    ) # type: ignore
    
    measure_mode: bpy.props.EnumProperty(
        name="Mode",
        description="Choose how to select the object for volume calculation",
        items=[
            ('ACTIVE', 'Active Selected', 'Dynamically calculate volume for the active selection'),
            ('SPECIFIC', 'Specific Object', 'Lock calculation to a specific object only'),
        ],
        default='ACTIVE'
    ) # type: ignore
    
    target_object: bpy.props.PointerProperty(
        name="Target Object",
        description="Specific object to measure. If empty, uses active object",
        type=bpy.types.Object
    ) # type: ignore
    
    target_volume: bpy.props.FloatProperty(
        name="Target Volume",
        description="Target volume to match when scaling (in ml)",
        default=500.0,
        min=0.001,
        precision=2
    ) # type: ignore
    
    realtime: bpy.props.BoolProperty(
        name="Real-time Volume",
        description="Calculate volume automatically on changes",
        default=False,
        update=lambda self, context: __import__(__package__ + '.operators', fromlist=['update_realtime_toggle']).update_realtime_toggle(self, context)
    ) # type: ignore
    
    refresh_rate: bpy.props.FloatProperty(
        name="Refresh Rate",
        description="Time in seconds between updates",
        default=0.25,
        min=0.01,
        max=5.0,
        precision=2
    ) # type: ignore
    
    show_overlay: bpy.props.BoolProperty(
        name="Show Overlay",
        description="Show the volume result text in the 3D viewport",
        default=False
    ) # type: ignore
    
    use_selection: bpy.props.BoolProperty(
        name="Use Selection",
        description="Only calculate volume for assigned faces in Vertex Group",
        default=False
    ) # type: ignore
    
    use_waterline: bpy.props.BoolProperty(
        name="Use Waterline",
        description="Cap the volume at a specific Z height",
        default=False
    ) # type: ignore
    
    waterline_z: bpy.props.FloatProperty(
        name="Liquid Height",
        description="The height of the liquid from the bottom of the geometry",
        default=0.0,
        precision=3,
        min=0.0
    ) # type: ignore
    
    show_waterline_plane: bpy.props.BoolProperty(
        name="Show Preview",
        description="Show the blue liquid surface plane in the viewport",
        default=True
    ) # type: ignore
    
    unit: bpy.props.EnumProperty(
        name="Unit",
        description="Measurement unit for the volume display",
        items=[
            ('ML', 'Milliliters', 'Calculate in ml'),
            ('L', 'Liters', 'Calculate in L'),
            ('M3', 'Cubic Meters', 'Calculate in m³'),
            ('OZ', 'Fluid Ounces', 'Calculate in fl oz'),
        ],
        default='ML'
    ) # type: ignore
    
    use_precision: bpy.props.BoolProperty(
        name="Precision Mode",
        description="Use heavy BMesh operators for exact capping (better for open meshes)",
        default=True
    ) # type: ignore

def register():
    bpy.utils.register_class(KVolumeProperties)
    bpy.types.Scene.k_volume = bpy.props.PointerProperty(type=KVolumeProperties)
    
    # Object property
    bpy.types.Object.k_volume_vg = bpy.props.StringProperty(
        name="Volume Group",
        description="Vertex group to use for volume calculation"
    ) # type: ignore

def unregister():
    bpy.utils.unregister_class(KVolumeProperties)
    del bpy.types.Scene.k_volume
    del bpy.types.Object.k_volume_vg
