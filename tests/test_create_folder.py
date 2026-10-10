from pathlib import Path

STORAGE_STATE_PATH = Path(".auth/state.json")
def test_create_new_folder():
    # Test logic for creating a new folder
    
    STORAGE_STATE_PATH.parent.mkdir( exist_ok=True)
    assert STORAGE_STATE_PATH.parent.exists()