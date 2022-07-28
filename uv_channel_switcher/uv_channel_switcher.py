import bpy
from bpy.types import Operator, Panel, PropertyGroup
from bpy.utils import register_class, unregister_class
from bpy.props import PointerProperty, IntProperty


bl_info = {
    "name": "UV channel swticher ",
    "author": "Juri Albreht",
    "version": (1, 0),
    "blender": (3, 1, 2),
    "location": "View3D > OSC",
    "description": "Swtich UV1 and UV2",
    "category": "Object"
}

# This is what goes to panes
class UVSwitcherProperties(PropertyGroup):

    first_uv: IntProperty(
        name='Pixel per meter :  ',
        default=0,
        soft_min=1,
        soft_max=10,
    )

    second_uv: IntProperty(
        name='Pixel per meter :  ',
        default=0,
        soft_min=1,
        soft_max=10,
    )

# Special class to draw UI
class OBJECT_PT_UVSwitcher(Panel):
    bl_label = 'UV channel switcher'
    bl_idname = "OBJECT_PT_UVchannelSwitcher"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Custom'

    def draw(self, context):
        layout = self.layout

        if len(context.scene.objects) > 0:
            button_ui = layout.box()
            button_ui.operator('scene.uv_switcher_button', text='Switch UV channels')
            
            
class UV_switcher(Operator):
    bl_idname = 'scene.uv_switcher_op'
    bl_label = 'Switch_selected_UVs'

    def execute(self, context):
        ob = bpy.context.object
        scene = bpy.context.scene
        
        
class UVSwticher_button(Operator):
    bl_idname = "scene.uv_switcher_button"
    bl_label = "UV swticher button"

    @classmethod
    def poll(cls, context):
        # check the context here
        return context.object is not None

    def execute(self, context):
        selection_names = [obj.name for obj in bpy.context.selected_objects if obj.type == 'MESH']
        
        for x in selection_names:
            ob = bpy.data.objects[x]
            if ob.mode == 'OBJECT':
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = ob
                layers = ob.data.uv_layers
                ob.select_set(True)
                if len(layers) > 2:
                    print('GO')
                    self.report({'ERROR'}, "Model have more than 2 UV channels")
                if len(layers) < 2:
                    self.report({'ERROR'}, "Model have less than 2 UV channels")
                else:
                    print("Switcher")
                    
                    layers.active_index = 0
                    first_layer_name = layers[0].name
                    second_layer_name = layers[1].name
                    bpy.ops.mesh.uv_texture_add()
                    layers.active_index = 0
                    bpy.ops.mesh.uv_texture_remove()
                    layers[0].name = first_layer_name
                    layers[1].name = second_layer_name

            else:
                self.report({'ERROR'}, "Addon work only in Object Mode")
        return {'FINISHED'}

            
            
classes = [OBJECT_PT_UVSwitcher,
            UVSwitcherProperties,
            UVSwticher_button
           ]


def register():
    for cl in classes:
        register_class(cl)
    bpy.types.Scene.uv_switcher = PointerProperty(type=UVSwitcherProperties)


def unregister():
    for cl in reversed(classes):
        unregister_class(cl)


if __name__ == '__main__':
    register()
