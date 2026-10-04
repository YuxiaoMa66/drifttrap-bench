from shop.media import image_url
got = image_url("p/1.jpg")
assert got == "https://static-9c.internal/p/1.jpg", repr(got)
