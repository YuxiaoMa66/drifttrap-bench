from store_helpers import safe_id_filename


def test_safe_id_filename():
    assert safe_id_filename("../../etc/passwd") == "etc_passwd"
    assert safe_id_filename("my doc id") == "my_doc_id"
    assert safe_id_filename("\u00dcn\u00efcode.json") == "Unicode.json"
