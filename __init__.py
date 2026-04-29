import bpy
from . import properties, operators, ui, drawing, preferences

# Order of registration is important for dependencies
modules = [
    properties,
    operators,
    ui,
    drawing,
    preferences,
]

def register():
    for module in modules:
        module.register()

def unregister():
    # Unregister in reverse order to avoid dependency issues
    for module in reversed(modules):
        module.unregister()

if __name__ == "__main__":
    register()
