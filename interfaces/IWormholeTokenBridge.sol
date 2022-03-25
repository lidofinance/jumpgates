//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

interface IWormholeTokenBridge {
    function transferTokens(
        address token,
        uint256 amount,
        uint16 recipientChain,
        bytes32 recipient,
        uint256 arbiterFee,
        uint32 nonce
    ) external returns (uint64 sequence);
}
