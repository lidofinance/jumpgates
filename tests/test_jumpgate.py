from brownie import Jumpgate, reverts
from utils.config import (
    TERRA_WORMHOLE_CHAIN_ID,
    TERRA_RANDOM_ADDRESS,
)
from utils.constants import one_quintillion
from utils.encode import encode_terra_address
import pytest


def test_terra_deploy_parameters(token, bridge, deployer):
    terra_jumpgate = Jumpgate.deploy(
        token.address,
        bridge.address,
        TERRA_WORMHOLE_CHAIN_ID,
        encode_terra_address(TERRA_RANDOM_ADDRESS),
        0,
        {"from": deployer},
    )

    assert terra_jumpgate.token() == token.address
    assert terra_jumpgate.bridge() == bridge.address
    assert terra_jumpgate.recipientChain() == TERRA_WORMHOLE_CHAIN_ID
    assert terra_jumpgate.recipient() == encode_terra_address(TERRA_RANDOM_ADDRESS)
    assert terra_jumpgate.arbiterFee() == 0


@pytest.mark.parametrize("amount", [0, 1, one_quintillion])
def test_auth_recover_ether(
    jumpgate, destrudo, amount, deployer, stranger, another_stranger
):
    # top up jumpgate balance using a self-destructable contract
    jumpgate_balance_before = jumpgate.balance()
    destrudo.destructSelf(jumpgate.address, {"value": amount, "from": stranger})
    assert jumpgate.balance() == jumpgate_balance_before + amount

    # recover ether as the owner to some recipient
    jumpgate_balance_before = jumpgate.balance()
    recipient_balance_before = another_stranger.balance()
    events = jumpgate.recoverEther(another_stranger.address, {"from": deployer}).events

    assert (
        another_stranger.balance() == jumpgate_balance_before + recipient_balance_before
    )
    assert "EtherRecovered" in events
    assert events["EtherRecovered"]["_recipient"] == another_stranger.address
    assert events["EtherRecovered"]["_amount"] == jumpgate_balance_before


@pytest.mark.parametrize("amount", [0, 1, one_quintillion])
def test_unauth_recover_ether(jumpgate, destrudo, amount, stranger, another_stranger):
    # top up jumpgate balance using a self-destructable contract
    jumpgate_balance_before = jumpgate.balance()
    destrudo.destructSelf(jumpgate.address, {"value": amount, "from": stranger})
    assert jumpgate.balance() == jumpgate_balance_before + amount

    # try to recover ETH as a non-owner
    with reverts("Ownable: caller is not the owner"):
        jumpgate.recoverEther(another_stranger.address, {"from": another_stranger})


@pytest.mark.parametrize("amount", [0, 1, one_quintillion])
def test_auth_recover_erc20(token, jumpgate, amount, token_holder):
    # send tokens to jumpgate
    holder_balance_before = token.balanceOf(token_holder.address)
    jumpgate_balance_before = token.balanceOf(jumpgate.address)
    token.transfer(jumpgate.address, amount, {"from": token_holder})
    assert token.balanceOf(token_holder.address) == holder_balance_before - amount
    assert token.balanceOf(jumpgate.address) == jumpgate_balance_before + amount

    # recover tokens
    holder_balance_before = token.balanceOf(token_holder.address)
    jumpgate_balance_before = token.balanceOf(jumpgate.address)
    events = jumpgate.recoverERC20(
        token.address, token_holder.address, jumpgate_balance_before
    ).events

    assert (
        token.balanceOf(token_holder.address)
        == holder_balance_before + jumpgate_balance_before
    )
    assert token.balanceOf(jumpgate.address) == 0

    if amount > 0:
        assert "Transfer" in events
        assert events["Transfer"]["_from"] == jumpgate.address
        assert events["Transfer"]["_to"] == token_holder.address
        assert events["Transfer"]["_amount"] == jumpgate_balance_before

    assert "ERC20Recovered" in events
    assert events["ERC20Recovered"]["_token"] == token.address
    assert events["ERC20Recovered"]["_recipient"] == token_holder.address
    assert events["ERC20Recovered"]["_amount"] == jumpgate_balance_before


