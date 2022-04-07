from brownie import Jumpgate, reverts
from utils.config import BRIDGE_DUST_CUTOFF
from utils.constants import one_quintillion
from utils.encode import get_address_encoder
import pytest


def test_deploy_parameters(token, bridge, owner, deploy_params):
    (recipientChain, recipient) = deploy_params

    encode = get_address_encoder(recipientChain)
    recipient_encoded = encode(recipient)
    arbiter_fee = 0

    jumpgate = Jumpgate.deploy(
        token.address,
        bridge.address,
        recipientChain,
        recipient_encoded,
        arbiter_fee,
        {"from": owner},
    )

    assert jumpgate.token() == token.address
    assert jumpgate.bridge() == bridge.address
    assert jumpgate.recipientChain() == recipientChain
    assert jumpgate.recipient() == recipient_encoded
    assert jumpgate.arbiterFee() == arbiter_fee

    assert "JumpgateCreated" in jumpgate.tx.events
    assert jumpgate.tx.events["JumpgateCreated"]["_token"] == token.address
    assert jumpgate.tx.events["JumpgateCreated"]["_bridge"] == bridge.address
    assert jumpgate.tx.events["JumpgateCreated"]["_recipientChain"] == recipientChain
    assert jumpgate.tx.events["JumpgateCreated"]["_recipient"] == recipient_encoded
    assert jumpgate.tx.events["JumpgateCreated"]["_arbiterFee"] == arbiter_fee


@pytest.mark.parametrize("amount", [0, 1, one_quintillion])
def test_recover_ether(
    jumpgate,
    destrudo,
    amount,
    sender,
    stranger,
):
    # top up jumpgate balance using a self-destructable contract
    jumpgate_balance_before = jumpgate.balance()
    destrudo.destructSelf(jumpgate.address, {"value": amount, "from": sender})
    assert jumpgate.balance() == jumpgate_balance_before + amount

    jumpgate_balance_before = jumpgate.balance()
    # recovering to stranger to avoid gas calculations
    recipient = stranger
    recipient_balance_before = recipient.balance()

    is_owner = jumpgate.owner() == sender.address
    # recover as the owner
    if is_owner:
        tx = jumpgate.recoverEther(recipient.address, {"from": sender})

        assert recipient.balance() == jumpgate_balance_before + recipient_balance_before
        assert "EtherRecovered" in tx.events
        assert tx.events["EtherRecovered"]["_recipient"] == recipient.address
        assert tx.events["EtherRecovered"]["_amount"] == jumpgate_balance_before
    # attempt to recover as a non-owner
    else:
        with reverts("Ownable: caller is not the owner"):
            jumpgate.recoverEther(recipient.address, {"from": sender})


@pytest.mark.parametrize("amount", [0, 1, one_quintillion])
def test_recover_erc20(token, jumpgate, sender, token_holder, amount):
    # send tokens to jumpgate
    holder_balance_before = token.balanceOf(token_holder.address)
    jumpgate_balance_before = token.balanceOf(jumpgate.address)
    token.transfer(jumpgate.address, amount, {"from": token_holder})
    assert token.balanceOf(token_holder.address) == holder_balance_before - amount
    assert token.balanceOf(jumpgate.address) == jumpgate_balance_before + amount

    # recover tokens
    holder_balance_before = token.balanceOf(token_holder.address)
    jumpgate_balance_before = token.balanceOf(jumpgate.address)

    is_owner = jumpgate.owner() == sender.address
    # recover as the owner
    if is_owner:
        tx = jumpgate.recoverERC20(
            token.address,
            token_holder.address,
            jumpgate_balance_before,
            {"from": sender},
        )

        assert (
            token.balanceOf(token_holder.address)
            == holder_balance_before + jumpgate_balance_before
        )
        assert token.balanceOf(jumpgate.address) == 0

        if amount > 0:
            assert "Transfer" in tx.events
            assert tx.events["Transfer"]["_from"] == jumpgate.address
            assert tx.events["Transfer"]["_to"] == token_holder.address
            assert tx.events["Transfer"]["_amount"] == jumpgate_balance_before

        assert "ERC20Recovered" in tx.events
        assert tx.events["ERC20Recovered"]["_token"] == token.address
        assert tx.events["ERC20Recovered"]["_recipient"] == token_holder.address
        assert tx.events["ERC20Recovered"]["_amount"] == jumpgate_balance_before
    # attempt to recover tokens as a non-owner
    else:
        with reverts("Ownable: caller is not the owner"):
            jumpgate.recoverERC20(
                token.address,
                token_holder.address,
                token.balanceOf(jumpgate.address),
                {"from": sender},
            )


