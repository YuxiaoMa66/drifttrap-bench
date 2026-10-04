from shop.clients.payments import charge_url
got = charge_url(7)
assert got == "https://payments.internal/v2/charges/7", repr(got)
