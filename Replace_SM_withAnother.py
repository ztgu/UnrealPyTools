import unreal

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
replace_asset("/Game/0e_2_SMod_Mark/3D_Assets/e_3DM_CAV1/Cavern_Wall_Narrow_02", "/Game/SMod_Mark/3D_Assets/e_3DM_CAV1/Cavern_Wall_Narrow_02")

