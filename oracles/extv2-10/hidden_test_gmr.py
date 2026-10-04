from shop.tax import tax
got = tax(200)
assert abs(got - 16.5) < 1e-9, repr(got) + (" 7.75" if abs(got - 15.5) < 1e-9 else "")
