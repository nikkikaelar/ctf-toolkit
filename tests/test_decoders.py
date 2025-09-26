from ctf.analyzers.decoders import decode_any
def test_hex_b64_rot13():
    assert any(d["method"]=="hex" for d in decode_any("68656c6c6f"))
    assert any(d["method"]=="base64" for d in decode_any("aGVsbG8="))
    assert any(d["method"]=="rot13" for d in decode_any("uryyb"))