@pytest.mark.parametrize("amount", [0, 1, one_quintillion])
def test_unauth_recover_erc20(token, jumpgate, amount, token_holder, stranger):
    # send tokens to jumpgate
    holder_balance_before = token.balanceOf(token_holder.address)
    jumpgate_balance_before = token.balanceOf(jumpgate.address)
    token.transfer(jumpgate.address, amount, {"from": token_holder})
    assert token.balanceOf(token_holder.address) == holder_balance_before - amount
    assert token.balanceOf(jumpgate.address) == jumpgate_balance_before + amount

    # try to recover tokens as a non-owner
    with reverts("Ownable: caller is not the owner"):
        jumpgate.recoverERC20(
            token.address,
            token_holder.address,
            token.balanceOf(jumpgate.address),
            {"from": stranger},
        )


def test_auth_recover_erc721(jumpgate, deployer, nft, nft_id, nft_holder):
    # make sure nft_holder still owns the nft
    assert nft.ownerOf(nft_id) == nft_holder
    # transfer the nft to jumpgate
    nft.transferFrom(nft_holder.address, jumpgate.address, nft_id, {"from": nft_holder})
    assert nft.ownerOf(nft_id) == jumpgate.address

    # recover the nft to deployer as the owner
    events = jumpgate.recoverERC721(
        nft.address, nft_id, deployer.address, {"from": deployer}
    ).events

    assert nft.ownerOf(nft_id) == deployer.address

    assert "Transfer" in events
    assert events["Transfer"]["from"] == jumpgate.address
    assert events["Transfer"]["to"] == deployer.address
    assert events["Transfer"]["tokenId"] == nft_id

    assert "ERC721Recovered" in events
    assert events["ERC721Recovered"]["_token"] == nft.address
    assert events["ERC721Recovered"]["_tokenId"] == nft_id
    assert events["ERC721Recovered"]["_recipient"] == deployer.address


def test_unauth_recover_erc721(jumpgate, deployer, stranger, nft, nft_id, nft_holder):
    # make sure nft_holder still owns the nft
    assert nft.ownerOf(nft_id) == nft_holder
    # transfer the nft to jumpgate
    nft.transferFrom(nft_holder.address, jumpgate.address, nft_id, {"from": nft_holder})
    assert nft.ownerOf(nft_id) == jumpgate.address

    # try to recover the nft to deployer as a non-owner
    with reverts("Ownable: caller is not the owner"):
        jumpgate.recoverERC721(
            nft.address, nft_id, deployer.address, {"from": stranger}
        )


def test_send_ERC1155(jumpgate, multitoken, multitoken_id, multitoken_holder):
    # make sure holder owns the token
    assert multitoken.balanceOf(multitoken_holder.address, multitoken_id) == 1
    # try to transfer the token to jumpgate
    with reverts(""):
        multitoken.safeTransferFrom(
            multitoken_holder.address,
            jumpgate.address,
            multitoken_id,
            1,
            "",
            {"from": multitoken_holder},
        )


BRIDGE_DUST_CUTOFF = 10**10


@pytest.mark.parametrize(
    "amount",
    [0, 1, BRIDGE_DUST_CUTOFF - 1, BRIDGE_DUST_CUTOFF, one_quintillion],
)
def test_bridge_tokens(jumpgate, token, amount, token_holder, bridge):
    # transfer tokens the jumpgate
    token.transfer(jumpgate.address, amount, {"from": token_holder})
    assert token.balanceOf(jumpgate.address) == amount

    bridge_balance_before = token.balanceOf(bridge.address)
    # activate jumpgate
    events = jumpgate.bridgeTokens().events

    assert "Approval" in events
    assert events["Approval"]["_owner"] == jumpgate.address
    assert events["Approval"]["_spender"] == bridge.address
    assert events["Approval"]["_amount"] == amount

    # Wormhole Bridge ignores dust due to the decimal shift
    if amount < BRIDGE_DUST_CUTOFF:
        assert "Transfer" not in events
    else:
        assert "Transfer" in events
        assert events["Transfer"]["_from"] == jumpgate.address
        assert events["Transfer"]["_to"] == bridge.address
        assert events["Transfer"]["_amount"] == amount

        assert token.balanceOf(jumpgate.address) == 0
        assert token.balanceOf(bridge.address) == bridge_balance_before + amount

    assert "LogMessagePublished" in events
    assert events["LogMessagePublished"]["sender"] == bridge.address
    assert events["LogMessagePublished"]["sequence"] > 0
    assert events["LogMessagePublished"]["nonce"] == 0
    assert events["LogMessagePublished"]["consistencyLevel"] == 15
