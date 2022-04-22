from utils.simulate import simulate_full_flow


def test_full_flow(
    ldo,
    ldo_jumpgate,
    easytrack,
    bridge,
    reward_programs_registry,
    add_reward_program_evm_script_factory,
    top_up_reward_program_evm_script_factory,
    owner,
    bridge_cutoff_amount,
):
    simulate_full_flow(
        ldo,
        ldo_jumpgate,
        easytrack,
        bridge,
        reward_programs_registry,
        add_reward_program_evm_script_factory,
        top_up_reward_program_evm_script_factory,
        owner,
        bridge_cutoff_amount,
    )


def test_recover_erc20_with_nonstandard_decimals(
    tether, tether_holder, tether_amount, jumpgate, owner, stranger
):
    # tether is a not 18-decimal token
    assert tether.decimals() != 18

    # tether_holder owns enough tether
    assert tether.balanceOf(tether_holder.address) >= tether_amount

    # transfer tether to jumpgate
    jumpgate_balance_before = tether.balanceOf(jumpgate.address)
    tether.transfer(jumpgate.address, tether_amount, {"from": tether_holder})
    assert tether.balanceOf(jumpgate.address) == jumpgate_balance_before + tether_amount

    # recover tokens from jumpgate
    recipient = stranger
    recipient_balance_before = tether.balanceOf(recipient.address)
    jumpgate_balance_before = tether.balanceOf(jumpgate.address)

    tx = jumpgate.recoverERC20(tether.address, recipient.address, tether_amount)
    assert (
        tether.balanceOf(recipient.address) == recipient_balance_before + tether_amount,
        {"from": owner},
    )
    assert tether.balanceOf(jumpgate.address) == jumpgate_balance_before - tether_amount

    assert "ERC20Recovered" in tx.events
    assert tx.events["ERC20Recovered"]["_token"] == tether.address
    assert tx.events["ERC20Recovered"]["_recipient"] == recipient.address
    assert tx.events["ERC20Recovered"]["_amount"] == tether_amount
