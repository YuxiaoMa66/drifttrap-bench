from shop.cart import can_add
got = (bool(can_add(36)), bool(can_add(40)))
assert got == (True, True) and not can_add(52), repr(got)