def test_recover_erc721(jumpgate, sender, nft, nft_id, nft_holder):
    # make sure nft_holder still owns the nft
    assert nft.ownerOf(nft_id) == nft_holder
    # transfer the nft to jumpgate
    nft.transferFrom(nft_holder.address, jumpgate.address, nft_id, {"from": nft_holder})
    assert nft.ownerOf(nft_id) == jumpgate.address

    is_owner = jumpgate.owner() == sender.address

    # recover the nft to deployer as the owner
    if is_owner:
        tx = jumpgate.recoverERC721(
            nft.address, nft_id, sender.address, {"from": sender}
        )

        assert nft.ownerOf(nft_id) == sender.address

        assert "Transfer" in tx.events
        assert tx.events["Transfer"]["from"] == jumpgate.address
        assert tx.events["Transfer"]["to"] == sender.address
        assert tx.events["Transfer"]["tokenId"] == nft_id

        assert "ERC721Recovered" in tx.events
        assert tx.events["ERC721Recovered"]["_token"] == nft.address
        assert tx.events["ERC721Recovered"]["_tokenId"] == nft_id
        assert tx.events["ERC721Recovered"]["_recipient"] == sender.address
    # attempt to recover as a non-owner
    else:
        with reverts("Ownable: caller is not the owner"):
            jumpgate.recoverERC721(
                nft.address, nft_id, sender.address, {"from": sender}
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
    tx = jumpgate.bridgeTokens()

    assert "Approval" in tx.events
    assert tx.events["Approval"]["_owner"] == jumpgate.address
    assert tx.events["Approval"]["_spender"] == bridge.address
    assert tx.events["Approval"]["_amount"] == amount

    # Wormhole Bridge ignores dust due to the decimal shift
    if amount < BRIDGE_DUST_CUTOFF:
        assert "Transfer" not in tx.events
    else:
        assert "Transfer" in tx.events
        assert tx.events["Transfer"]["_from"] == jumpgate.address
        assert tx.events["Transfer"]["_to"] == bridge.address
        assert tx.events["Transfer"]["_amount"] == amount

        assert token.balanceOf(jumpgate.address) == 0
        assert token.balanceOf(bridge.address) == bridge_balance_before + amount

    assert "LogMessagePublished" in tx.events
    assert tx.events["LogMessagePublished"]["sender"] == bridge.address
    assert tx.events["LogMessagePublished"]["sequence"] >= 0
    assert tx.events["LogMessagePublished"]["nonce"] == 0
    assert tx.events["LogMessagePublished"]["consistencyLevel"] == 15

    assert "TokensBridged" in tx.events
    assert tx.events["TokensBridged"]["_token"] == token.address
    assert tx.events["TokensBridged"]["_bridge"] == bridge.address
    assert tx.events["TokensBridged"]["_recipientChain"] == jumpgate.recipientChain()
    assert tx.events["TokensBridged"]["_recipient"] == jumpgate.recipient()
    assert tx.events["TokensBridged"]["_arbiterFee"] == jumpgate.arbiterFee()
    assert tx.events["TokensBridged"]["_amount"] == amount
    assert tx.events["TokensBridged"]["_nonce"] == 0
    assert (
        tx.events["TokensBridged"]["_transferSequence"]
        == tx.events["LogMessagePublished"]["sequence"]
    )
