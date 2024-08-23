import unreal

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

def replace_asset(original, replacement):
    # Load the original and replacement assets
    original_asset = unreal.EditorAssetLibrary.load_asset(original)
    replacement_asset = unreal.EditorAssetLibrary.load_asset(replacement)
    
    # Ensure both assets are loaded
    if original_asset and replacement_asset:
        # Consolidate the original asset into the replacement asset
        unreal.EditorAssetLibrary.consolidate_assets(replacement_asset, [original_asset])
        unreal.log(f"Replaced {original} with {replacement}")
    else:
        unreal.log_warning("One or both of the assets could not be loaded.")

# Example usage: replace an old asset with a new one
#replace_asset("/Game/0e_2_SMod_Mark/3D_Assets/e_3DM_CAV1/Cavern_RockCliff_01", "/Game/SMod_Mark/3D_Assets/e_3DM_CAV1/Cavern_RockCliff_01")

sm_paths_to_remove = list_static_meshes_in_directory("/Game/0e_2_SMod_Mark/3D_Assets/e_MMC_W357/")
sm_paths_to_keep = list_static_meshes_in_directory("/Game/SMod_Mark/3D_Assets/e_MMC_W357/")

for sm_toRemove in sm_paths_to_remove:
    for sm_toKeep in sm_paths_to_keep:
        if sm_toRemove.split("/")[-1] in sm_toKeep.split("/")[-1]:
            #print(sm_repl.split("/")[-1])
            print(sm_toKeep, " repl: ", sm_toRemove)
            #() REPLACE
            replace_asset(sm_toRemove, sm_toKeep)
            #exit()

print(len(sm_paths_to_remove))
print(len(sm_paths_to_keep))
