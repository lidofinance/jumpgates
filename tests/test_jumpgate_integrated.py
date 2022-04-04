from eth_abi import encode_single
from eth_utils import to_wei

from utils.config import BRIDGE_DUST_CUTOFF
from utils.simulate import enact_motion


def test_full_flow(
    token,
    jumpgate,
    easytrack,
    bridge,
    reward_program_registry,
    add_reward_program_evm_script_factory,
    top_up_reward_program_evm_script_factory,
):
    # register Jumpgate as a Reward Program
    enact_motion(
        easytrack,
        add_reward_program_evm_script_factory,
        encode_single("(address,string)", [jumpgate.address, "Jumpgate Recipient #1"]),
    )

    assert jumpgate.address in reward_program_registry.getRewardPrograms()

    # make sure reward programs use the same token as Jumpgate
    assert top_up_reward_program_evm_script_factory.rewardToken() == jumpgate.token()

    jumpgate_balance_before = token.balanceOf(jumpgate.address)
    amount = to_wei(1, "ether")

    # top up Jumpgate
    enact_motion(
        easytrack,
        top_up_reward_program_evm_script_factory,
        encode_single("(address[],uint256[])", [[jumpgate.address], [amount]]),
    )

    assert token.balanceOf(jumpgate.address) == jumpgate_balance_before + amount

    bridge_balance_before = token.balanceOf(bridge.address)

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
