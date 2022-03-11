from brownie import network


def is_development():
    return network.show_active() == "mainnet-fork"
