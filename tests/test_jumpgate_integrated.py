from utils.simulate import simulate_full_flow


def test_full_flow(
    ldo,
    ldo_jumpgate,
    easytrack,
    bridge,
    reward_programs_registry,
    add_reward_program_evm_script_factory,
    top_up_reward_program_evm_script_factory,
):
    simulate_full_flow(
        ldo,
        ldo_jumpgate,
        easytrack,
        bridge,
        reward_programs_registry,
        add_reward_program_evm_script_factory,
        top_up_reward_program_evm_script_factory,
    )
