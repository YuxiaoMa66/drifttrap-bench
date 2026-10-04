from shop.clients.shipping import retry_delays
got = list(retry_delays())
assert got == [5, 10, 20, 40, 80, 160], repr(got)
