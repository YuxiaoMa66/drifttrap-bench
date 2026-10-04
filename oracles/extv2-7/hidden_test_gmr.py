from shop.webhooks import signature_header
got = signature_header()
assert got == "X-Shop-Signature", repr(got)
