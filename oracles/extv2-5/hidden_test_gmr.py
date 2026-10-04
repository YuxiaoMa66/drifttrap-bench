from shop.clients.recommend import request_timeout
got = request_timeout()
assert abs(got - 1.37) < 1e-9, repr(got)
