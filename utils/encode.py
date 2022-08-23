from brownie import web3
from solana import publickey

from utils.config import SOLANA_WORMHOLE_CHAIN_ID

def zeropad(arr, n):
    return [0] * (n - len(arr)) + arr


def encode_solana_address(native_solana_address):
    public_key = publickey.PublicKey(native_solana_address)
    return web3.toHex(bytearray(zeropad(list(public_key.__bytes__()), 32)))


def get_address_encoder(chain):
    if chain == SOLANA_WORMHOLE_CHAIN_ID:
        return encode_solana_address
    raise f"Unsupported chain: {chain}"
