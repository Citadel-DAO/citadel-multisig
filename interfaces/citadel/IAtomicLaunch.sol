// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

interface IAtomicLaunch {
    function launch(uint256 citadelToLiquidity, uint256 wbtcToLiquidity) external;
}