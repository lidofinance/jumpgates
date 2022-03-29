from brownie import Jumpgate, reverts, web3
from eth_utils import to_wei
from utils.config import (
    TERRA_WORMHOLE_CHAIN_ID,
    TERRA_RANDOM_ADDRESS,
)
from utils.constants import one_quintillion
from utils.encode import encode_terra_address
import pytest


@pytest.fixture(scope="function")
def jumpgate(deployer, token, bridge):
    return Jumpgate.deploy(
        token.address,
        bridge.address,
        TERRA_WORMHOLE_CHAIN_ID,
        encode_terra_address(TERRA_RANDOM_ADDRESS),
        0,
        {"from": deployer},
    )


def test_deploy_parameters(jumpgate, token, bridge):
    assert jumpgate.token() == token.address
    assert jumpgate.bridge() == bridge.address
    assert jumpgate.recipientChain() == TERRA_WORMHOLE_CHAIN_ID
    assert jumpgate.recipient() == encode_terra_address(TERRA_RANDOM_ADDRESS)
    assert jumpgate.arbiterFee() == 0


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
    jumpgate.recoverEther(another_stranger.address, {"from": deployer})
    assert (
        another_stranger.balance() == jumpgate_balance_before + recipient_balance_before
    )


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
    jumpgate.recoverERC20(token.address, token_holder.address)
    assert (
        token.balanceOf(token_holder.address)
        == holder_balance_before + jumpgate_balance_before
    )
    assert token.balanceOf(jumpgate.address) == 0


@pytest.mark.parametrize("amount", [0, 1, one_quintillion])
def test_unauth_recover_ether(jumpgate, destrudo, amount, stranger, another_stranger):
    # top up jumpgate balance using a self-destructable contract
    jumpgate_balance_before = jumpgate.balance()
    destrudo.destructSelf(jumpgate.address, {"value": amount, "from": stranger})
    assert jumpgate.balance() == jumpgate_balance_before + amount

    # try to recover ETH as a non-owner
    with reverts("Ownable: caller is not the owner"):
        jumpgate.recoverEther(another_stranger.address, {"from": another_stranger})


def test_auth_recover_erc721(jumpgate, deployer, nft, nft_id, nft_holder):
    # make sure nft_holder still owns the nft
    assert nft.ownerOf(nft_id) == nft_holder
    # transfer the nft to jumpgate
    nft.transferFrom(nft_holder.address, jumpgate.address, nft_id, {"from": nft_holder})
    assert nft.ownerOf(nft_id) == jumpgate.address

    # recover the nft to deployer as the owner
    jumpgate.recoverERC721(nft.address, nft_id, deployer.address, {"from": deployer})
    assert nft.ownerOf(nft_id) == deployer.address


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
