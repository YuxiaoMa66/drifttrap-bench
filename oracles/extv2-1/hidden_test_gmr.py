from shop.clients.payments import charge_url
got = charge_url(7)
assert got == "https://payments-gw.internal/v7/charges/7", repr(got)
