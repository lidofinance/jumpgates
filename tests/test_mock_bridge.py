import brownie as b
from eth_utils import to_wei
import pytest
from utils.account import get_account
from utils.config import (
    TERRA_RANDOM_ADDRESS,
    TERRA_WORMHOLE_CHAIN_ID,
)
from utils.encode import encode_terra_address
from utils.network import is_dev


def test_transfer_tokens():
    deployer = get_account()
    bridge = b.MockWormholeTokenBridge.deploy({"from": deployer})
    token = b.MockERC20Token.deploy(to_wei(10**9, "ether"), {"from": deployer})

    amount = to_wei(10**9, "ether")
    recipient = encode_terra_address(TERRA_RANDOM_ADDRESS)
    arbiter_fee = 0
    nonce = 0

    tx = bridge.transferTokens(
        token.address,
        amount,
        TERRA_WORMHOLE_CHAIN_ID,
        recipient,
        arbiter_fee,
        nonce,
        {"from": deployer},
    )
    tx.wait(1)

    events = b.network.event._decode_logs(tx.logs)

    assert "WormholeTransfer" in events
    assert events["WormholeTransfer"]["token"] == token.address
    assert events["WormholeTransfer"]["amount"] == amount
    assert events["WormholeTransfer"]["recipientChain"] == TERRA_WORMHOLE_CHAIN_ID
    assert events["WormholeTransfer"]["recipient"] == recipient
    assert events["WormholeTransfer"]["arbiterFee"] == arbiter_fee
    assert events["WormholeTransfer"]["nonce"] == nonce
    assert events["WormholeTransfer"]["value"] == 0
