from shop.order_ids import format_order_id
got = format_order_id(42)
assert got == "SHP-24-00000042", repr(got)
