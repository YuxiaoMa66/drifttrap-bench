from sanic.response import text
from cookie_helpers import logout


def test_logout():
    r = text("ok")
    logout(r)
    c = r.cookies.get_cookie("session")
    assert c is not None and c.max_age == 0
