from typing import List, Tuple
import bech32
from brownie import web3
from solana import publickey

from utils.config import TERRA_WORMHOLE_CHAIN_ID


def zeropad(arr, n):
    return [0] * (n - len(arr)) + arr


def encode_terra_address(native_terra_address):
    decoded_address: Tuple[str, List[int]] = bech32.bech32_decode(native_terra_address)
    return web3.toHex(
        bytearray(zeropad(bech32.convertbits(decoded_address[1], 5, 8, False), 32))
    )


def encode_solana_address(native_solana_address):
    public_key = publickey.PublicKey(native_solana_address)
    return web3.toHex(bytearray(zeropad(list(public_key.__bytes__()), 32)))


def get_address_encoder(chain):
    if chain == TERRA_WORMHOLE_CHAIN_ID:
        return encode_terra_address
    raise f"Unsupported chain: {chain}"
