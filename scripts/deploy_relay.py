from brownie import Relay, MockERC20, network, accounts
from utils.secrets import get_private_key
from utils.config import (
    TERRA_WORMHOLE_CHAIN_ID,
    TERRA_RANDOM_ADDRESS,
    wormhole_token_bridge,
)
from utils.encode import encode_terra_address


def main():
    print(f"Network {network.chain.id}")
    development = "fork" in network.show_active()
    private_key = get_private_key()
    account = accounts.add(private_key)
    # account = accounts[0]
    print(f"My address: {account.address}")

    print(f"Deploying MockERC20...")
    mock_erc20 = MockERC20.deploy(
        10**9, {"from": account}, publish_source=not development
    )

    print("Deploying Relay contract...")
    relay = Relay.deploy(
        mock_erc20.address,
        wormhole_token_bridge.get(network.chain.id),
        TERRA_WORMHOLE_CHAIN_ID,
        encode_terra_address(TERRA_RANDOM_ADDRESS),
        0,
        {"from": account},
        publish_source=not development,
    )
