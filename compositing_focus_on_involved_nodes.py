# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Focus on involved nodes",
    "description": "Unhides all nodes that lead up to the selected one and hides all others.",
    "category": "Node",
    "author": "Konrad Kleine",
    "version": (1, 0),
    "blender": (2, 69, 0),
    "location": "Node Editor > Node > Focus on involved nodes",
	"wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Compositing/FocusOnInvolvedNodes",
    "category": "Compositing",
	"warning": ""
}

import bpy

# Unhides all nodes that lead up to @a node by following its inputs
# links and nodes recursively.
def unhide_involved_nodes(node):
    node.hide = False
    for input in node.inputs:
        if not input.is_linked:
            continue
        for link in input.links:
            unhide_involved_nodes(link.from_node)


class FocusOnInvolvedNodes(bpy.types.Operator):
    """Focus On Involved Nodes"""
    bl_idname = "nodes.focus_on_involved_nodes"
    bl_label = "Focus on involved nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):       
        scene = context.scene
        cursor = scene.cursor_location
        if not scene.use_nodes:
            return {'FINISHED'}
        tree = scene.node_tree
        active_node = tree.nodes.active
        if not active_node:
            return {'FINISHED'}
        # First hide all other nodes
        for node in tree.nodes:
            node.hide=True                   
        # Then unhide all the nodes that lead up to the active node
        unhide_involved_nodes(active_node)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(FocusOnInvolvedNodes.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(FocusOnInvolvedNodes)
    bpy.types.NODE_MT_node.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='NODE_EDITOR', region_type='WINDOW')
    kmi = km.keymap_items.new(FocusOnInvolvedNodes.bl_idname, 'H', 'PRESS', alt=True)
    addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(FocusOnInvolvedNodes)
    bpy.types.NODE_MT_node.remove(menu_func)
   
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()