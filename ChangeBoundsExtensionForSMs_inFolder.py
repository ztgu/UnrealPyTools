import unreal

#() STEP1: First change pivot to middle of object! and bake using Pivot Tool Plugin
#() STEP2: UE
#() Change each SM build scale to 2x or something else and defined here:
scale_factor = 2.0  # Set to the desired scale factor
#PS: This script changes bounds extension to 0 first
#() STEP3: Then run script! # The directory path with static meshes. Recalculate bounds extensions
directory_path = "/Game/e_3DM_MODW/StaticMeshes/WoodenShacks/"

def list_static_meshes_in_directory(directory_path):
    # Get all asset paths in the specified directory
    asset_paths = unreal.EditorAssetLibrary.list_assets(directory_path, recursive=True, include_folder=False)
    
    # Filter and list static meshes
    static_meshes = []
    for asset_path in asset_paths:
        # Check if asset exists
        if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
            # Get asset data
            asset_data = unreal.EditorAssetLibrary.find_asset_data(asset_path)
            # Use get_class() and compare to StaticMesh class
            if asset_data.get_class() == unreal.StaticMesh.static_class():
                static_meshes.append(asset_path)
    
    # Return the list of static meshes
    return static_meshes

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

# List static meshes in the specified directory and store the result
static_meshes_list = list_static_meshes_in_directory(directory_path)

# Go through he list of static meshes
if static_meshes_list:
    unreal.log("Static Meshes in directory '" + directory_path + "':")
    for static_mesh_asset_path in static_meshes_list:
        unreal.log(static_mesh_asset_path)

        # Don't check subdirectories! Only static meshes in given directory path last folder:
        if (directory_path.split("/")[-2] in static_mesh_asset_path.split("/")[-2]):
            #() Set bounds extensions to zero
            set_SM_BoundsExtensionTo0Default(static_mesh_asset_path, scale_factor)

            #() Recalculate the static mesh bounds
            recalculate_static_mesh_bounds(static_mesh_asset_path, scale_factor)
        
else:
    unreal.log("No static meshes found in directory '" + directory_path + "'.")
