from brownie import network


def is_development() -> bool:
    dev_networks = [
        "development",
        "hardhat",
        "hardhat-fork",
        "mainnet-fork",
        "goerli-fork",
    ]
    return network.show_active() in dev_networks
