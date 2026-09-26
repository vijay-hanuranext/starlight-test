from pathlib import Path


def test_create_new_folder():
    storage_path = Path(".auth/state.json")
    storage_path.parent.mkdir(exist_ok=True)
