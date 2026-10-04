from shop.checkout import checkout_version
got = checkout_version()
assert got == "v2", repr(got)
