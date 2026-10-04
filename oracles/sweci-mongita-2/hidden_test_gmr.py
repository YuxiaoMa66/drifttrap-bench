from mongita.engines.memory_engine import MemoryEngine
from store_helpers import stash_doc


def test_stash_doc():
    engine = MemoryEngine()
    stash_doc(engine, "shop", "orders", {"_id": "o1", "total": 5})
    assert engine.get_doc("shop.orders", "o1")["total"] == 5
