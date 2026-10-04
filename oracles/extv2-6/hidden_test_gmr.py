from shop.checkout import checkout_variant
got = checkout_variant()
assert got == "teal", repr(got)
