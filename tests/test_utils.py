from utils.encode import encode_terra_address


def test_encode_terra_address():
    terra_address = "terra12hwmnfl79vp6xf765s0vuztpxz4mdy8w0z72pp"
    encoded = encode_terra_address(terra_address)
    assert (
        encoded == "0x00000000000000000000000055ddb9a7fe2b03a327daa41ece096130abb690ee"
    )
