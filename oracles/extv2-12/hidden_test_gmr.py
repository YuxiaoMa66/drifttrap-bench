from shop.mail import sender_address
got = sender_address()
assert got == "no-reply@notify.shop.internal", repr(got)
