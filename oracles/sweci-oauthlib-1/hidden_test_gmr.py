from oauth_helpers import from_wsgi


def test_from_wsgi():
    r = from_wsgi(b"https://a.test/p?x=1", b"POST", b"a=1", {b"Content-Type": b"application/x-www-form-urlencoded"})
    assert (r.uri, r.http_method, r.body) == ("https://a.test/p?x=1", "POST", "a=1")
    assert all(isinstance(k, str) and isinstance(v, str) for k, v in r.headers.items())
