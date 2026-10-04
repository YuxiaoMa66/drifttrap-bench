from shop.clients.currency import is_supported_currency as f
got = (bool(f("usd")), bool(f("CHF")), bool(f("sek")), bool(f("EUR")))
assert got == (True, True, True, False), repr(got)
