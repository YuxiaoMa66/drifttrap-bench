from sanic.response import text
from cookie_helpers import cookie_value


def test_cookie_value():
    r = text("ok")
    r.add_cookie("theme", "dark")
    assert cookie_value(r, "theme") == "dark"
    assert cookie_value(r, "missing") is None
