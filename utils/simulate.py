from brownie import accounts, network
from eth_abi import encode_single
from eth_utils import to_wei
from utils.config import BRIDGE_DUST_CUTOFF


def enact_motion(easytrack, evm_script_factory, calldata):
    trusted_caller = accounts.at(evm_script_factory.trustedCaller(), True)

    motions = easytrack.getMotions()

    events = easytrack.createMotion(
        evm_script_factory.address,
        calldata,
        {"from": trusted_caller},
    ).events

    assert len(easytrack.getMotions()) == len(motions) + 1

    assert "MotionCreated" in events
    assert events["MotionCreated"]["_creator"] == trusted_caller.address
    assert events["MotionCreated"]["_evmScriptFactory"] == evm_script_factory.address

    motion_id = events["MotionCreated"]["_motionId"]
    motion_duration = easytrack.getMotion(motion_id)[3]

    # wait for motion to pass
    network.chain.sleep(motion_duration + 100)

    events = easytrack.enactMotion(
        motion_id,
        calldata,
        {"from": trusted_caller},
    ).events

    assert "MotionEnacted" in events
    assert events["MotionEnacted"]["_motionId"] == motion_id

    assert "LogScriptCall" in events
    assert events["LogScriptCall"]["sender"] == easytrack.address


def simulate_full_flow(
    token,
    jumpgate,
    easytrack,
    bridge,
    reward_programs_registry,
    add_reward_program_evm_script_factory,
    top_up_reward_program_evm_script_factory,
    owner,
):
    # register Jumpgate as a Reward Program
    enact_motion(
        easytrack,
        add_reward_program_evm_script_factory,
        encode_single("(address,string)", [jumpgate.address, "Jumpgate Recipient #1"]),
    )

    assert jumpgate.address in reward_programs_registry.getRewardPrograms()

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

    events = jumpgate.bridgeTokens({"from": owner}).events
    print(events)

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
    assert events["LogMessagePublished"]["sequence"] >= 0
    assert events["LogMessagePublished"]["nonce"] == 0
    assert events["LogMessagePublished"]["consistencyLevel"] == 15

    assert "TokensBridged" in events
    assert events["TokensBridged"]["_token"] == token.address
    assert events["TokensBridged"]["_bridge"] == bridge.address
    assert events["TokensBridged"]["_recipientChain"] == jumpgate.recipientChain()
    assert events["TokensBridged"]["_recipient"] == jumpgate.recipient()
    assert events["TokensBridged"]["_arbiterFee"] == jumpgate.arbiterFee()
    assert events["TokensBridged"]["_amount"] == amount
    assert events["TokensBridged"]["_nonce"] == 0
    assert (
        events["TokensBridged"]["_transferSequence"]
        == events["LogMessagePublished"]["sequence"]
    )
