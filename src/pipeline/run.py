from pathlib import Path

from src.config.paths import DATA_DIR
from src.ingestion.ddragon import update_ddragon, fetch_latest_patch
from src.ingestion.fandom import update_fandom
from src.parsing.ddragon import parse_ddragon_basic_json
from src.parsing.champions import parse_champions_lua
from src.parsing.aram_modifiers import parse_aram_modifiers
from src.merging.canonical import merge_champion_data
from src.loading.load_champions import load_champions_for_patch
from src.utils.versioning import patch_mm


def run_pipeline():
    latest_patch = fetch_latest_patch()
    patch_dir = DATA_DIR / "ddragon" / "raw" / latest_patch

    is_new_patch = not patch_dir.exists()

    if not is_new_patch:
        print(f"Patch {latest_patch} already downloaded. Skipping ingestion.")
        full_patch = latest_patch
    else:
        print(f"New patch detected: {latest_patch}")
        update_fandom()
        full_patch = update_ddragon(keep_only_latest=True)

    patch = patch_mm(full_patch)

    print("Parsing data...")
    ddragon_basic = parse_ddragon_basic_json(full_patch)
    champions_lua = parse_champions_lua()
    aram_changes = parse_aram_modifiers()

    print("Merging...")
    merge_champion_data(
        ddragon_basic,
        champions_lua,
        aram_changes,
        patch,
    )

    if is_new_patch:
        stats = load_champions_for_patch(patch)
        print("Champion DB load:", stats)
    else:
        print("Patch already loaded in DB")

    return patch
