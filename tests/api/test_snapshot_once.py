from utils.snapshot import take_snapshot

def test_take_snapshot(api):
    take_snapshot(api, "snapshot.db")
