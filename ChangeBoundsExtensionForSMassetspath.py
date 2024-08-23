import unreal

#() STEP1: First change pivot to middle of object! and bake using Pivot Tool Plugin
#() STEP2: UE
#() Change each SM build scale to 2x or something else, defined here:
scale_factor = 5.0  # Set to the desired scale factor

#() STEP3: Then run script! Recalculate bounds extensions
# Define file paths to the static mesh assets and use the desired scale factor
sm_assets = """
/Game/e_3DM_ME17/Meshes/Props/SM_Root_01
/Game/e_3DM_ME17/Meshes/Props/SM_Root_02
/Game/e_3DM_ME17/Meshes/Props/SM_Root_03
/Game/e_3DM_ME17/Meshes/Props/SM_Root_04
/Game/e_3DM_ME17/Meshes/Props/SM_Root_05
/Game/e_3DM_ME17/Meshes/Props/SM_Root_06
/Game/e_3DM_ME17/Meshes/Props/SM_Root_07
/Game/e_3DM_ME17/Meshes/Props/SM_Root_08
"""

def set_SM_BoundsExtensionTo0Default(asset_path, scale_factor):
    # Load the static mesh asset
    static_mesh = unreal.EditorAssetLibrary.load_asset(asset_path)
    
    if not static_mesh or not isinstance(static_mesh, unreal.StaticMesh):
        unreal.log_error("Failed to load Static Mesh: " + asset_path)
        return
    
    unreal.log("Loaded Static Mesh: " + asset_path)

    # Set positive and negative bounds extensions to zero
    positive_extension = unreal.Vector(0, 0, 0)
    negative_extension = unreal.Vector(0, 0, 0)
    
    # Apply the bounds extensions
    static_mesh.set_editor_property("positive_bounds_extension", positive_extension)
    static_mesh.set_editor_property("negative_bounds_extension", negative_extension)
    
    # Log the updated bounds for verification
    updated_bounds = static_mesh.get_bounding_box()
    unreal.log("Updated Bounds: Min=" + str(updated_bounds.min) + " Max=" + str(updated_bounds.max))
    
    # Save the asset
    success = unreal.EditorAssetLibrary.save_asset(asset_path)
    
    if success:
        unreal.log("Successfully updated and saved Static Mesh with new bounds: " + asset_path)
    else:
        unreal.log_error("Failed to save Static Mesh: " + asset_path)

def recalculate_static_mesh_bounds(asset_path, scale_factor):
    # Load the static mesh asset
    static_mesh = unreal.EditorAssetLibrary.load_asset(asset_path)
    
    if not static_mesh or not isinstance(static_mesh, unreal.StaticMesh):
        unreal.log_error("Failed to load Static Mesh: " + asset_path)
        return
    
    unreal.log("Loaded Static Mesh: " + asset_path)
    
    # Get the original bounding box
    original_bounds = static_mesh.get_bounding_box()
    
    # Calculate the original center and extents
    original_center = (original_bounds.max + original_bounds.min) * 0.5
    original_extent = (original_bounds.max - original_bounds.min) * 0.5

    # Calculate the new extents based on the scaling factor
    new_extent = original_extent * scale_factor

    # Calculate the positive and negative bounds extensions
    positive_extension = new_extent - original_extent
    negative_extension = positive_extension  # Both extensions should be the same

    # Apply the bounds extensions
    static_mesh.set_editor_property("positive_bounds_extension", positive_extension)
    static_mesh.set_editor_property("negative_bounds_extension", positive_extension)
    
    # Log the updated bounds for verification
    updated_bounds = static_mesh.get_bounding_box()
    unreal.log("Updated Bounds: Min=" + str(updated_bounds.min) + " Max=" + str(updated_bounds.max))
    
    # Save the asset
    success = unreal.EditorAssetLibrary.save_asset(asset_path)
    
    if success:
        unreal.log("Successfully updated and saved Static Mesh with new bounds: " + asset_path)
    else:
        unreal.log_error("Failed to save Static Mesh: " + asset_path)


for static_mesh_asset_path in sm_assets.split("\n"):
    print(static_mesh_asset_path)

    #() Set bounds extensions to zero
    set_SM_BoundsExtensionTo0Default(static_mesh_asset_path, scale_factor)

    #() Recalculate the static mesh bounds
    recalculate_static_mesh_bounds(static_mesh_asset_path, scale_factor)

