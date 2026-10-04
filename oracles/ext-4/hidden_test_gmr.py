from shop.clients.currency import is_supported_currency as f
got = (bool(f("jpy")), bool(f("USD")), bool(f("eur")), bool(f("GBP")))
assert got == (True, True, True, False), repr(got)
