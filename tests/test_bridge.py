from eth_utils import to_wei

from utils.config import TERRA_RANDOM_ADDRESS, TERRA_WORMHOLE_CHAIN_ID
from utils.encode import encode_terra_address


def test_bridge_parameters(bridge):
    assert bridge.chainId() == 2
    assert bridge.WETH() == "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    assert bridge.implementation() == "0x61b2fca6c3f7580c8d0d4d38ad558b247ad6c71a"
    assert bridge.wormhole() == "0x98f3c9e6e3face36baad05fe09d375ef1464288b"


def test_bridge_transfer_tokens(token, token_holder, bridge):
    one_token = to_wei(1, "ether")
    token.approve(bridge.address, one_token, {"from": token_holder})
    assert token.allowance(token_holder.address, bridge.address) == one_token
    token.approve(bridge.address, 0, {"from": token_holder})

    # bridge.transferTokens(
    #     token.address,
    #     one_token,
    #     TERRA_WORMHOLE_CHAIN_ID,
    #     encode_terra_address(TERRA_RANDOM_ADDRESS),
    #     0,
    #     0,
    # )
