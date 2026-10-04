from oauth_helpers import auth_header


def test_auth_header():
    h = auth_header(b"ck", b"cs", "https://a.test/r")
    assert isinstance(h, str) and h.startswith("OAuth ")
    assert 'oauth_consumer_key="ck"' in h and 'oauth_signature_method="HMAC-SHA1"' in h
