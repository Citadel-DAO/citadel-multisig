// SPDX-License-Identifier: MIT
// !! THIS FILE WAS AUTOGENERATED BY abi-to-sol v0.5.3. SEE SOURCE BELOW. !!
pragma solidity >=0.7.0 <0.9.0;

interface IKnightingRoundGuestList {
    event Paused(address account);
    event ProveInvitation(address indexed account, bytes32 indexed guestRoot);
    event SetGuestRoot(bytes32 indexed guestRoot);
    event Unpaused(address account);

    function PAUSER_ROLE() external view returns (bytes32);

    function TECH_OPERATIONS_ROLE() external view returns (bytes32);

    function UNPAUSER_ROLE() external view returns (bytes32);

    function __GlobalAccessControlManaged_init(address _globalAccessControl)
        external;

    function authorized(address _guest, bytes32[] memory _merkleProof)
        external
        view
        returns (bool);

    function gac() external view returns (address);

    function guestRoot() external view returns (bytes32);

    function guests(address) external view returns (bool);

    function initialize(address _globalAccessControl) external;

    function pause() external;

    function paused() external view returns (bool);

    function proveInvitation(address account, bytes32[] memory merkleProof)
        external;

    function setGuestRoot(bytes32 guestRoot_) external;

    function setGuests(address[] memory _guests, bool[] memory _invited)
        external;

    function unpause() external;
}

// THIS FILE WAS AUTOGENERATED FROM THE FOLLOWING ABI JSON:
/*
[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"bytes32","name":"guestRoot","type":"bytes32"}],"name":"ProveInvitation","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"guestRoot","type":"bytes32"}],"name":"SetGuestRoot","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"inputs":[],"name":"PAUSER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TECH_OPERATIONS_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"UNPAUSER_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_globalAccessControl","type":"address"}],"name":"__GlobalAccessControlManaged_init","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_guest","type":"address"},{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"}],"name":"authorized","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"gac","outputs":[{"internalType":"contract IGac","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"guestRoot","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"guests","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_globalAccessControl","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"bytes32[]","name":"merkleProof","type":"bytes32[]"}],"name":"proveInvitation","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"guestRoot_","type":"bytes32"}],"name":"setGuestRoot","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"_guests","type":"address[]"},{"internalType":"bool[]","name":"_invited","type":"bool[]"}],"name":"setGuests","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"}]
*/