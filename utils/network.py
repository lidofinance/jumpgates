from brownie import network


def is_dev():
    return not network.show_active() in ["ropsten", "goerli", "mainnet"]
