// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

interface IGlobalAccessControl {
    event Paused(address account);
    event RoleAdminChanged(
        bytes32 indexed role,
        bytes32 indexed previousAdminRole,
        bytes32 indexed newAdminRole
    );
    event RoleGranted(
        bytes32 indexed role,
        address indexed account,
        address indexed sender
    );
    event RoleRevoked(
        bytes32 indexed role,
        address indexed account,
        address indexed sender
    );
    event Unpaused(address account);

    function BLOCKLISTED_ROLE() external view returns (bytes32);

    function BLOCKLIST_MANAGER_ROLE() external view returns (bytes32);

    function CITADEL_MINTER_ROLE() external view returns (bytes32);

    function CONTRACT_GOVERNANCE_ROLE() external view returns (bytes32);

    function DEFAULT_ADMIN_ROLE() external view returns (bytes32);

    function KEEPER_ROLE() external view returns (bytes32);

    function PAUSER_ROLE() external view returns (bytes32);

    function POLICY_OPERATIONS_ROLE() external view returns (bytes32);

    function TECH_OPERATIONS_ROLE() external view returns (bytes32);

    function TREASURY_GOVERNANCE_ROLE() external view returns (bytes32);

    function TREASURY_OPERATIONS_ROLE() external view returns (bytes32);

    function UNPAUSER_ROLE() external view returns (bytes32);

    function getRoleAdmin(bytes32 role) external view returns (bytes32);

    function getRoleMember(bytes32 role, uint256 index)
        external
        view
        returns (address);

    function getRoleMemberCount(bytes32 role) external view returns (uint256);

    function grantRole(bytes32 role, address account) external;

    function hasRole(bytes32 role, address account)
        external
        view
        returns (bool);

    function initialize(address _initialContractGovernance) external;

    function initializeNewRole(
        bytes32 role,
        string memory roleString,
        bytes32 adminRole
    ) external;

    function pause() external;

    function paused() external view returns (bool);

    function renounceRole(bytes32 role, address account) external;

    function revokeRole(bytes32 role, address account) external;

    function supportsInterface(bytes4 interfaceId) external view returns (bool);

    function transferFromDisabled() external view returns (bool);

    function unpause() external;
}
