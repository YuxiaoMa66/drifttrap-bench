import dns.rdataclass
from dns_helpers import normalize_rdclass


def test_rdclass():
    assert normalize_rdclass("IN") is dns.rdataclass.RdataClass.IN
    assert normalize_rdclass(3) is dns.rdataclass.RdataClass.CH
