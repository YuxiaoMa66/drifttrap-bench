from unittest import mock
from oauthlib.common import Request
from oauth_helpers import issue_token


def test_issue_token():
    req = Request("https://a.test/token")
    req.scopes = ["read"]
    req.state = None
    v = mock.Mock()
    tok = issue_token(v, req)
    assert tok["token_type"] == "Bearer" and tok["access_token"] and tok["refresh_token"]
    v.save_bearer_token.assert_called_once_with(req, tok)
