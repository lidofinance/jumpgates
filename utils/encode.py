from typing import List, Tuple
import bech32
from brownie import web3


def zeropad(arr, n):
    return [0] * (n - len(arr)) + arr


def encode_terra_address(native_terra_address):
    decoded_address: Tuple[str, List[int]] = bech32.bech32_decode(native_terra_address)
    return web3.toHex(
        bytearray(zeropad(bech32.convertbits(decoded_address[1], 5, 8, False), 32))
    )
