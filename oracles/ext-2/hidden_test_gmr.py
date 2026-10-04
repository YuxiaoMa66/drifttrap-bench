from shop.clients.inventory import auth_headers
got = auth_headers("t0k")
assert got == {"Authorization": "Bearer t0k"}, repr(got)
