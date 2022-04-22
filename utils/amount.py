from utils.config import BRIDGE_DUST_CUTOFF_DECIMALS


def get_bridgeable_amount(amount, decimals):
    if decimals > BRIDGE_DUST_CUTOFF_DECIMALS:
        amount = amount // 10 ** (decimals - BRIDGE_DUST_CUTOFF_DECIMALS)
        amount = amount * 10 ** (decimals - BRIDGE_DUST_CUTOFF_DECIMALS)

    return amount
