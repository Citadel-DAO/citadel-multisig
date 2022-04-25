# citadel-multisig

This repo is where all EVM multisig operations take place for the CitadelDAO

It relies heavily on [`ganache-cli`](https://docs.nethereum.com/en/latest/ethereum-and-clients/ganache-cli/), [`eth-brownie`](https://github.com/eth-brownie/brownie), [`gnosis-py`](https://github.com/gnosis/gnosis-py) and a custom developed evolution of [`ape-safe`](https://github.com/banteg/ape-safe); [`great-ape-safe`](https://github.com/gosuto-ai/great-ape-safe).


# Multisig Adresses

| Label | Description | Address (Links) |
|-|-|-|
|`governance`| Governance/admin rights; set parameters, queue/execute timelock txs, etc.|Mainnet: `0xa95ecbDc51082ED2a2D078a5dE5275777dD73347` ([Etherscan](https://etherscan.io/address/0xa95ecbDc51082ED2a2D078a5dE5275777dD73347), [Gnosis Safe](https://gnosis-safe.io/app/eth:0xa95ecbDc51082ED2a2D078a5dE5275777dD73347/), [Zapper](https://zapper.fi/account/0xa95ecbDc51082ED2a2D078a5dE5275777dD73347))|
|`Treasury Vault`|Treasury long-term holdings; bitcoin, ether (gas), farming.|Mainnet: `0x38724146C8dc1Aa49c3395091cf86B789c37F52c` ([Etherscan](https://etherscan.io/address/0x38724146C8dc1Aa49c3395091cf86B789c37F52c), [Gnosis Safe](https://gnosis-safe.io/app/eth:0x38724146C8dc1Aa49c3395091cf86B789c37F52c/), [Zapper](https://zapper.fi/account/0x38724146C8dc1Aa49c3395091cf86B789c37F52c))|
|`Policy Ops`| Policy Ops for Citadel Contracts|Mainnet: `0x7426e8987f8d388e731Dec452D8B0a1710d8E416` ([Etherscan](https://etherscan.io/address/0x7426e8987f8d388e731Dec452D8B0a1710d8E416), [Gnosis Safe](https://gnosis-safe.io/app/eth:0x7426e8987f8d388e731Dec452D8B0a1710d8E416/), [Zapper](https://zapper.fi/account/0x7426e8987f8d388e731Dec452D8B0a1710d8E416))|
