import dns.rdatatype
from dns_helpers import normalize_rdtype


def test_rdtype():
    assert normalize_rdtype("MX") is dns.rdatatype.RdataType.MX
    assert normalize_rdtype(15) is dns.rdatatype.RdataType.MX
