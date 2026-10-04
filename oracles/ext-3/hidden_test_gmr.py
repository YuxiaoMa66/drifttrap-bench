from shop.clients.shipping import retry_delays
got = list(retry_delays())
assert got == [2, 4, 8, 16, 32], repr(got)
