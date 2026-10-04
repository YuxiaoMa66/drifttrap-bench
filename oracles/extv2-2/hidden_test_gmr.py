from shop.clients.inventory import auth_headers
got = auth_headers("t0k")
assert got == {"X-Inventory-Token": "Tok t0k"}, repr(got)
