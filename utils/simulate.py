from ast import AnnAssign
from brownie import accounts, network


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
