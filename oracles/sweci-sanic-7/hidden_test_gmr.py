from sanic.response import text
from cookie_helpers import cookie_header_bytes


def test_cookie_header_bytes():
    r = text("ok")
    c = r.add_cookie("a", "1", max_age=5)
    got = cookie_header_bytes(c)
    assert isinstance(got, bytes) and got.startswith(b"a=1") and b"Max-Age=5" in got
