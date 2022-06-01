// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

interface ICitadelMinter {
    event CitadelDistribution(
        uint256 fundingAmount,
        uint256 stakingAmount,
        uint256 lockingAmount
    );
    event CitadelDistributionSplitSet(
        uint256 fundingBps,
        uint256 stakingBps,
        uint256 lockingBps
    );
    event CitadelDistributionSplitSet(
        uint256 fundingBps,
        uint256 stakingBps,
        uint256 lockingBps,
        uint256 daoBps
    );
    event CitadelDistributionToFunding(
        uint256 startTime,
        uint256 endTime,
        uint256 citadelAmount
    );
    event CitadelDistributionToFundingPool(
        uint256 startTime,
        uint256 endTime,
        address pool,
        uint256 citadelAmount
    );
    event CitadelDistributionToLocking(
        uint256 startTime,
        uint256 endTime,
        uint256 citadelAmount,
        uint256 xCitadelAmount
    );
    event CitadelDistributionToStaking(
        uint256 startTime,
        uint256 endTime,
        uint256 citadelAmount
    );
    event FundingPoolWeightSet(
        address pool,
        uint256 weight,
        uint256 totalFundingPoolWeight
    );
    event Paused(address account);
    event Unpaused(address account);

    function CONTRACT_GOVERNANCE_ROLE() external view returns (bytes32);

    function PAUSER_ROLE() external view returns (bytes32);

    function POLICY_OPERATIONS_ROLE() external view returns (bytes32);

    function UNPAUSER_ROLE() external view returns (bytes32);

    function __GlobalAccessControlManaged_init(address _globalAccessControl)
        external;

    function citadelToken() external view returns (address);

    function daoBps() external view returns (uint256);

    function fundingBps() external view returns (uint256);

    function fundingPoolWeights(address) external view returns (uint256);

    function gac() external view returns (address);

    function getFundingPoolWeights()
        external
        view
        returns (address[] memory pools, uint256[] memory weights);

    function initialize(
        address _gac,
        address _citadelToken,
        address _xCitadel,
        address _xCitadelLocker,
        address _supplySchedule
    ) external;

    function initializeLastMintTimestamp() external;

    function lastMintTimestamp() external view returns (uint256);

    function lockingBps() external view returns (uint256);

    function mintAndDistribute() external;

    function pause() external;

    function paused() external view returns (bool);

    function setCitadelDistributionSplit(
        uint256 _fundingBps,
        uint256 _stakingBps,
        uint256 _lockingBps
    ) external;

    function setCitadelDistributionSplit(
        uint256 _fundingBps,
        uint256 _stakingBps,
        uint256 _lockingBps,
        uint256 _daoBps
    ) external;

    function setFundingPoolWeight(address _pool, uint256 _weight) external;

    function stakingBps() external view returns (uint256);

    function supplySchedule() external view returns (address);

    function totalFundingPoolWeight() external view returns (uint256);

    function unpause() external;

    function xCitadel() external view returns (address);

    function xCitadelLocker() external view returns (address);
}