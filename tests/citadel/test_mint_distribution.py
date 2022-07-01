def test_mint_distribution(policy_ops):
    policy_ops.citadel.set_citadel_distribution_split(
        int(5000), int(2500), int(1000), int(1500)
    )
